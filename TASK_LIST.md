# TASK_LIST: PYRE

__Status:__ Complete
__Last Updated:__ 2026-03-03

---

## Phase 1 — Project Setup

- [x] `T01` Initialize git repo + `.gitignore` (Python, pyinstaller, venv)
- [x] `T02` Create `requirements.txt` (PyQt6, any font-loading deps)
- [x] `T03` Create `README.md`
- [x] `T04` Create `LICENSE.md` (ISC)
- [x] `T05` Set up project file structure (`src/`, `assets/fonts/`)
- [x] `T06` Download and bundle Anton + Bebas Neue + JetBrains Mono fonts as local assets

---

## Phase 2 — Core App Shell (Stella)

- [x] `T07` Bootstrap PyQt6 app — frameless window, fullscreen, dark background (`#0A0705`)
- [x] `T08` Implement start screen — PYRE wordmark (Anton 128px, fire gradient), tagline, "IGNITE SESSION" button
- [x] `T09` Implement screen transition (start → editor) on button press

---

## Phase 3 — Editor & Timer Engine (Stella)

- [x] `T10` Implement full-screen text editor widget — Inter 16px, `#F0E0C8` on `#0A0705`, no scrollbar
- [x] `T11` Wire keystroke detection → timer reset (QTimer, 5000ms)
  - Valid: any character key, backspace/delete (up to 9 consecutive)
  - Invalid (no reset): paste (Ctrl/Cmd+V), arrow keys, modifier-only keys
- [x] `T11a` Implement consecutive backspace/delete counter — burn immediately on 10th consecutive press without an intervening character key
- [x] `T12` Implement real-time word count display (unobtrusive, bottom bar)
- [x] `T13` Implement SVG ring timer widget (QPainter, ember gradient stroke, fire-glow shadow)
- [x] `T14` Implement timer drain animation (5s → 0, smooth arc update on QTimer tick)

---

## Phase 4 — Urgency Escalation & Deletion (Stella)

- [x] `T15` Implement heat-creep urgency state: at <3s remaining, ember glow bleeds into editor background
- [x] `T16` Implement "WRITE NOW" warning label blink at <2s
- [x] `T17` Implement deletion event at zero:
  - Instant text wipe
  - Window border shifts to ember-orange pulse
  - "BURNED." overlay with session stats (words lost, duration)
  - "Begin Again" / "Quit" buttons

---

## Phase 5 — Auto-Save & Settings

- [x] `T18` Implement auto-save engine — debounced write every 10s to `~/Documents/pyre/draft_<YYYY-MM-DD_HH-MM-SS>.txt`
- [x] `T19` Create `~/Documents/pyre/` on first launch if it doesn't exist; read save path from `~/.pyre/config.json`
- [x] `T20` On burn: fire immediate save of last content, display save path in burn overlay
- [x] `T21` On clean exit: fire final save, rename file to `session_<timestamp>.txt`
- [x] `T22` Implement settings screen (start screen only) — folder picker, save to `~/.pyre/config.json`

---

## Phase 6 — Polish & QA (Cap + Stella)

- [x] `T23` Match PYRE color palette precisely against `design-mockup-2-ember.html`
- [x] `T24` Test keystroke edge cases: paste no-resets, arrow keys no-reset, backspace counter resets on char key
- [x] `T25` Test backspace burn: confirm 10th consecutive backspace triggers immediate burn
- [x] `T26` Test auto-save: confirm file written to correct folder, correct naming on burn vs clean exit
- [x] `T27` Test deletion edge case — empty editor does not burn (nothing to lose)
- [x] `T28` macOS launch test — clean open, no console errors
- [x] `T29` Update `LOCAL_LOG.md` with build phase notes

---

## Stretch Goals (Post-v1)

- [ ] `S01` Pyinstaller `.app` bundle for macOS
- [ ] `S02` Ember particle animation on start screen
- [ ] `S03` Configurable timer (3s / 5s / 10s setting)
- [ ] `S04` "Survived" end state if user exits cleanly with >100 words
