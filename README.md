# pluto-never-one-of-us
### Orb Theory Ep002 — "Why Pluto Was Never One Of Us"

A full 16:9 (1920×1080, 24 fps) funny-sarcastic space documentary built on the
**owner-passed proof-factory recipe v1** (`superz1402/proof-factory`):
specimen-plate system, CUT / XRAY / KICKER modes, deterministic motion —
**every frame a pure function of t** (PIL layers → ffmpeg) — Edge TTS
narration, and a synthesized dark-archive music bed.

**Status: rendered & QA'd — `output/ep002-pluto.mp4`** (see
`output/REPORT-ep002-pluto.md` and `output/qa/`).

## Watch it

- `output/ep002-pluto.mp4` — the full episode (~5.6 min, H.264 + AAC).
- `output/qa/final-contact-sheet.jpg` — 14 frames across the film.
- `output/qa/plates-contact-sheet.jpg` — the 7 adopted specimen plates.

## Structure

```
AGENTS.md            operator contract (CEO file) for this episode
script/script.json   single source of truth: 24 scenes, copy, devices
script/script.md     human script + fact cards
assets/              7 generated specimen plates (A–G) + prompts.md (verbatim)
src/                 gen_plates.sh · normalize_plates.py · tts.py ·
                     motion.py (renderer) · music.py (score) · assemble.py
output/audio/        per-scene Edge TTS mp3 + durations.json + music.wav
output/qa/           contact sheets + final-qa.json (ffprobe, freezedetect)
worklogs/            WORKLOG.md brick ledger + run reports
```

## Rebuild

```bash
pip install edge-tts
bash src/gen_plates.sh          # regenerate raw plates (z-ai image)
python3 src/normalize_plates.py # -> proven 3:2 / 1920x1280 / webp q90
python3 src/tts.py              # per-scene narration (durations probed)
python3 src/motion.py proof     # 12s motion proof (optional gate)
python3 src/motion.py frames    # ~8k deterministic frames
python3 src/motion.py encode    # per-scene segments (frame-accurate audio)
python3 src/music.py            # deterministic bed + synced cues
python3 src/assemble.py         # concat + mix + QA gates
```

## The recipe in one paragraph

Aged cream ledger grounds for CUT (examination beats), near-black emerald
archive grounds for XRAY (the "body" beats: orbit, belt, heart), tightening
crop + payoff panel + stamp for KICKER (verdicts). Furniture: header rule,
mode tag, kinetic type slams, label cards, checklist cards, targeting rings,
comet/light pulses, archive light sweep, case-file progress bar, FILED/CLOSED
stamps. Deterministic film grain doubles as the anti-freeze device
(freezedetect-clean without fake zooms). Hard cuts only; fades at head/tail.

## Credits

Recipe + plate vocabulary: proof-factory (owner-passed 2026-10-28).
Owner: Bilal · Operator: Momo · Narration: Edge TTS Andrew (multilingual).
