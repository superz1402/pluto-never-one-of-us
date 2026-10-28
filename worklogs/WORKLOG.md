# WORKLOG — Ep002: Why Pluto Was Never One Of Us
Operator: Momo · Owner: Bilal (order received 2026-10-28, Discord)
Standing rule: every brick logs here; every run writes a report; secrets never
touch any file, commit, or log (tokens live only in the shell session).

---

## 2026-10-28 · 11:0x UTC — brick 1 · recon + repo
- Absorbed the owner-passed recipe from `superz1402/proof-factory` (AGENTS.md,
  README, DECISION references, `proof_motion.py`, `visual-plan.md`,
  `assets/prompts.md`). No deviations from the contract; new devices only from
  proven primitives.
- `ansaribilal14` token DEAD (401 Bad credentials) — not used anywhere.
  Owner should rotate it; it was also pasted in chat, so treat as burned.
- Working token: superz1402 fine-grained PAT (transient shell use only).
- Created repo `superz1402/pluto-never-one-of-us` (public, empty, no auto-init).
- Local git init (branch `main`, identity Momo). `.gitignore`: frames,
  segments, raw plates, pycache, reference copies.

## 2026-10-28 · 11:1x UTC — brick 2 · script + plates
- `script/script.json` + `script/script.md`: 24 scenes (23 VO + 1 title card),
  hook-first cold open, case-file spine (CASE FILE 002 · THE PLUTO HEARING),
  fact cards checked (diameters, 3:2 resonance, IAU 2006 vote, New Horizons,
  Tombaugh ashes; "smaller across" phrasing for the Eris coda — deliberate).
- 7 plates generated as asset tests (z-ai image, 1344×768, prompts verbatim
  in `assets/prompts.md`). Normalized per proven geometry (96px side-crop →
  3:2 → LANCZOS 1920×1280 → WebP q90).
- **Plate QA (operator judgment):** A, C, D, E, F, G = PASS (F noted: reads
  galactic rather than belt — accepted, archive-plausible; heart glyph small
  and subtle). **Plate B attempt 0 REJECTED** (planets crowd the left third —
  violates staging criterion 2); **attempt 1 PASS** (diagonal lineup, quiet
  paper for the stack). Adopted: 7/7.
- Contact sheet: `output/qa/plates-contact-sheet.jpg`.

## 2026-10-28 · 11:2x UTC — brick 3 · narration
- Edge TTS per scene: primary voice `en-US-AndrewMultilingualNeural`
  (+8% rate, +2Hz pitch) — alive, male, dry; fallback GuyNeural not needed.
- 23 VO scenes probed; total narration span 311.4s; title card fixed 3.2s.
  Tail pad 0.9s/scene. Expected film ≈ 5.6 min.
- Audio + `durations.json` at `output/audio/`.

## 2026-10-28 · 11:3x UTC — brick 4 · motion proof
- 12s motion proof (s01 hook / s08 orbit / s16 verdict) rendered + encoded
  (`output/motion-proof-12s.mp4`).
- **Proof findings:** CUT hook stack + label card + progress bar ✓; XRAY
  comet pulse, targeting rings, checklist card, scan band ✓; KICKER payoff
  panel + crop ✓; grain anti-freeze present ✓.
- **Defect found & fixed:** header furniture colored by MODE (KICKER → cream)
  instead of by plate ground → invisible cream-on-paper headers. Fix: `dark`
  keyed on plate ground (`plate not in PAPER_PLATES`). Re-verified s16 t=1.0
  and t=2.0 clean; the earlier "white sliver" suspicion disproven (seek
  artifact in proof extraction, code was correct).
- Frame cost measured 0.08–0.27s/frame → full render ≈ 8.1k frames ≈ 20–25 min.

## 2026-10-28 · 11:4x UTC — brick 5 · full render (running)
- Full frame render launched detached (`src/motion.py frames` → `encode`),
  log at `output/render.log`. No frozen environment trust: everything that
  matters is committed to the repo as it lands.
- `src/music.py` (deterministic score: drone + air + heartbeat + synced stamp
  thumps & checklist ticks; cue times replicate motion formulas — noted in
  report) and `src/assemble.py` (concat → mix → ffprobe/freezedetect/contact
  sheet gates) written and committed while frames render.

## Brick ledger (mirror of AGENTS.md)
- [x] Repo created; recipe absorbed; dead token identified & reported.
- [x] Script + fact cards (24 scenes).
- [x] 7 plates adopted (1 reject → regenerated), prompts logged.
- [x] Edge TTS narration complete.
- [x] 12s motion proof; header-color defect found & fixed.
- [x] Full render launched (detached, logged).
- [ ] Final assemble + QA gates (ffprobe / freezedetect / contact sheet).
- [ ] Run report + honest limits (`output/REPORT-ep002-pluto.md`).
- [ ] Final push + owner delivery (Telegram token currently 401 — see report).

## 2026-10-28 · 12:0x–12:2x UTC — brick 6 · full render + assemble + QA
- Disk-bound frame store killed mid-run (0.4 MB/s I/O); replaced with the
  rawvideo pipe into ffmpeg (0.15 s/frame, zero intermediate frames).
- Defect: STORY crash — unconditional ANCH access; fixed with guarded .get().
- Bitrate cap added (crf 23 / maxrate 2M / audio 160k) to respect GitHub's
  100 MB file limit; detached background runs get reaped here — foreground
  chunked renders used instead (4 chunks, ~20 min total).
- All 24 segments rendered: 53 MB.
- Assembled: concat + music mix (46 synced cues) + QA.
  **QA: ffprobe 1920×1080/23.99fps/5:33 PASS · freezedetect NONE PASS ·
  contact sheets inspected PASS · audio no clipping.**
- Master 56.9 MB; Telegram 720p cut 19.3 MB; title-card + rules spot-frames
  verified (`output/qa/title-check*.jpg`).
- Run report: `output/REPORT-ep002-pluto.md` (incl. honest limits).
- Telegram bot token supplied by owner returns 401 — delivery via repo + chat;
  token flagged for rotation.

## Brick ledger — final state
- [x] Repo created; recipe absorbed; dead token identified & reported.
- [x] Script + fact cards (24 scenes).
- [x] 7 plates adopted (1 reject → regenerated), prompts logged.
- [x] Edge TTS narration complete (Andrew, 311.4 s).
- [x] 12s motion proof; header-color defect found & fixed.
- [x] Full render (streamed, deterministic) + music bed + assembly.
- [x] QA gates all PASS.
- [x] Run report + honest limits written.
- [x] Everything pushed to superz1402/pluto-never-one-of-us.
