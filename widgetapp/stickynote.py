#!/usr/bin/env python3
"""119-handwritten-note: a photo of a handwritten sticky note (callback request) with a name and phone number,
next to a printed note with a different number. Task: the handwritten phone number. complete = digits match."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFilter
import base, perception, receipt
TITLE = "Desk photo"; W, H = 960, 560; QUESTION = "What phone number is written on the HANDWRITTEN sticky note? Enter digits only."
NAMES = ["Marta Kowalski", "Dev Anand", "Yusuf Demir", "Ines Carvalho", "Tomas Berg", "Aiko Tanaka"]
S = {"name": "", "phone": "", "printed": ""}


def reset():
    S["name"] = random.choice(NAMES); S["phone"] = f"{random.randint(200, 989)} {random.randint(200, 999)} {random.randint(1000, 9999)}"; S["printed"] = f"{random.randint(200, 989)} {random.randint(200, 999)} {random.randint(1000, 9999)}"


def draw():
    img = Image.new("RGB", (W, H), (96, 84, 70)); d = ImageDraw.Draw(img)
    note = Image.new("RGB", (330, 330), (252, 232, 120)); nd = ImageDraw.Draw(note); hf = receipt.hand_font(34); hs = receipt.hand_font(26)
    nd.text((22, 30), "Call back:", fill=(30, 40, 120), font=hs); nd.text((22, 80), S["name"], fill=(30, 40, 120), font=hf)
    nd.text((22, 150), S["phone"], fill=(30, 40, 120), font=receipt.hand_font(40)); nd.text((22, 230), "re: invoice, before 3pm", fill=(30, 40, 120), font=hs)
    note = note.rotate(random.Random(len(S["name"])).uniform(-9, 9), expand=True, resample=Image.BICUBIC, fillcolor=(96, 84, 70)); img.paste(note, (80, 90))
    card = Image.new("RGB", (360, 200), (250, 250, 250)); cd = ImageDraw.Draw(card); cd.text((20, 20), "Northwind Support", fill=(30, 30, 30), font=base.font(22)); cd.text((20, 60), "Main line", fill=(90, 90, 90), font=base.font(15, False)); cd.text((20, 84), S["printed"], fill=(30, 30, 30), font=base.font(26)); cd.text((20, 140), "Mon-Fri 9-6", fill=(90, 90, 90), font=base.font(15, False))
    card = card.rotate(3, expand=True, resample=Image.BICUBIC, fillcolor=(96, 84, 70)); img.paste(card, (520, 220))
    return img.filter(ImageFilter.GaussianBlur(0.5))


def check(s):
    return "".join(ch for ch in s if ch.isdigit()) == S["phone"].replace(" ", "")


def answer_state(): return {"phone": S["phone"], "printed_decoy": S["printed"], "name": S["name"]}


perception.make(sys.modules[__name__], W, H)
if __name__ == "__main__":
    base.serve(sys.modules[__name__], 8837)
