#!/usr/bin/env python3
"""Ep002 assembly + QA gates (contract: ffprobe, freezedetect, contact sheet).
Concat per-scene segments -> mix deterministic music bed -> run QA gates."""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "output")
SEG = os.path.join(OUT, "segments")
CFG = json.load(open(os.path.join(REPO, "script/script.json")))
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def FBf(s): return ImageFont.truetype(FB, s)

def sh(cmd):
    subprocess.run(cmd, check=True)

def concat():
    lst = os.path.join(SEG, "list.txt")
    with open(lst, "w") as f:
        for s in CFG["scenes"]:
            f.write(f"file '{os.path.join(SEG, s['id'] + '.mp4')}'\n")
    silent = os.path.join(OUT, "ep002-pluto-silent.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", lst, "-c", "copy", silent])
    return silent

def mix(silent):
    final = os.path.join(OUT, "ep002-pluto.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", silent,
        "-i", os.path.join(OUT, "audio/music.wav"),
        "-filter_complex",
        "[1:a]volume=0.45[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final])
    return final

def ffprobe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=codec_name,width,height,avg_frame_rate:format=duration,size,bit_rate",
                        "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)

def freezedetect(path):
    r = subprocess.run(["ffmpeg", "-vf", "freezedetect=n=-50dB:d=2.5",
                        "-f", "null", "-"], stderr=subprocess.PIPE, text=True, input="")
    freezes = re.findall(r"freeze_start: ([0-9.]+)", r.stderr)
    return freezes

def contact_sheet(path):
    outp = os.path.join(OUT, "qa/final-contact-sheet.jpg")
    probe = ffprobe(path)
    dur = float(probe["format"]["duration"])
    times = [dur * f for f in (0.02, 0.08, 0.16, 0.24, 0.32, 0.40,
                               0.48, 0.56, 0.64, 0.72, 0.80, 0.88, 0.94, 0.985)]
    cols, rows = 4, 4
    tw, th = 480, 270
    sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 34) + 12), (18, 15, 12))
    d = ImageDraw.Draw(sheet)
    for i, ts in enumerate(times):
        p = os.path.join(OUT, "qa", f"final_{i:02d}.jpg")
        sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ts:.2f}", "-i", path,
            "-frames:v", "1", "-q:v", "3", p])
        im = Image.open(p).convert("RGB"); im.thumbnail((tw, th))
        x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 34)
        sheet.paste(im, (x, y))
        d.text((x + 4, y + th + 4), f"t={ts:.0f}s", font=FBf(18), fill=(255, 235, 190))
    sheet.save(outp, quality=90)
    return outp

def telegram_cut(final):
    """Bot API sendVideo caps at 50 MB — ship a 720p cut for Telegram."""
    outp = os.path.join(OUT, "ep002-pluto-telegram.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", final,
        "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "medium",
        "-crf", "27", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", outp])
    return outp

def main():
    silent = concat()
    final = mix(silent)
    os.remove(silent)
    probe = ffprobe(final)
    print("== FFPROBE ==")
    print(json.dumps(probe, indent=1))
    size_mb = int(probe["format"]["size"]) / 1e6
    print(f"size: {size_mb:.1f} MB")
    print("== FREEZEDETECT (n=-50dB:d=2.5) ==")
    fr = freezedetect(final)
    print("freezes:", fr if fr else "NONE — PASS")
    sheet = contact_sheet(final)
    print("sheet:", sheet)
    tcut = telegram_cut(final)
    print("telegram cut:", tcut, f"{os.path.getsize(tcut)/1e6:.1f} MB")
    json.dump({"freezes": fr, "size_mb": round(size_mb, 1),
               "telegram_mb": round(os.path.getsize(tcut)/1e6, 1),
               "probe": probe},
              open(os.path.join(OUT, "qa/final-qa.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
