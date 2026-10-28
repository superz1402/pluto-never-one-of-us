#!/usr/bin/env python3
"""Normalize Ep002 plates to the proven geometry (see assets/prompts.md):
raw 1344x768 -> symmetric 96px side-crop to 3:2 -> LANCZOS 1920x1280 -> WebP q90.
Also builds the plates contact sheet for in-frame QA."""
import os
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO, "assets/raw")
OUT = os.path.join(REPO, "assets")

PLATES = [
    "plate-a-pluto-hero", "plate-b-lineup", "plate-c-observatory",
    "plate-d-orbit-xray", "plate-e-eris", "plate-f-kuiper-xray",
    "plate-g-heart-xray",
]

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def FBf(s): return ImageFont.truetype(FB, s)

for name in PLATES:
    src = os.path.join(RAW, f"{name}.png")
    dst = os.path.join(OUT, f"{name}.webp")
    img = Image.open(src).convert("RGB")
    w, h = img.size
    assert (w, h) == (1344, 768), f"unexpected size {w}x{h} for {name}"
    # symmetric 96px side-crop -> 1152x768 (3:2)
    img = img.crop((96, 0, w - 96, h))
    img = img.resize((1920, 1280), Image.LANCZOS)
    img.save(dst, "WEBP", quality=90)
    print(f"{name}.webp  {os.path.getsize(dst):,} B")

# contact sheet: 4 x 2 grid of 16:9 letterboxed thumbnails
cols, rows = 4, 2
tw, th = 480, 282
sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 40) + 12), (18, 15, 12))
d = ImageDraw.Draw(sheet)
for i, name in enumerate(PLATES):
    im = Image.open(os.path.join(OUT, f"{name}.webp")).convert("RGB")
    im.thumbnail((tw, th))
    x = 12 + (i % cols) * (tw + 12)
    y = 12 + (i // cols) * (th + 40)
    sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
    d.text((x + 4, y + th + 6), name, font=FBf(18), fill=(255, 235, 190))
outp = os.path.join(REPO, "output/qa/plates-contact-sheet.jpg")
sheet.save(outp, quality=90)
print("sheet:", outp)
