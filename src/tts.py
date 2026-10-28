#!/usr/bin/env python3
"""Ep002 narration: per-scene Edge TTS -> output/audio/sXX.mp3 + durations.json.
Voice per owner order: male, funky/energetic. Primary en-US-AndrewMultilingualNeural
(+8% rate, +2Hz pitch), fallback en-US-GuyNeural. Deterministic: script.json is
the single source of truth; re-running overwrites identical audio."""
import asyncio, json, os, subprocess, sys
import edge_tts

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "script/script.json")
AUD = os.path.join(REPO, "output/audio")
os.makedirs(AUD, exist_ok=True)

cfg = json.load(open(SCRIPT))
voice = cfg["voice"]
scenes = [s for s in cfg["scenes"] if s.get("dialogue")]

async def synth(scene, name, rate, pitch, outp):
    tts = edge_tts.Communicate(scene["dialogue"], name, rate=rate, pitch=pitch)
    await tts.save(outp)

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())

async def main():
    durations = {}
    vname = voice["name"]
    try:
        await synth(scenes[0], vname, voice["rate"], voice["pitch"], os.path.join(AUD, "_probe.mp3"))
    except Exception as e:
        print("primary voice failed:", e)
        vname = voice["fallback"]
        await synth(scenes[0], vname, voice["rate"], voice["pitch"], os.path.join(AUD, "_probe.mp3"))
    print("voice:", vname)
    for s in cfg["scenes"]:
        sid = s["id"]
        if not s.get("dialogue"):
            durations[sid] = cfg["title_scene_seconds"]
            print(f"{sid}: (title card, fixed {cfg['title_scene_seconds']}s)")
            continue
        outp = os.path.join(AUD, f"{sid}.mp3")
        await synth(s, vname, voice["rate"], voice["pitch"], outp)
        d = probe(outp)
        durations[sid] = d
        print(f"{sid}: {d:.2f}s  | {s['dialogue'][:58]}...")
    json.dump({"voice": vname, "durations": durations},
              open(os.path.join(AUD, "durations.json"), "w"), indent=1)
    total = sum(durations.values())
    print(f"TOTAL NARRATION SPAN: {total:.1f}s  ({total/60:.1f} min)")

if __name__ == "__main__":
    asyncio.run(main())
