# PRD: Text Chaser App

__Version:__ 0.3
__Author:__ Cap (OPST Team Lead)
__Date:__ 2026-03-03
__Status:__ Design Locked — Ready for Build

---

## 1. Product Overview

__PYRE__ is a pressure-driven desktop writing app. If you stop typing, you lose everything. The mechanic is the feature — it eliminates writer's block by making inaction catastrophic. Inspired by "The Most Dangerous Writing App."

---

## 2. Core Mechanic

- User opens the app and begins typing in a full-screen text editor.
- A visible countdown timer resets to __5 seconds__ every time a valid keystroke is detected.
- If the timer reaches zero (no valid keystroke for 5 seconds), __all text is permanently deleted__.
- Backspace/Delete counts as a valid keystroke — but only up to 9 consecutive presses. The 10th consecutive backspace/delete without an intervening character key triggers immediate burn, regardless of the timer state. You cannot erase your way to safety.
- Paste from clipboard does __not__ reset the timer and does not count as a valid keystroke. Pasting is cheating.
- No undo. No recovery. Gone.

---

## 3. User Stories

- As a writer, I want a blank, distraction-free canvas so I can focus on output.
- As a writer, I want a clear visual signal that the clock is ticking so I know when I'm in danger.
- As a writer, I want my text to vanish instantly if I stop so the mechanic has real stakes.
- As a writer, I want to be able to see my word count in real time so I feel a sense of progress.

---

## 4. Functional Requirements

### 4.1 Editor

- Full-screen text input area (no scroll bars visible by default).
- Real-time word count display (unobtrusive).
- No menu bar, no toolbar, no distractions.

### 4.2 Countdown Timer

- Default timeout: __5 seconds__.
- Timer resets on every valid keystroke.
- Visual urgency escalation: UI changes (color, pulse, glow) as time runs low.
- At zero: instant, irreversible text wipe. No confirmation dialog.

### 4.3 Auto-Save

- PYRE continuously auto-saves the editor contents to a draft file: `draft_<session-timestamp>.txt`
- Default save location: `~/Documents/pyre/` (created on first launch if it doesn't exist)
- Save location is configurable via settings (see 4.5).
- Auto-save fires on a debounced interval — every 10 seconds of active writing, or immediately on any burn event.
- On burn: the last saved draft remains on disk. The burn overlay displays the save path so the user can retrieve it.
- On clean exit (user closes window): final save fires, session is marked `[completed]` in the filename.
- File naming: `draft_<YYYY-MM-DD_HH-MM-SS>.txt` for burn sessions, `session_<YYYY-MM-DD_HH-MM-SS>.txt` for clean exits.

### 4.4 Start Screen

- Minimal launch screen with app name/brand and a single "Begin" button.
- Brief one-line description of the mechanic visible on start.

### 4.5 Settings

- Accessible from the start screen only (not during a session).
- Single configurable option for v1: __Save Folder__ — file picker to set auto-save destination.
- Settings persisted to a local config file (`~/.pyre/config.json`).

---

## 5. Platform & Tech Stack

- __Platform:__ macOS desktop (primary), Windows compatible as bonus.
- __Language:__ Python 3.x
- __GUI Library:__ `PyQt6` — selected for custom painter control (SVG ring timer, fire gradients, full window chrome override). CustomTkinter lacks the painting API depth PYRE's design requires.
- __Distribution:__ Single runnable script for now; `pyinstaller` bundle as a stretch goal.

---

## 6. Design Direction — PYRE (Locked)

- __App Name:__ PYRE
- __Tagline:__ "Every word keeps the fire alive. Stop typing and it all burns down."
- __Reference:__ `design-mockup-2-ember.html`
- __Palette:__ Coal Void `#0A0705`, Charcoal Deep `#1A1410`, Ember Glow `#FF6B1A`, Ember Hot `#FF4500`, Ember Core `#FF2000`, Blood Red `#8B1500`, Heat Yellow `#FFA500`, Text Primary `#F0E0C8`
- __Typography:__ Anton (display/wordmark), Bebas Neue (UI buttons), Inter (editor body), JetBrains Mono (timer/mono UI)
- __Timer:__ SVG ring drain with ember gradient stroke and fire-glow drop shadow
- __Deletion:__ Screen immolates — orange border pulse, scanline flicker, "BURNED." headline, stats overlay

---

## 7. Out of Scope (v1)

- Cloud sync or account system.
- Configurable timer (hard-coded at 5s for MVP).
- Multi-session history.
- Mobile or web versions.

---

## 8. Success Criteria

- App launches cleanly on macOS.
- Typing resets the timer reliably with no lag.
- Deletion at zero is instantaneous.
- The visual design creates genuine tension and urgency.
- A writer can sit down and use it with zero instruction.
