# REPORT — Ep002 full-episode run (2026-10-28)

Operator: Momo · Order: owner (Discord, 2026-10-28): full video, sarcastic
Pluto documentary, 16:9, Edge TTS male funky voice, per-dialogue scenes,
Fern-grade hooks, new repo, everything pushed.

## Deliverable

- **`output/ep002-pluto.mp4`** — 1920×1080, 24 fps, H.264 + AAC, **5:33**,
  56.9 MB @ 1.37 Mbps.
- `output/ep002-pluto-telegram.mp4` — 720p cut, 19.3 MB (Bot API sendVideo
  caps at 50 MB).
- 24 scenes = 23 narrated + 1 title card; hard cuts; case-file progress
  device opens 0% → CASE CLOSED.

## Pipeline as executed (per contract)

1. Recipe absorbed from `superz1402/proof-factory` (owner-passed v1).
2. Script + fact cards (`script/`), hook lands < 8 s.
3. 7 plates generated as asset tests; 1 rejected on staging (plate B
   attempt 0), regenerated, adopted; prompts verbatim in `assets/prompts.md`.
4. Normalization per proven geometry (96 px side-crop → 3:2 → 1920×1280 →
   WebP q90).
5. Edge TTS per scene — `en-US-AndrewMultilingualNeural` (+8% rate, +2 Hz
   pitch), 311.4 s narration.
6. 12 s motion proof → header-color defect found and fixed.
7. Full deterministic render — rawvideo piped straight into ffmpeg per scene
   (zero intermediate disk frames; ~0.15 s/frame), segments carry their own
   frame-accurate audio.
8. Deterministic music bed (drone + air + heartbeat) with 46 synced cues
   (4 stamp thumps, 42 checklist ticks), RMS −23 dBFS, mixed at 0.45.
9. Assembly + QA gates.

## QA gates

1. **Contact sheets inspected** (plates + proof + final, 14 frames across the
   film + title-card and rules spot-frames): no truncated labels, no
   furniture striking through text, no specimen crowded by type. PASS.
2. **ffprobe**: h264 1920×1080, 23.99 fps avg, 333.1 s, AAC stereo. PASS.
3. **freezedetect n=-50dB:d=2.5**: zero freezes (deterministic grain + sweeps
   + pulses provide full-frame state changes; no fake zooms). PASS.
4. **Audio**: head mean −22.9 dB / max −8.7 dB; mid mean −22.5 dB / max
   −6.6 dB — no clipping, VO dominant, bed subtle.

## Defects found & fixed this run

- Header/mode furniture was colored by MODE (KICKER → cream → invisible on
  paper). Fix: color keyed on plate ground. Verified on re-render.
- `ANCH[s["plate"]]` unconditional access crashed STORY scenes without rings
  (s04). Fix: guarded `.get()` everywhere.
- Disk-bound JPEG frame store (~0.4 MB/s I/O → 1.2 s/frame) replaced with the
  rawvideo pipe (0.15 s/frame). Detached background runs get reaped by this
  environment — switched to foreground chunked renders.
- Segment bitrate capped (crf 23 / maxrate 2.0M) to keep the master under
  GitHub's 100 MB file limit.

## Honest limits

- Voice energy comes from rate/pitch/copy rhythm; the free Edge endpoint has
  no emotion styles. "Funky" is delivered as dry, fast, deadpan.
- The music bed is synthesized (deterministic), not licensed scoring; it is a
  subtle archive hum + heartbeat + synced cue hits, not a soundtrack.
- Plates are generated illustrations (asset tests), not evidence photos;
  plate F reads galactic rather than literal belt — archive-plausible,
  accepted with note.
- DejaVu Sans Bold stands in for the benchmark's condensed grotesque.
- Grain is ±4/255 — subtle; at heavy compression (Telegram cut) it can
  shimmer slightly. The 1080p master is the reference.
- Cue-time formulas are replicated between `motion.py` and `music.py`
  (single source of truth is `script.json` + `durations.json`); a shared
  module is the clean fix if the recipe moves again.
- Aspect ratio is 16:9 as ordered; "same visual rules" interpreted as the
  proof-factory specimen-plate system (owner-passed benchmark).
- Telegram delivery was attempted with the supplied bot token — it returned
  401 Unauthorized (invalid/revoked). Final video is in the repo; a fresh
  token from @BotFather will let the next run push it to chat.

## Token hygiene

- `ansaribilal14` ghp_ token: dead (401), never used, never stored.
- superz1402 PAT: used transiently in shell only; never written to any file,
  commit, or log. Owner should rotate both since they were pasted in chat.
