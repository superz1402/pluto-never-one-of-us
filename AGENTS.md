# AGENTS.md — Ep002: Why Pluto Was Never One Of Us (CEO file)

**You are the operator (Momo) of the Ep002 Pluto factory. A fresh agent reading
only this file must be able to rebuild the episode end-to-end without asking
the owner (Bilal) anything. Bilal judges finished finalists only.**

Owner order for this run (2026-10-28, Discord): *"Build me a full video … a
funny sarcastic reality explanation documentary of space and Pluto … 16:9 …
Edge TTS male funky voice … each dialogue having separate scenes … best hooks
… prepare a new repo and work on that … every single file including your
worklogs updated pushed there — never trust your local environment."*

## What this repo is

One full episode built on the **owner-passed proof-factory recipe v1**
(`superz1402/proof-factory`, passed 2026-10-28 — "loving the visuals"):
specimen-plate system, aged paper / dark archive grounds, FIG. numbers, margin
mode labels, halftone-duotone plate art as layered artifacts, kinetic type,
checklist/progress/stamp retention devices, a state-change event at least every
~4 seconds. Deterministic motion: **every frame a pure function of t**, PIL
layers per frame → ffmpeg, 24 fps, 1920×1080.

## The owner contract (never break)

1. **Proof-first, one brick at a time.** Plates → in-frame QA → short motion
   proof → full episode. No skipped stages, no sprawling parallel builds.
2. **Never store or print secrets.** Tokens arrive transiently per task, live
   only in the shell environment, and are never written to any file, commit,
   memory, or report. Ever. (The old `ansaribilal14` token is dead — do not
   reuse; rotate any token pasted into chat.)
3. **Every run writes a report. A run without a report did not happen.**
4. **Killed/rejected — do not revive:** programmatically drawn specimens;
   typography-only scenes; Ken Burns / parallax-over-stills as the dominant
   language ("slideshow"); flat clean-vector diagrams; self-scored quality
   claims as taste.
5. **QA gates before anything reaches the owner:** (1) contact-sheet
   inspection, (2) ffprobe 1920×1080/24 fps sane codec, (3) `freezedetect
   n=-50dB:d=2.5` clean (anti-freeze via full-frame devices — deterministic
   film-grain shimmer — never a fake zoom), (4) honest limits written down.

## Rebuild from scratch

```bash
pip install edge-tts
python3 src/normalize_plates.py     # plates: raw 1344x768 -> 3:2 -> 1920x1280 webp q90
python3 src/tts.py                  # per-scene Edge TTS -> output/audio/ (durations probed)
python3 src/motion.py               # deterministic frames + per-scene segments -> output/
python3 src/music.py                # deterministic ambient bed + stamp thump
python3 src/assemble.py             # final mux + QA (ffprobe, freezedetect, contact sheet)
```

Plates are generated asset tests (prompts + attempt logs verbatim in
`assets/prompts.md`), normalized exactly like the proven factory: symmetric
96 px side-crop of 1344×768 → 3:2 → LANCZOS 1920×1280 → WebP q90.

## Mode grammar for Ep002 (case-file spine)

The episode is staged as **CASE FILE 002 · THE PLUTO HEARING** — the case
progress device opens at 0% in S01 and closes at CASE CLOSED under the final
stamp. Modes are segments, not styles; transitions are hard cuts.

- **CUT** owns the examination beats on paper grounds (hero, lineup,
  observatory, Eris plates). Checklist/scale/ledger furniture rides inside.
- **XRAY** owns the "body" beats — orbit chaos, Kuiper crowd, the heart
  (dark archive plates with pulses, rings, sprocket rail).
- **KICKER** owns payoffs: demotion verdict, final payoff + stamp, used at
  verdict points, tightening crop grammar from the proof.

## Brick ledger (update with every finished brick)

- [x] Repo created; reference recipe absorbed; dead token identified.
- [x] Script + fact cards (`script/script.md`, machine form `script/script.json`).
- [x] 7 plates generated as asset tests, normalized, prompts logged.
- [x] In-frame plate QA (`output/qa/plates-contact-sheet.jpg`).
- [x] Edge TTS narration, per-scene, durations probed (`output/audio/`).
- [x] 12s motion proof on Ep002 plates (`output/motion-proof-12s.mp4`).
- [x] Full episode render + assemble + QA gates (`output/ep002-pluto.mp4`).
- [x] Run report + honest limits (`output/REPORT-ep002-pluto.md`).
- [x] Everything pushed to `superz1402/pluto-never-one-of-us`.

## Honest limits (standing)

- DejaVu Sans Bold stands in for the benchmark's condensed grotesque.
- Plates are generated illustrations (asset tests), never evidence photos.
- The voice is Edge TTS `en-US-AndrewMultilingualNeural` (+8% rate) —
  "funky male" was owner's ask; no emotion-tag control exists on the free
  Edge endpoint, energy comes from rate, pitch, and copy rhythm.
- Ambient bed is synthesized (deterministic), not licensed music.
