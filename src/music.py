#!/usr/bin/env python3
"""Ep002 music bed — deterministic synthesized dark-archive ambient.
Pure functions of t (same determinism contract as the picture): layered
detuned drone + filtered air + heartbeat pulse + synced SFX cues
(stamp thumps at payoff stamps, paper ticks at checklist marks).
Cue times replicate motion.py formulas from script.json + durations.json
(single source of truth; noted in the run report)."""
import json, math, os
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(REPO, "script/script.json")))
DUR = json.load(open(os.path.join(REPO, "output/audio/durations.json")))["durations"]
SR = 44100

def scene_duration(s):
    return DUR[s["id"]] if s.get("dialogue") else CFG["title_scene_seconds"]

def build_cues():
    cues = []  # (abs_time, kind)
    acc = 0.0
    for s in CFG["scenes"]:
        dur = scene_duration(s)
        if s["choreo"] in ("CROP_PAYOFF", "OUTRO"):
            st = s.get("stamp_time") or (dur - 1.65)
            cues.append((acc + st, "stamp"))
        elif s["choreo"] == "TITLE":
            cues.append((acc + 2.2, "stamp"))
        rows = s.get("checklist") or []
        if rows:
            span0, span1 = 0.30 * dur, 0.72 * dur
            for i in range(len(rows)):
                on = span0 + (span1 - span0) * (i / max(1, len(rows) - 1)) if len(rows) > 1 else span0
                cues.append((acc + on, "tick"))
        acc += dur + CFG["tail_pad"]
    return cues, acc

def env_exp(n, decay):
    return np.exp(-np.arange(n) / (SR * decay))

def thump(freq0=130.0, freq1=52.0, dur_s=0.42, amp=0.5):
    n = int(SR * dur_s)
    t = np.arange(n) / SR
    f = freq0 + (freq1 - freq0) * (t / dur_s)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env_exp(n, 0.09) * amp
    click = (np.random.default_rng(5).random(n) * 2 - 1) * env_exp(n, 0.004) * amp * 0.25
    return x + click

def tick(amp=0.05):
    n = int(SR * 0.05)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 1750 * t) * env_exp(n, 0.008) * amp
    return x

def main():
    cues, total = build_cues()
    total += 1.2
    n = int(SR * total)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)

    # drone: A1 + beat-detune + fifth, slow LFO breathing
    lfo = 0.75 + 0.25 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t - 1.2))
    droneL = (np.sin(2 * np.pi * 55.00 * t) * 0.050 +
              np.sin(2 * np.pi * 55.33 * t) * 0.038 +
              np.sin(2 * np.pi * 82.41 * t) * 0.026) * lfo
    droneR = (np.sin(2 * np.pi * 55.22 * t) * 0.050 +
              np.sin(2 * np.pi * 55.55 * t) * 0.038 +
              np.sin(2 * np.pi * 82.41 * t) * 0.026) * (1.5 - lfo)

    # air: heavily low-passed noise, very quiet, slow swell
    noise = rng.standard_normal(n + SR)
    kern = 220
    air = np.convolve(noise, np.ones(kern) / kern, mode="same")[SR // 2: SR // 2 + n]
    air_lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.021 * t + 0.7)
    airL = air * 0.05 * (0.4 + 0.6 * air_lfo)
    airR = np.roll(air, 900) * 0.05 * (0.4 + 0.6 * (1 - air_lfo))

    mixL = droneL + airL
    mixR = droneR + airR

    # heartbeat pulse every 4.8s
    hb = thump(70, 48, 0.5, 0.16)
    for k in np.arange(2.4, total, 4.8):
        i = int(k * SR)
        seg = min(len(hb), n - i)
        if seg > 0:
            mixL[i:i + seg] += hb[:seg] * 0.55
            mixR[i:i + seg] += hb[:seg] * 0.45

    # synced cues
    stamp = thump(150, 50, 0.5, 0.62)
    tk = tick()
    for ct, kind in cues:
        i = int(ct * SR)
        if i >= n: continue
        if kind == "stamp":
            seg = min(len(stamp), n - i)
            mixL[i:i + seg] += stamp[:seg]
            mixR[i:i + seg] += stamp[:seg] * 0.9
        else:
            seg = min(len(tk), n - i)
            mixL[i:i + seg] += tk[:seg]
            mixR[i:i + seg] += tk[:seg] * 0.8

    # hook section (first 14s) gets a touch more energy
    boost = np.clip((14.0 - t) / 14.0, 0, 1) * 0.15
    mixL *= (1 + boost); mixR *= (1 + boost)

    # soft clip + RMS normalize to -23 dBFS
    mixL = np.tanh(mixL * 1.4); mixR = np.tanh(mixR * 1.4)
    rms = math.sqrt(0.5 * np.mean(mixL ** 2) + 0.5 * np.mean(mixR ** 2)) or 1e-9
    g = 10 ** (-23 / 20) / rms
    mixL *= g; mixR *= g
    peak = max(np.abs(mixL).max(), np.abs(mixR).max())
    if peak > 0.92:
        mixL *= 0.92 / peak; mixR *= 0.92 / peak

    st = np.stack([mixL, mixR], axis=1)
    pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    import wave
    outp = os.path.join(REPO, "output/audio/music.wav")
    with wave.open(outp, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"music.wav: {total:.1f}s, cues: {len(cues)} ({sum(1 for c in cues if c[1]=='stamp')} stamps)")

if __name__ == "__main__":
    main()
