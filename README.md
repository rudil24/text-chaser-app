# PYRE

> Every word keeps the fire alive. Stop typing and it all burns down.

PYRE is a pressure-driven desktop writing app. If you stop typing for 5 seconds, everything you've written is gone. No undo. No recovery.

The mechanic is the feature. Writer's block dies when inaction has consequences.

---

## How It Works

- Start a session and begin writing.
- Every keystroke resets a 5-second countdown.
- Let the timer hit zero → your text burns. Instantly. Permanently.
- Backspace counts — but only 9 times in a row. The 10th triggers a burn.
- Pasting from clipboard doesn't count. Write it yourself.

---

## Running PYRE

```bash
# Install dependencies
pip install -r requirements.txt

# Download fonts (first time only)
bash scripts/download_fonts.sh

# Run
python src/main.py
```

---

## Project Files

- [PRD.md](PRD.md) — Product requirements
- [TASK_LIST.md](TASK_LIST.md) — Build task tracker

---

## Tech Stack

- Python 3.x
- PyQt6

## License

ISC — see [LICENSE.md](LICENSE.md)
