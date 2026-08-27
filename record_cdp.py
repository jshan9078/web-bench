#!/usr/bin/env python3
"""Headless per-run video recorder via Chrome DevTools screencast — NO visible window.

    python3 record_cdp.py <sid> <out.mp4>

Finds the session's page target (the harness tags its title `REC-<sid>` at setup so we can locate it
across all running Chrome endpoints), opens a SECOND CDP client to that target, and records
Page.screencastFrame events. On SIGTERM/SIGINT it stops, then assembles the JPEG frames into an mp4
with real inter-frame timing via ffmpeg (frames kept if ffmpeg is absent).

Discovery: reads `DevToolsActivePort` (line 1 = port) from every ~/.browser-daemon/profiles/*/ and
$TMPDIR/browser-daemon-*/ dir, queries http://127.0.0.1:<port>/json, and matches title == REC-<sid>.
"""
import asyncio, base64, json, os, signal, subprocess, sys, tempfile, urllib.request
from pathlib import Path

try:
    import websockets
except Exception:
    print("record_cdp: `websockets` not available in this python", file=sys.stderr); sys.exit(3)


def candidate_ports():
    dirs = list((Path.home() / ".browser-daemon" / "profiles").glob("*"))
    dirs += list(Path(os.environ.get("TMPDIR", "/tmp")).glob("browser-daemon-*"))
    ports = []
    for d in dirs:
        f = d / "DevToolsActivePort"
        if f.exists():
            try:
                ports.append(int(f.read_text().splitlines()[0].strip()))
            except Exception:
                pass
    return sorted(set(ports))


def find_target(sid):
    marker = f"REC-{sid}"
    for port in candidate_ports():
        try:
            data = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=1))
        except Exception:
            continue
        for t in data:
            if t.get("type") == "page" and (t.get("title", "") == marker or t.get("title", "").startswith(marker)):
                return t.get("webSocketDebuggerUrl")
    return None


async def run(sid, out):
    ws_url = None
    for _ in range(40):  # the page may take a moment to get its marker title
        ws_url = find_target(sid)
        if ws_url:
            break
        await asyncio.sleep(0.25)
    if not ws_url:
        print(f"record_cdp: no target titled REC-{sid} found", file=sys.stderr); return
    frames_dir = Path(tempfile.mkdtemp(prefix="rec-"))
    frames = []  # (path, timestamp)
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(s, stop.set)
    async with websockets.connect(ws_url, max_size=None, ping_interval=None) as ws:
        mid = [0]
        async def send(method, params=None):
            mid[0] += 1
            await ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
        await send("Page.enable")
        await send("Page.startScreencast", {"format": "jpeg", "quality": 60,
                                            "maxWidth": 1280, "maxHeight": 900, "everyNthFrame": 1})
        n = 0
        while not stop.is_set():
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=0.5)
            except asyncio.TimeoutError:
                continue
            except Exception:
                break
            msg = json.loads(raw)
            if msg.get("method") == "Page.screencastFrame":
                p = msg["params"]
                fp = frames_dir / f"f{n:06d}.jpg"; fp.write_bytes(base64.b64decode(p["data"]))
                ts = p.get("metadata", {}).get("timestamp")
                frames.append((fp, ts)); n += 1
                try:
                    await send("Page.screencastFrameAck", {"sessionId": p["sessionId"]})
                except Exception:
                    break
        try:
            await send("Page.stopScreencast")
        except Exception:
            pass
    assemble(frames, out)
    print(f"record_cdp: {len(frames)} frames -> {out}", file=sys.stderr)


def assemble(frames, out):
    if not frames:
        print("record_cdp: no frames captured (screencast may be unsupported on this build)", file=sys.stderr)
        return
    # per-frame durations from timestamps (fallback 0.1s); concat demuxer -> variable frame rate mp4
    ts = [t for _, t in frames]
    base = next((x for x in ts if x is not None), 0.0)
    durs = []
    for i in range(len(frames)):
        if i + 1 < len(frames) and ts[i] is not None and ts[i + 1] is not None:
            durs.append(max(0.02, ts[i + 1] - ts[i]))
        else:
            durs.append(0.1)
    listfile = Path(frames[0][0]).parent / "list.txt"
    with listfile.open("w") as f:
        for (fp, _), d in zip(frames, durs):
            f.write(f"file '{fp}'\nduration {d:.3f}\n")
        f.write(f"file '{frames[-1][0]}'\n")  # concat demuxer needs the last file repeated
    try:
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
                        "-vsync", "vfr", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
                       check=True, capture_output=True)
    except Exception as e:
        print(f"record_cdp: ffmpeg failed ({e}); frames kept in {frames[0][0].parent}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(run(sys.argv[1], sys.argv[2]))
