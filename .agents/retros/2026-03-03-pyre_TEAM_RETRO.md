# Team Retro: PYRE

__Date:__ 2026-03-03
__Project:__ PYRE (text-chaser-app)
__Team:__ Cap, Stella, Vera

---

## 1. What went well

__Cap (Team Lead):__

- The review-driven flow held up perfectly. PRD → design gate → TASK_LIST approval → build was clean and produced zero scope creep. Product Owner never had to course-correct a wrong assumption.
- Spinning up 3 design mockups in parallel was the right call. Rudi could compare them side by side at pixel fidelity rather than imagining abstract descriptions. Decision was immediate and confident.
- PyQt6 choice was correct. The custom `QPainter` ring timer and the `QGraphicsDropShadowEffect` urgency glow would have been impossible with CustomTkinter.
- Splitting core logic into `TimerEngine`, `AutoSaveManager`, and `config.py` made unit testing surgical — Vera could test each module in isolation with no GUI required.

__Stella (Python Developer / Creative Director):__

- Playing the dual role of Creative Director and Developer was efficient. Same agent who designed the PYRE brand also implemented it — zero translation loss between design intent and code.
- The HTML mockup format (standalone browser files) was the right tool for "pixel ready" presentations. The PO saw the real thing, not a sketch. The fire gradient animations, SVG ring timer, and deletion events were all faithful to the final product.
- `_NopasteTextEdit` subclassing `QTextEdit` to override `insertFromMimeData` was a clean, idiomatic Qt solution for blocking paste — zero hacks.
- The `_finalized` flag pattern in `AutoSaveManager` was the right design — it just had a subtle bug in the call order.

__Vera (QA Engineer):__

- Writing tests before running them caught the `auto_save.py` bug that wouldn't have surfaced until a user's session data was lost silently. The `_finalized` self-block would have been hard to spot in manual testing.
- The `_make_manager` helper pattern (mock `get_save_folder` at construction time) was the right isolation strategy for testing file I/O without touching the real filesystem.
- 14 tests in 0.15s — fast enough to run on every commit without friction.

---

## 2. What went wrong

__Cap (Team Lead):__

- `LOCAL_LOG.md` was not updated after the build phase — only Stage 1 was logged. The build phase, bug fix cycle, and QA stage were never captured. This violates GLOBAL_EVOLUTION.md §6 (mandatory continuous logging).
- The TASK_LIST checkboxes were never ticked off as tasks completed. The list was used for planning only, not as a live tracker.

__Stella (Python Developer / Creative Director):__

- The `finalize_burn` / `finalize_clean` self-block bug (`_finalized = True` set before calling `save()`, which guards on that flag) was a classic execution-order mistake. A single unit test in the same session would have caught it before it shipped. Tests should be written alongside code, not after.
- The `keyPressEvent` override on `EditorScreen` was redundant and actively harmful — the `eventFilter` on the child widget already handled the interception. The duplicate handler was never needed and caused the double-count bug. This was an over-engineering mistake.
- The `eventFilter` not checking `event.type() == QEvent.Type.KeyPress` (accepting both press and release) was a subtle Qt event model misunderstanding. Qt event filters receive ALL event types — always filter by type explicitly.

__Vera (QA Engineer):__

- Bash permissions blocked test execution in the subagent — Vera had to hand the run back to Cap. The test suite was written but not run in the same agent, which broke the feedback loop. Vera needs Bash access to be useful as QA.

---

## 3. What did we discover

__Cap (Team Lead):__

- The "Creative Director" role expansion for Stella is repeatable and high-value. For any project with a visual component, having the dev agent produce pixel-ready mockups before a line of code is written creates a concrete approval gate that prevents rework. This should be a standard step in the software kickoff workflow.
- The HTML mockup format (self-contained, browser-renderable, with real CSS animations) is the correct tool for desktop app UI design in this environment. It bridges the gap between Figma-quality mockups and what can be generated in-session without external tools.

__Stella (Python Developer / Creative Director):__

- Qt event filters receive every event type by default. When using `installEventFilter` for keyboard interception, always add an explicit `event.type() == QEvent.Type.KeyPress` guard or you will process key release, key repeat, and other events you didn't intend to handle.
- The `_finalized` guard pattern (preventing double-writes in a state machine) is sound architecture — but the guard must not block the finalizer's own write. The fix is a private `_write()` method that bypasses the guard, called directly by the finalizers, while the public `save()` method (called by periodic timers) remains guarded.

__Vera (QA Engineer):__

- Testing `AutoSaveManager` without touching the real filesystem requires patching `get_save_folder` at construction time, not at call time, because the path is resolved in `__init__`. The patch must be active when the object is instantiated.
- Separating file-write logic from finalization state logic (`_write()` vs `save()`) made the unit tests significantly cleaner — tests could call `_write()` directly to pre-populate the draft file before testing rename behavior.

---

## Product Owner Section

_Rudi — please add your notes below. What did you think went well? Anything frustrating? Anything you'd want us to do differently next time?_

### What went well (PO)

* Stella rocked it with the three mockups, this is the level of detail / branding / and CHOICE i've been craving on past projects. Was also pretty cool that she could just show me in a browser rather than through figma. i'm sure we'll eventually see a need for figma but not yet!

### What went wrong (PO)

* would like to see more block-level commenting in the source, i have somewhere (maybe it's just in the readme template?) that i always want documented code that a newby can follow.
* i'm stil not getting the "glass" noise to prompt me when you need me. might be a vs code restart issue, i'll try that.

### What did we discover (PO)
* mockups in html worked really well, i was skeptical. will be cool to see if that translates to "hairier" projects.
* this team is really coming together in its abilities to run end-to-end software projects. great job!