#!/usr/bin/env python3
"""Shared, idempotent, resumable work queue for the final-set matrix sweep.
Store: env MATRIX_STORE = s3://bucket/prefix (fleet) or a local directory (tests). Keys under the store:
  pending/<task>__<label>        {task,label,lane}            work to do (lane: local | realsite)
  claims/<task>__<label>         {worker,host,ts}             leased by a worker; heartbeat refreshes ts
  done/<task>__<label>           {task,label,worker,pass,...} finished (raw bundle uploaded under raw/)
  failed/<task>__<label>         {attempts,last_error}        gave up after MAX_TRIES harness failures
  blocked/<task>__<label>        {count,last}                 bot wall seen (kept pending until count>=3)
  raw/<task>.<label>.json (+ .mp4, .shot*.jpg, .stream.txt) and results/<task>/<label>.json
Commands:
  init [--attempts N]            add pending markers for every missing (task,label) in the final set
  claim <worker> [--lane L] [--family f1,f2]   atomically claim one pending item (family = config prefixes, spreads providers across workers) (stale leases > LEASE_S are reclaimed); prints "task label"
  heartbeat <task> <label> <worker>
  complete <task> <label> <worker> [--blocked | --error MSG]   upload artifacts, mark done / requeue / fail
  status [--configs]             per-config table: done / running / pending / failed / blocked, plus pass counts
  workers                        active leases per worker with age
  sync                           download every done run's raw bundle and result json into local raw/ and results/
  reset-stale                    release leases older than LEASE_S (also done implicitly by claim)"""
import json, os, sys, time, socket, glob, io
LEASE_S = int(os.environ.get("LEASE_S", "1500")); MAX_TRIES = 3
STORE = os.environ.get("MATRIX_STORE", "results/matrix_store")
REALSITE_KINDS = {"judge"}


class Local:
    def __init__(self, root): self.root = root; os.makedirs(root, exist_ok=True)
    def _p(self, k): p = os.path.join(self.root, k); os.makedirs(os.path.dirname(p), exist_ok=True); return p
    def list(self, prefix): return sorted(os.path.relpath(p, self.root) for p in glob.glob(os.path.join(self.root, prefix, "**"), recursive=True) if os.path.isfile(p))
    def get(self, k):
        try: return open(self._p(k), "rb").read()
        except FileNotFoundError: return None
    def put(self, k, data, if_none=False, if_match=None):
        p = self._p(k)
        if if_none:
            try: fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError: return False
            os.write(fd, data); os.close(fd); return True
        if if_match is not None:
            cur = self.get(k)
            if cur is None or self.etag(cur) != if_match: return False
        open(p, "wb").write(data); return True
    def delete(self, k):
        try: os.remove(self._p(k))
        except FileNotFoundError: pass
    def put_file(self, k, path): self.put(k, open(path, "rb").read())
    def get_file(self, k, path): d = self.get(k); os.makedirs(os.path.dirname(path) or ".", exist_ok=True); open(path, "wb").write(d)
    @staticmethod
    def etag(data): import hashlib; return hashlib.md5(data).hexdigest()
    def head_etag(self, k): d = self.get(k); return None if d is None else self.etag(d)


class S3:
    def __init__(self, url):
        import boto3; from botocore.exceptions import ClientError
        self.ClientError = ClientError; b, _, p = url[5:].partition("/"); self.b, self.pre = b, p.rstrip("/") + "/" if p else ""; self.c = boto3.client("s3")
    def _k(self, k): return self.pre + k
    def list(self, prefix):
        out = []; tok = None
        while True:
            kw = dict(Bucket=self.b, Prefix=self._k(prefix)); kw.update(ContinuationToken=tok) if tok else None
            r = self.c.list_objects_v2(**kw); out += [o["Key"][len(self.pre):] for o in r.get("Contents", [])]
            if not r.get("IsTruncated"): return out
            tok = r["NextContinuationToken"]
    def get(self, k):
        try: return self.c.get_object(Bucket=self.b, Key=self._k(k))["Body"].read()
        except self.ClientError as e:
            if e.response["Error"]["Code"] in ("NoSuchKey", "404"): return None
            raise
    def put(self, k, data, if_none=False, if_match=None):
        kw = dict(Bucket=self.b, Key=self._k(k), Body=data)
        if if_none: kw["IfNoneMatch"] = "*"
        if if_match is not None: kw["IfMatch"] = if_match
        try: self.c.put_object(**kw); return True
        except self.ClientError as e:
            if e.response["Error"]["Code"] in ("PreconditionFailed", "412", "ConditionalRequestConflict", "409"): return False
            raise
    def delete(self, k): self.c.delete_object(Bucket=self.b, Key=self._k(k))
    def put_file(self, k, path): self.c.upload_file(path, self.b, self._k(k))
    def get_file(self, k, path): os.makedirs(os.path.dirname(path) or ".", exist_ok=True); self.c.download_file(self.b, self._k(k), path)
    def head_etag(self, k):
        try: return self.c.head_object(Bucket=self.b, Key=self._k(k))["ETag"]
        except self.ClientError: return None


def store(): return S3(STORE) if STORE.startswith("s3://") else Local(STORE)
def key(t, l): return f"{t}__{l}"
def j(d): return json.dumps(d).encode()
def lane_of(task):
    import harness; return "realsite" if harness.TASKS[task]["kind"] in REALSITE_KINDS else "local"


def final_tasks(): return list(json.load(open("results/core_set.json"))) + list(json.load(open("results/validated_set.json")))
CONFIGS = os.environ.get("MATRIX_CONFIGS", "").split() or (
    [f"spark13-{e}" for e in ("low", "medium", "high", "xhigh", "ultra")] + [f"sonnet-{e}" for e in ("low", "medium", "high", "xhigh", "max")]
    + [f"opus-{e}" for e in ("low", "medium", "high", "xhigh", "max")] + [f"gemini-3.8-flash-{e}" for e in ("low", "medium", "high")]
    + [f"luna-{e}" for e in ("low", "medium", "high", "xhigh", "max")])
def label(cfg, a): return f"{cfg}-val" + ("" if a == 1 else str(a))
def cfg_of(label_): return label_.split("-val")[0]


def cmd_init(S, args):
    att = int(args[args.index("--attempts") + 1]) if "--attempts" in args else 1
    have = {k.split("/", 1)[1] for k in S.list("pending/") + S.list("done/") + S.list("failed/") + S.list("claims/")}
    n = 0
    for a in range(1, att + 1):
        for t in final_tasks():
            for c in CONFIGS:
                l = label(c, a)
                if key(t, l) in have: continue
                if os.path.exists(f"raw/{t}.{l}.json") or (a == 1 and os.path.exists(f"raw/{t}.{c}.json")):
                    # already run locally: register as done and upload the bundle so the fleet skips it
                    cmd_complete(S, [t, l, "local-import"], quiet=True); n += 1; continue
                S.put(f"pending/{key(t, l)}", j({"task": t, "label": l, "lane": lane_of(t)}), if_none=True); n += 1
    print("init: registered", n, "items")


def stale(S, k):
    d = S.get(k)
    if not d: return True
    return time.time() - json.loads(d).get("ts", 0) > LEASE_S


def cmd_claim(S, args):
    worker = args[0]; lane = args[args.index("--lane") + 1] if "--lane" in args else None
    fams = args[args.index("--family") + 1].split(",") if "--family" in args else None   # config family prefixes, e.g. sonnet,opus
    pend = S.list("pending/"); import random; random.shuffle(pend)
    claimed = {k.split("/", 1)[1] for k in S.list("claims/")}
    for k in pend:
        item = json.loads(S.get(k) or b"{}")
        if lane and item.get("lane") != lane: continue
        if fams and not any(cfg_of(item["label"]) == f or cfg_of(item["label"]).startswith(f + "-") for f in fams): continue
        ck = "claims/" + k.split("/", 1)[1]; body = j({"worker": worker, "host": socket.gethostname(), "ts": time.time(), "task": item["task"], "label": item["label"]})
        if k.split("/", 1)[1] in claimed:
            if not stale(S, ck): continue
            et = S.head_etag(ck)
            if et is None or not S.put(ck, body, if_match=et): continue
        elif not S.put(ck, body, if_none=True): continue
        print(item["task"], item["label"]); return
    print("")


def cmd_heartbeat(S, args):
    t, l, w = args[:3]; S.put(f"claims/{key(t, l)}", j({"worker": w, "host": socket.gethostname(), "ts": time.time(), "task": t, "label": l}))


def cmd_complete(S, args, quiet=False):
    t, l, w = args[:3]; k = key(t, l)
    if "--blocked" in args or "--error" in args:
        fk = "failed/" + k if "--error" in args else "blocked/" + k; prev = json.loads(S.get(fk) or b"{}"); n = prev.get("attempts", prev.get("count", 0)) + 1
        msg = args[args.index("--error") + 1] if "--error" in args else "bot wall"
        S.delete(f"claims/{k}")
        if n >= MAX_TRIES:
            S.put(fk, j({"attempts": n, "last_error": msg, "worker": w, "ts": time.time()})); S.delete(f"pending/{k}"); print("gave up", t, l); return
        S.put(fk, j({"attempts": n, "count": n, "last_error": msg, "worker": w, "ts": time.time()}))
        # keep the raw bundle of the failed attempt for audit, then remove it locally so a retry can record afresh
        for f in glob.glob(f"raw/{t}.{l}.*"): S.put_file(f"attempts/{k}/{n}/{os.path.basename(f)}", f); os.remove(f)
        for f in glob.glob(f"results/{t}/{l}.*"): os.remove(f)
        print("requeued", t, l, "attempt", n); return
    files = glob.glob(f"raw/{t}.{l}.*") + glob.glob(f"results/{t}/{l}.*")
    if not os.path.exists(f"raw/{t}.{l}.json"):
        # local-import of an older label without -val suffix
        c = cfg_of(l); files = glob.glob(f"raw/{t}.{c}.*") + glob.glob(f"results/{t}/{c}.*")
    if w == "local-import": files = [f for f in files if f.endswith(".json")]   # runs already on the workstation: metadata only
    for f in files: S.put_file(f.replace(f"raw/{t}.{cfg_of(l)}.", f"raw/{t}.{l}."), f)
    res = {}
    for cand in (f"results/{t}/{l}.json", f"results/{t}/{cfg_of(l)}.json"):
        if os.path.exists(cand): res = json.load(open(cand)); break
    S.put(f"done/{k}", j({"task": t, "label": l, "worker": w, "ts": time.time(), "success": res.get("success"), "needs_judge": res.get("needs_judge"), "blocked": res.get("blocked"), "cli_calls": res.get("cli_calls"), "wall_s": res.get("wall_s")}))
    S.delete(f"pending/{k}"); S.delete(f"claims/{k}")
    if not quiet: print("done", t, l)


def table(S):
    rows = {}
    def add(kind, k, extra=None):
        t, l = k.split("/", 1)[1].split("__"); c = cfg_of(l); r = rows.setdefault(c, {"done": 0, "running": 0, "pending": 0, "failed": 0, "blocked": 0, "pass": 0, "judge_pending": 0})
        r[kind] += 1
        if kind == "done" and extra:
            if extra.get("success") is True: r["pass"] += 1
            elif extra.get("needs_judge") and extra.get("success") is None: r["judge_pending"] += 1
    claims = {k.split("/", 1)[1] for k in S.list("claims/") if not stale(S, k)}
    for k in S.list("pending/"):
        add("running" if k.split("/", 1)[1] in claims else "pending", k)
    for k in S.list("done/"): add("done", k, json.loads(S.get(k) or b"{}"))
    for k in S.list("failed/"): add("failed", k)
    for k in S.list("blocked/"): add("blocked", k)
    return rows


def cmd_status(S, args):
    rows = table(S); tot = {"done": 0, "running": 0, "pending": 0, "failed": 0, "pass": 0}
    print(f"{'config':26} {'done':>5} {'pass':>5} {'judg':>4} {'run':>4} {'pend':>5} {'fail':>4} {'blk':>4}")
    for c in CONFIGS + [c for c in rows if c not in CONFIGS]:
        r = rows.get(c)
        if not r: continue
        print(f"{c:26} {r['done']:5} {r['pass']:5} {r['judge_pending']:4} {r['running']:4} {r['pending']:5} {r['failed']:4} {r['blocked']:4}")
        for k in tot: tot[k] += r[k]
    print(f"{'TOTAL':26} {tot['done']:5} {tot['pass']:5} {'':4} {tot['running']:4} {tot['pending']:5} {tot['failed']:4}")


def cmd_workers(S, args):
    now = time.time()
    for k in S.list("claims/"):
        d = json.loads(S.get(k) or b"{}"); age = now - d.get("ts", now); print(f"{d.get('worker','?'):20} {d.get('host','?'):24} {d.get('task','?'):28} {d.get('label','?'):26} lease age {age:5.0f}s{'  STALE' if age > LEASE_S else ''}")


def cmd_sync(S, args):
    n = 0
    for k in S.list("raw/") + S.list("results/"):
        if not os.path.exists(k): S.get_file(k, k); n += 1
    print("downloaded", n, "files")


def cmd_reindex(S, args):
    n = 0
    for k in S.list("done/"):
        t, l = k.split("/", 1)[1].split("__"); d = json.loads(S.get(k) or b"{}")
        for cand in (f"results/{t}/{l}.json", f"results/{t}/{cfg_of(l)}.json"):
            if os.path.exists(cand):
                res = json.load(open(cand)); d.update(success=res.get("success"), needs_judge=res.get("needs_judge"), blocked=res.get("blocked"), cli_calls=res.get("cli_calls"), wall_s=res.get("wall_s")); S.put(k, j(d)); n += 1; break
    print("reindexed", n)


def cmd_reset_stale(S, args):
    for k in S.list("claims/"):
        if stale(S, k): S.delete(k); print("released", k)


if __name__ == "__main__":
    S = store(); cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"init": cmd_init, "claim": cmd_claim, "heartbeat": cmd_heartbeat, "complete": cmd_complete, "status": cmd_status, "workers": cmd_workers, "sync": cmd_sync, "reindex": cmd_reindex, "reset-stale": cmd_reset_stale}[cmd](S, sys.argv[2:])
