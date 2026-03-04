# TASK_LIST: PYRE

__Status:__ Awaiting Product Owner Approval
__Last Updated:__ 2026-03-03

---

## Phase 1 — Project Setup

- [ ] `T01` Initialize git repo + `.gitignore` (Python, pyinstaller, venv)
- [ ] `T02` Create `requirements.txt` (PyQt6, any font-loading deps)
- [ ] `T03` Create `README.md`
- [ ] `T04` Create `LICENSE.md` (ISC)
- [ ] `T05` Set up project file structure (`src/`, `assets/fonts/`)
- [ ] `T06` Download and bundle Anton + Bebas Neue + JetBrains Mono fonts as local assets

---

## Phase 2 — Core App Shell (Stella)

- [ ] `T07` Bootstrap PyQt6 app — frameless window, fullscreen, dark background (`#0A0705`)
- [ ] `T08` Implement start screen — PYRE wordmark (Anton 128px, fire gradient), tagline, "IGNITE SESSION" button
- [ ] `T09` Implement screen transition (start → editor) on button press

---

## Phase 3 — Editor & Timer Engine (Stella)

- [ ] `T10` Implement full-screen text editor widget — Inter 16px, `#F0E0C8` on `#0A0705`, no scrollbar
- [ ] `T11` Wire keystroke detection → timer reset (QTimer, 5000ms)
  - Valid: any character key, backspace/delete (up to 9 consecutive)
  - Invalid (no reset): paste (Ctrl/Cmd+V), arrow keys, modifier-only keys
- [ ] `T11a` Implement consecutive backspace/delete counter — burn immediately on 10th consecutive press without an intervening character key
- [ ] `T12` Implement real-time word count display (unobtrusive, bottom bar)
- [ ] `T13` Implement SVG ring timer widget (QPainter, ember gradient stroke, fire-glow shadow)
- [ ] `T14` Implement timer drain animation (5s → 0, smooth arc update on QTimer tick)

---

## Phase 4 — Urgency Escalation & Deletion (Stella)

- [ ] `T15` Implement heat-creep urgency state: at <3s remaining, ember glow bleeds into editor background
- [ ] `T16` Implement "WRITE NOW" warning label blink at <2s
- [ ] `T17` Implement deletion event at zero:
  - Instant text wipe
  - Window border shifts to ember-orange pulse
  - "BURNED." overlay with session stats (words lost, duration)
  - "Begin Again" / "Quit" buttons

---

## Phase 5 — Auto-Save & Settings

- [ ] `T18` Implement auto-save engine — debounced write every 10s to `~/Documents/pyre/draft_<YYYY-MM-DD_HH-MM-SS>.txt`
- [ ] `T19` Create `~/Documents/pyre/` on first launch if it doesn't exist; read save path from `~/.pyre/config.json`
- [ ] `T20` On burn: fire immediate save of last content, display save path in burn overlay
- [ ] `T21` On clean exit: fire final save, rename file to `session_<timestamp>.txt`
- [ ] `T22` Implement settings screen (start screen only) — folder picker, save to `~/.pyre/config.json`

---

## Phase 6 — Polish & QA (Cap + Stella)

- [ ] `T23` Match PYRE color palette precisely against `design-mockup-2-ember.html`
- [ ] `T24` Test keystroke edge cases: paste no-resets, arrow keys no-reset, backspace counter resets on char key
- [ ] `T25` Test backspace burn: confirm 10th consecutive backspace triggers immediate burn
- [ ] `T26` Test auto-save: confirm file written to correct folder, correct naming on burn vs clean exit
- [ ] `T27` Test deletion edge case — empty editor does not burn (nothing to lose)
- [ ] `T28` macOS launch test — clean open, no console errors
- [ ] `T29` Update `LOCAL_LOG.md` with build phase notes

---

## Stretch Goals (Post-v1)

- [ ] `S01` Pyinstaller `.app` bundle for macOS
- [ ] `S02` Ember particle animation on start screen
- [ ] `S03` Configurable timer (3s / 5s / 10s setting)
- [ ] `S04` "Survived" end state if user exits cleanly with >100 words
