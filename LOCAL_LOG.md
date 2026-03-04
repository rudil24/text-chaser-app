# LOCAL_LOG: PYRE

__Project:__ PYRE (text-chaser-app)
__Team Lead:__ Cap
__Started:__ 2026-03-03

---

## Stage 1 — Scope & Design

### 2026-03-03

- Project directory initialized: `text-chaser-app/`
- `owner.txt` reviewed — concept confirmed: pressure-driven writing app, 5s deletion timer
- `PRD.md` drafted (v0.1) by Cap covering core mechanic, functional requirements, platform, and success criteria
- Stella (Creative Director) presented 3 pixel-ready design directions:
  - Mockup 1: DEADTYPE — Noir/Terminal
  - Mockup 2: PYRE — Ember/Fire
  - Mockup 3: STILL — Stark Minimalist
- __Product Owner selected: PYRE (Mockup 2)__
- `PRD.md` updated to v0.2 — design locked, GUI library decision made: PyQt6
- `TASK_LIST.md` pending Product Owner review before build begins

---

## Stage 2 — Build (Phases 1–5)

Date: 2026-03-03

- Phase 1: git init, `.gitignore`, `requirements.txt`, `README.md`, `LICENSE.md`, directory structure, font download script
- Phase 2–5: Stella (Python Developer) implemented all 10 source files:
  - `src/main.py`, `src/app.py`
  - `src/core/config.py`, `src/core/timer_engine.py`, `src/core/auto_save.py`
  - `src/widgets/ring_timer.py`
  - `src/screens/start_screen.py`, `src/screens/editor_screen.py`, `src/screens/burn_screen.py`, `src/screens/settings_screen.py`
- Fonts downloaded (Anton, Bebas Neue, Inter, JetBrains Mono) into `assets/fonts/`
- PyQt6 6.10.2 installed in `.venv`
- Initial commit pushed to [github.com/rudil24/text-chaser-app](https://github.com/rudil24/text-chaser-app)

---

## Stage 3 — QA & Bug Fix

Date: 2026-03-03

- Manual testing by Product Owner revealed 2 bugs:
  - Backspace burning at ~3 presses instead of 10
  - App launching fullscreen instead of 800×600
- Cap diagnosed root causes:
  - `eventFilter` firing on both `KeyPress` and `KeyRelease` (doubled counter per press)
  - Redundant `keyPressEvent` handler on parent widget
  - `showFullScreen()` in `main.py`
- Third bug found by Vera's unit tests: `finalize_burn`/`finalize_clean` never wrote files (self-blocked by `_finalized` flag set before calling `save()`)
- All 3 bugs fixed. 14 unit tests written (Vera), all passing in 0.15s
- Fix commit pushed: `48bcac2`

---

## Stage 4 — Retro

Date: 2026-03-03

- Retro executed. Team contributed (Cap, Stella, Vera). PO reviewed and added feedback.
- 8 learnings extracted → `.agents/learnings/2026-03-03-pyre.md`
- Retro summary → `.agents/retros/2026-03-03-pyre.md`
- Team retro document → `.agents/retros/2026-03-03-pyre_TEAM_RETRO.md`
- __Project status: COMPLETE__
