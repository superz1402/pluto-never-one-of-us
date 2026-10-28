#!/usr/bin/env python3
"""
Ep002 — WHY PLUTO WAS NEVER ONE OF US (owner order 2026-10-28).
Built on the owner-passed proof-factory recipe v1 (CUT/XRAY/KICKER,
deterministic motion: every frame a pure function of t, PIL -> ffmpeg,
24 fps, 1920x1080). Devices reused from the proof: header rule draw,
mode tag slam, kinetic stack slam-in, label card slide-up, archive light
sweep, targeting rings, light pulse + scan band, checklist card,
tightening crop, payoff panel, stamp (overshoot + shake), global fades.
New devices (from proven primitives, per device-ledger rule): case-file
progress bar spanning the film, orbit comet pulse, crowd twinkle,
deterministic film grain (anti-freeze device).
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 24
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(REPO, "assets")
OUT = os.path.join(REPO, "output")
FRAMES = os.path.join(OUT, "frames")
SEG = os.path.join(OUT, "segments")
AUD = os.path.join(OUT, "audio")
CFG = json.load(open(os.path.join(REPO, "script/script.json")))
DUR = json.load(open(os.path.join(AUD, "durations.json")))["durations"]
PAD = CFG["tail_pad"]

INK = (43, 34, 26); RED = (179, 64, 42); CREAM = (238, 230, 210)
EMERALD = (10, 92, 70); PAPER = (238, 228, 203); DARK = (10, 26, 22)
PAYOFF_RED = (232, 110, 84)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def FB(s): return ImageFont.truetype(FONT, s)
def FR(s): return ImageFont.truetype(FONT_R, s)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)

PAPER_PLATES = ("plate-a-pluto-hero.webp", "plate-b-lineup.webp",
                "plate-c-observatory.webp", "plate-e-eris.webp")

# ---------- canvases: plate scaled to 1620x1080, feathered onto ground ----------
def make_canvas(path, ground_rgb, paste_x):
    plate = Image.open(path).convert("RGB")
    plate = plate.resize((1620, 1080), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), ground_rgb)
    mask = Image.new("L", (1620, 1080), 255)
    feather = 90
    m = np.asarray(mask).astype(np.float32)
    ramp = np.linspace(0, 1, feather, dtype=np.float32)
    m[:, :feather] *= ramp[None, :]
    m[:, -feather:] *= ramp[::-1][None, :]
    canvas.paste(plate, (paste_x, 0), Image.fromarray(m.astype(np.uint8)))
    return canvas

CANVASES = {}
def get_canvas(plate):
    if plate not in CANVASES:
        if plate in PAPER_PLATES:
            CANVASES[plate] = make_canvas(os.path.join(ASSETS, plate), (236, 226, 198), 300)
        else:
            CANVASES[plate] = make_canvas(os.path.join(ASSETS, plate), (9, 25, 21), 150)
    return CANVASES[plate]

# ---------- sprites ----------
def text_sprite(text, size, color, font_fn=FB, pad=14):
    f = font_fn(size)
    tmp = Image.new("RGBA", (10, 10)); d = ImageDraw.Draw(tmp)
    bb = d.textbbox((0, 0), text, font=f)
    w, h = bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - bb[0], pad - bb[1]), text, font=f, fill=color + (255,))
    return img

def set_alpha(img, a):
    if a >= 0.999: return img
    out = img.copy(); al = out.split()[3].point(lambda v: int(v * clamp(a)))
    out.putalpha(al); return out

def slam_paste(base, sprite, cx, cy, t, onset, dur=0.22):
    lt = t - onset
    if lt < 0: return
    s = 1.0 + 0.32 * math.exp(-lt / 0.07) * clamp(lt / dur)
    if lt > dur: s = 1.0
    a = clamp(lt / 0.07)
    w2, h2 = int(sprite.width * s), int(sprite.height * s)
    sp = sprite.resize((w2, h2), Image.LANCZOS)
    base.alpha_composite(set_alpha(sp, a), (cx, int(cy - h2 / 2)))

_STAMPS = {}
def stamp_sprite(text):
    if text in _STAMPS: return _STAMPS[text]
    size = 88 if len(text) <= 7 else 64
    ov = Image.new("RGBA", (560, 180), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle([8, 8, 552, 172], outline=RED + (235,), width=10)
    d.rectangle([26, 26, 534, 154], outline=RED + (190,), width=3)
    f = FB(size)
    tw = d.textlength(text, font=f)
    while tw > 500 and size > 40:
        size -= 6; f = FB(size); tw = d.textlength(text, font=f)
    d.text(((560 - tw) / 2, (180 - size) / 2 - 6), text, font=f, fill=RED + (235,))
    r = np.random.default_rng(3); arr = np.asarray(ov).copy()
    arr[r.random(arr.shape[:2]) < 0.15] = (0, 0, 0, 0)
    sp = Image.fromarray(arr).rotate(-6, expand=True, resample=Image.BICUBIC)
    _STAMPS[text] = sp
    return sp

def glow_sprite(n=280, rgb=(210, 255, 225), amax=190):
    y, x = np.mgrid[0:n, 0:n]
    dist = np.sqrt((x - n / 2) ** 2 + (y - n / 2) ** 2) / (n / 2)
    a = np.clip(1 - dist, 0, 1) ** 2 * amax
    arr = np.zeros((n, n, 4), dtype=np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = rgb
    arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")
GLOW = glow_sprite()
GLOW_L = GLOW.resize((440, 440), Image.LANCZOS)
GLOW_WARM = glow_sprite(320, (255, 236, 200), 200)
GLOW_WARM_L = GLOW_WARM.resize((520, 520), Image.LANCZOS)

def light_band():
    n = 520
    a = (np.sin(np.linspace(0, np.pi, n)) ** 2 * 44).astype(np.uint8)
    arr = np.zeros((1080, n, 4), dtype=np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = 255, 246, 214
    arr[..., 3] = np.tile(a[None, :], (1080, 1))
    return Image.fromarray(arr, "RGBA")
BAND = light_band()

def scan_band_dark():
    n = 520
    a = (np.sin(np.linspace(0, np.pi, n)) ** 2 * 40).astype(np.uint8)
    arr = np.zeros((1080, n, 4), dtype=np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = 160, 255, 205
    arr[..., 3] = np.tile(a[None, :], (1080, 1))
    return Image.fromarray(arr, "RGBA")
DBAND = scan_band_dark()

# ---------- per-frame furniture ----------
def header(img, mode, fig, dark, t, onset=0.0):
    d = ImageDraw.Draw(img)
    col = CREAM if dark else INK
    p = ease((t - onset) / 0.8)
    d.text((80, 40), mode, font=FB(38), fill=col)
    tw = d.textlength(fig, font=FB(38))
    d.text((W - 80 - tw, 40), fig, font=FB(38), fill=col)
    if p > 0: d.line([78, 104, 78 + p * (W - 156), 104], fill=col, width=3)

def mode_tag(img, label, dark, t, onset):
    lt = t - onset
    if lt < 0: return
    d = ImageDraw.Draw(img, "RGBA")
    a = int(235 * clamp(lt / 0.1))
    tw = d.textlength(label, font=FB(30))
    d.rectangle([80, 126, 104 + tw + 18, 182], fill=RED + (a,))
    d.text((98, 136), label, font=FB(30), fill=(255, 245, 230, a))

def stack_colors(scene):
    order = {"ink": INK, "cream": CREAM, "red": RED}
    return [order.get(c, INK) for c in scene.get("stack_colors", ["ink"])]

def draw_stack(img, scene, t, y0=330, dy=122, size=92):
    lines = scene.get("stack") or []
    cols = stack_colors(scene)
    for i, (txt, on) in enumerate(lines):
        slam_paste(img, text_sprite(txt, size, cols[i % len(cols)]),
                   64, y0 + i * dy, t, on)

def label_card(img, scene, t, dur):
    lab = scene.get("label")
    if not lab: return
    p = ease((t - 3.2) / 0.5)
    if p <= 0: return
    y0 = int(884 + (1 - p) * 150)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([64, y0 + 10, 700, y0 + 140], fill=(0, 0, 0, 55))
    d.rectangle([60, y0, 696, y0 + 130], fill=(246, 240, 224, 255), outline=INK, width=2)
    f1 = FB(40); f2 = FR(27)
    t1 = lab[0]
    while d.textlength(t1, font=f1) > 600: f1 = FB(f1.size - 2)
    d.text((88, y0 + 18), t1, font=f1, fill=INK)
    t2 = lab[1]
    while d.textlength(t2, font=f2) > 600: f2 = FR(f2.size - 2)
    d.text((88, y0 + 74), t2, font=f2, fill=(96, 74, 50))

def checklist_card(img, scene, t, dur, dark):
    rows = scene.get("checklist")
    if not rows: return
    cross_idx = set(scene.get("tick_cross", []))
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1 = 1250, 1872
    hh = 64 + len(rows) * 62 + 16
    y1 = 936
    y0 = y1 - hh
    card_a = clamp(t / 0.3)
    if dark:
        fill = (12, 24, 20, int(238 * card_a)); ln = CREAM + (int(220 * card_a),)
        txt = CREAM; sub = (150, 200, 175)
    else:
        fill = (246, 240, 224, int(248 * card_a)); ln = INK + (int(230 * card_a),)
        txt = INK; sub = (96, 74, 50)
    d.rectangle([x0, y0, x1, y1], fill=fill)
    d.rectangle([x0, y0, x1, y1], outline=ln, width=2)
    d.text((x0 + 22, y0 + 16), "EXAMINATION NOTES", font=FB(26), fill=sub)
    span0, span1 = 0.30 * dur, 0.72 * dur
    for i, label in enumerate(rows):
        y = y0 + 64 + i * 62
        f = FB(30)
        while d.textlength(label, font=f) > 380: f = FB(f.size - 2)
        d.text((x0 + 72, y), label, font=f, fill=txt)
        d.rectangle([x0 + 26, y + 2, x0 + 60, y + 36], outline=ln, width=3)
        on = span0 + (span1 - span0) * (i / max(1, len(rows) - 1)) if len(rows) > 1 else span0
        if t >= on:
            ok = i not in cross_idx
            col = (140, 255, 190, 255) if dark else EMERALD + (255,)
            bad = RED + (255,)
            c = col if ok else bad
            if ok:
                d.line([x0 + 32, y + 20, x0 + 42, y + 30], fill=c, width=6)
                d.line([x0 + 42, y + 30, x0 + 55, y + 8], fill=c, width=6)
            else:
                d.line([x0 + 32, y + 8, x0 + 54, y + 30], fill=c, width=6)
                d.line([x0 + 54, y + 8, x0 + 32, y + 30], fill=c, width=6)

def big_rules(img, scene, t, dur):
    """s14 RULES: the three planet criteria as large centre-right furniture."""
    rows = scene.get("checklist")
    if not rows: return
    cross_idx = set(scene.get("tick_cross", []))
    d = ImageDraw.Draw(img, "RGBA")
    p = clamp(t / 0.4)
    if p <= 0: return
    x0, x1, y0 = 960, 1868, 330
    d.rectangle([x0, y0, x1, y0 + 56 + len(rows) * 118], fill=(246, 240, 224, int(246 * p)))
    d.rectangle([x0, y0, x1, y0 + 56 + len(rows) * 118], outline=INK + (int(235 * p),), width=3)
    d.text((x0 + 28, y0 + 16), "PLANET REQUIREMENTS — IAU, 2006", font=FB(28), fill=(96, 74, 50))
    span0, span1 = 0.26 * dur, 0.62 * dur
    for i, label in enumerate(rows):
        y = y0 + 74 + i * 118
        f = FB(52)
        while d.textlength(label, font=f) > 620: f = FB(f.size - 2)
        d.text((x0 + 96, y), label, font=f, fill=INK)
        d.rectangle([x0 + 28, y + 6, x0 + 76, y + 54], outline=INK, width=4)
        on = span0 + (span1 - span0) * (i / max(1, len(rows) - 1)) if len(rows) > 1 else span0
        if t >= on:
            ok = i not in cross_idx
            c = EMERALD + (255,) if ok else RED + (255,)
            if ok:
                d.line([x0 + 36, y + 32, x0 + 50, y + 46], fill=c, width=9)
                d.line([x0 + 50, y + 46, x0 + 70, y + 14], fill=c, width=9)
            else:
                d.line([x0 + 36, y + 14, x0 + 68, y + 46], fill=c, width=9)
                d.line([x0 + 68, y + 14, x0 + 36, y + 46], fill=c, width=9)

def sweep_light(img, t, dur, dark):
    if not (0.35 * dur < t < 0.97 * dur): return
    p = ease((t - 0.35 * dur) / (0.62 * dur))
    bx = int(-520 + p * (W + 520))
    img.alpha_composite(DBAND if dark else BAND, (bx, 0))

def rings_at(img, cx, cy, t, onsets, dark=True, r0=34, r1=92):
    d = ImageDraw.Draw(img, "RGBA")
    col = RED if dark else RED
    for cyc in onsets:
        lt = t - cyc
        if 0 <= lt < 1.3:
            r = r0 + (lt / 1.3) * (r1 - r0)
            d.ellipse([cx - r, cy - r, cx + r, cy + r],
                      outline=col + (int(215 * (1 - lt / 1.3)),), width=5)

def progress_bar(img, t_global, total, closing=False):
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1 = 1278, 1872
    d.rectangle([x0, 956, x1, 1040], fill=(236, 226, 198, 242), outline=INK, width=2)
    label = "CASE CLOSED" if closing else "CASE FILE 002 · THE PLUTO HEARING"
    f = FB(24) if closing else FB(22)
    while d.textlength(label, font=f) > 560: f = FB(f.size - 2)
    d.text((x0 + 12, 968), label, font=f, fill=INK)
    d.rectangle([x0 + 12, 1004, x1 - 12, 1028], outline=INK, width=3)
    frac = clamp(t_global / total)
    d.rectangle([x0 + 16, 1008, x0 + 16 + int(566 * frac), 1024], fill=RED)

def stamp_hit(img, text, t, onset):
    lt = t - onset
    if lt < 0: return
    ST = stamp_sprite(text)
    s = 1.0 + 1.1 * math.exp(-lt / 0.09) if lt < 0.45 else 1.0
    sp = ST.resize((int(ST.width * s), int(ST.height * s)), Image.LANCZOS)
    shake = 5 if lt < 0.12 else 0
    img.alpha_composite(sp, (int(1330 - (sp.width - ST.width) / 2) + shake,
                             int(210 - (sp.height - ST.height) / 2)))

# art anchor points (canvas coords; verified on the proof contact sheet)
ANCH = {
    "plate-a-pluto-hero.webp": (1080, 520),
    "plate-d-orbit-xray.webp": (1339, 335),
    "plate-f-kuiper-xray.webp": (700, 300),
    "plate-g-heart-xray.webp": (870, 430),
}

# ---------- deterministic grain (anti-freeze full-frame device) ----------
def grain(img_rgb, fidx):
    rng = np.random.default_rng(fidx * 2654435761 % (2**32))
    arr = np.asarray(img_rgb).astype(np.int16)
    n = rng.integers(-5, 6, (H, W, 1), dtype=np.int16)
    return np.clip(arr + n, 0, 255).astype(np.uint8)

# ---------- choreographies ----------
def ch_hook(img, s, t, dur, dark=False):
    draw_stack(img, s, t)
    label_card(img, s, t, dur)
    if s.get("sweep"): sweep_light(img, t, dur, dark)
    ax, ay = ANCH[s["plate"]]
    if s.get("rings"): rings_at(img, ax, ay, t, (0.42 * dur, 0.68 * dur), dark)
    checklist_card(img, s, t, dur, dark)

def ch_story(img, s, t, dur):
    ch_hook(img, s, t, dur, dark=False)

def ch_status(img, s, t, dur):
    draw_stack(img, s, t)
    ax, ay = ANCH[s["plate"]]
    if s.get("rings"): rings_at(img, ax, ay, t, (0.40 * dur, 0.66 * dur))
    checklist_card(img, s, t, dur, dark=True)
    sweep_light(img, t, dur, True)

def ch_orbit(img, s, t, dur):
    draw_stack(img, s, t)
    ax, ay = ANCH[s["plate"]]
    # comet pulse: travels sun-side -> the eccentric dot, then holds
    pp = clamp((t - 0.6) / (0.42 * dur))
    if 0 < pp < 1:
        px = int(430 + ease(pp) * (ax - 430))
        py = int(500 + ease(pp) * (ay - 500))
        img.alpha_composite(GLOW_L, (px - 220, py - 220))
        d = ImageDraw.Draw(img, "RGBA")
        d.line([430, 500, px, py], fill=(215, 255, 228, 60), width=3)
    if s.get("rings"): rings_at(img, ax, ay, t, (0.5 * dur, 0.72 * dur))
    sweep_light(img, t, dur, True)
    checklist_card(img, s, t, dur, dark=True)

def ch_crowd(img, s, t, dur):
    draw_stack(img, s, t)
    ax, ay = ANCH[s["plate"]]
    if s.get("pulse") == "crowd":
        # deterministic twinkle field — the belt is alive
        rng = np.random.default_rng(42)
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(26):
            x, y = int(rng.random() * W), int(rng.random() * H)
            ph = rng.random()
            a = max(0.0, math.sin(2 * math.pi * (t * 0.35 + ph))) ** 2 * 120
            if a > 8:
                d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(215, 255, 228, int(a)))
    if s.get("rings"): rings_at(img, ax, ay, t, (0.45 * dur, 0.7 * dur))
    sweep_light(img, t, dur, True)
    checklist_card(img, s, t, dur, dark=True)

def ch_heart(img, s, t, dur):
    draw_stack(img, s, t)
    ax, ay = ANCH[s["plate"]]
    # breathing glow on the heart
    br = 0.85 + 0.15 * math.sin(2 * math.pi * t / 2.4)
    if br > 0.05:
        g = GLOW_WARM_L
        w2 = int(g.width * br)
        g2 = g.resize((w2, int(g.height * br)), Image.LANCZOS)
        img.alpha_composite(set_alpha(g2, 0.8), (ax - w2 // 2, ay - g2.height // 2))
    if s.get("rings"): rings_at(img, ax, ay, t, (0.42 * dur, 0.68 * dur))
    sweep_light(img, t, dur, True)
    checklist_card(img, s, t, dur, dark=True)

def ch_rules(img, s, t, dur):
    draw_stack(img, s, t)
    big_rules(img, s, t, dur)
    sweep_light(img, t, dur, False)

def ch_title(img, s, t, dur, t_glob, total):
    # tightening crop handled outside (kicker); big stack + panel
    d = ImageDraw.Draw(img, "RGBA")
    if t > 0.15:
        d.rectangle([52, 220, 1240, 860], fill=(24, 19, 14, 210))
    lines = s["stack"]; cols = stack_colors(s)
    for i, (txt, on) in enumerate(lines):
        c = PAYOFF_RED if cols[i % len(cols)] == RED else CREAM
        slam_paste(img, text_sprite(txt, 116, c), 92, 340 + i * 180, t, on)
    stamp_hit(img, s.get("stamp", "FILED"), t, 2.2)

def ch_payoff(img, s, t, dur, title=False):
    d = ImageDraw.Draw(img, "RGBA")
    if t > 0.4:
        d.rectangle([52, 742, 1150, 1018], fill=(24, 19, 14, 205))
    lines = s.get("payoff") or []
    cols = s.get("payoff_colors", ["cream", "red"])
    for i, (txt, on) in enumerate(lines):
        c = PAYOFF_RED if cols[i % len(cols)] == "red" else CREAM
        size = 62 if len(txt) > 12 else 86
        slam_paste(img, text_sprite(txt, size, c), 84, 830 + i * 112, t, on)
    st_t = s.get("stamp_time") or (dur - 1.65)
    stamp_hit(img, s.get("stamp", "FILED"), t, st_t)

CHOREO = {
    "HOOK": ch_hook, "STORY": ch_story, "STATUS": ch_status,
    "ORBIT": ch_orbit, "CROWD": ch_crowd, "HEART": ch_heart,
    "RULES": ch_rules, "TITLE": ch_title,
    "CROP_PAYOFF": ch_payoff, "OUTRO": ch_payoff,
}

def scene_duration(s):
    return DUR[s["id"]] if s.get("dialogue") else CFG["title_scene_seconds"]

def render_frame(si, t, t_glob, total, fidx):
    s = CFG["scenes"][si]
    dur = scene_duration(s)
    # dark grounds get cream furniture; paper grounds get ink furniture —
    # keyed on the plate ground, not the mode (KICKER crops the paper plate)
    dark = s["plate"] not in PAPER_PLATES
    base = get_canvas(s["plate"])
    if s["choreo"] in ("CROP_PAYOFF", "OUTRO"):
        p = ease(t / max(0.001, dur - 1.2)) * 0.92
        cw = int(1920 - p * 500); ch = int(1080 - p * 281)
        cx = int(p * 460); cy = int(p * 170)
        img = base.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.LANCZOS).convert("RGBA")
    elif s["choreo"] == "TITLE":
        p = ease(t / 1.4) * 0.5
        cw = int(1920 - p * 500); ch = int(1080 - p * 281)
        cx = int(p * 460); cy = int(p * 170)
        img = base.crop((cx, cy, cx + cw, cy + ch)).resize((W, H), Image.LANCZOS).convert("RGBA")
    else:
        img = base.convert("RGBA")
    header(img, s["mode"], s["fig"], dark, t)
    mode_tag(img, f"MODE: {s['mode']}", dark, t, 0.25)
    CHOREO[s["choreo"]](img, s, t, dur) if s["choreo"] != "TITLE" else ch_title(img, s, t, dur, t_glob, total)
    closing = s.get("case_close") and t > dur - 2.2
    progress_bar(img, t_glob, total, closing)
    out = img.convert("RGB")
    arr = grain(out, fidx)
    f = clamp(t_glob / 0.4)
    tail = total - t_glob
    if tail < 0.8: f = min(f, clamp(tail / 0.8))
    if f < 1.0:
        arr = (arr.astype(np.float32) * f).astype(np.uint8)
    return Image.fromarray(arr)

# ---------- rendering drivers ----------
def render_scenes(scene_ids, tag):
    total_all = sum(scene_duration(s) + PAD for s in CFG["scenes"])
    starts = {}
    acc = 0.0
    for s in CFG["scenes"]:
        starts[s["id"]] = acc
        acc += scene_duration(s) + PAD
    total = acc
    for sid in scene_ids:
        si = next(i for i, s in enumerate(CFG["scenes"]) if s["id"] == sid)
        s = CFG["scenes"][si]
        dur = scene_duration(s) + PAD
        n = int(round(dur * FPS))
        fdir = os.path.join(FRAMES, sid)
        os.makedirs(fdir, exist_ok=True)
        t0 = starts[sid]
        for i in range(n):
            fpath = os.path.join(fdir, f"f{i:04d}.jpg")
            if os.path.exists(fpath): continue
            t = i / FPS
            render_frame(si, min(t, dur), t0 + t, total, int(round((t0 + t) * FPS))
                         ).save(fpath, quality=88)
        print(f"[{tag}] {sid}: {n} frames done", flush=True)

def encode_segment(sid):
    fdir = os.path.join(FRAMES, sid)
    dur = scene_duration(next(s for s in CFG["scenes"] if s["id"] == sid)) + PAD
    n = int(round(dur * FPS))
    seg = os.path.join(SEG, f"{sid}.mp4")
    os.makedirs(SEG, exist_ok=True)
    ap = os.path.join(AUD, f"{sid}.mp3")
    if os.path.exists(ap):
        vf = ["-framerate", str(FPS), "-i", os.path.join(fdir, "f%04d.jpg"),
              "-i", ap, "-af", f"apad=whole_dur={dur:.3f}",
              "-map", "0:v", "-map", "1:a"]
    else:
        vf = ["-framerate", str(FPS), "-i", os.path.join(fdir, "f%04d.jpg"),
              "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
              "-map", "0:v", "-map", "1:a"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *vf,
                    "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "44100", "-ac", "2", "-movflags", "+faststart", seg],
                   check=True)
    return seg

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "proof":
        # 12s proof: hook (s01) 4s / orbit (s08) 4s / verdict (s16) 4s
        os.makedirs(os.path.join(FRAMES, "proof"), exist_ok=True)
        picks = [("s01", 0.0, 4.0), ("s08", 0.0, 4.0), ("s16", 0.0, 4.0)]
        idx = 0
        for sid, a, b in picks:
            si = next(i for i, s in enumerate(CFG["scenes"]) if s["id"] == sid)
            s = CFG["scenes"][si]
            dur = scene_duration(s)
            n = int((b - a) * FPS)
            for i in range(n):
                t = a + i / FPS
                render_frame(si, min(t, dur), t, (b - a) * 3, idx
                             ).save(os.path.join(FRAMES, "proof", f"f{idx:04d}.jpg"), quality=90)
                idx += 1
        outp = os.path.join(OUT, "motion-proof-12s.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", os.path.join(FRAMES, "proof", "f%04d.jpg"),
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", outp], check=True)
        print("PROOF DONE", outp)
        return
    if mode == "frames":
        ids = sys.argv[2].split(",") if len(sys.argv) > 2 else [s["id"] for s in CFG["scenes"]]
        render_scenes(ids, "frames")
        return
    if mode == "encode":
        ids = sys.argv[2].split(",") if len(sys.argv) > 2 else [s["id"] for s in CFG["scenes"]]
        for sid in ids:
            encode_segment(sid)
            print("encoded", sid, flush=True)
        return
    if mode == "concat":
        segs = [os.path.join(SEG, f"{s['id']}.mp4") for s in CFG["scenes"]]
        lst = os.path.join(SEG, "list.txt")
        with open(lst, "w") as f:
            for p in segs: f.write(f"file '{p}'\n")
        outp = os.path.join(OUT, "ep002-pluto.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                        "-safe", "0", "-i", lst, "-c", "copy", outp], check=True)
        print("CONCAT DONE", outp)

if __name__ == "__main__":
    main()
