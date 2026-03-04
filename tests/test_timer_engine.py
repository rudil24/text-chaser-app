"""
Tests for src/core/timer_engine.py — TimerEngine

A QApplication must exist before any QObject/QTimer is instantiated.
pytest-qt provides the `qapp` fixture for this. We also define a module-level
fallback so the import itself doesn't fail if pytest-qt is unavailable.
"""
from __future__ import annotations

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def engine(qapp):
    """Return a fresh, started TimerEngine for each test."""
    from core.timer_engine import TimerEngine

    eng = TimerEngine()
    eng.start()
    return eng


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_delete_limit_constant_is_10():
    """_DELETE_LIMIT must be exactly 10 — the burn threshold."""
    from core.timer_engine import _DELETE_LIMIT

    assert _DELETE_LIMIT == 10


# ---------------------------------------------------------------------------
# Delete counter behaviour
# ---------------------------------------------------------------------------


def test_backspace_increments_counter(engine):
    """Nine consecutive backspaces should all return 'valid' and increment the
    counter on each stroke."""
    for i in range(1, 10):
        result = engine.on_keystroke(Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier)
        assert result == ("valid", None), f"Expected valid on stroke {i}, got {result}"
        assert engine.consecutive_delete_count == i, (
            f"Counter should be {i} after {i} backspaces, got {engine.consecutive_delete_count}"
        )


def test_valid_char_resets_delete_counter(engine):
    """After 5 backspaces the counter is 5; a regular char key must reset it to 0."""
    for _ in range(5):
        engine.on_keystroke(Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier)

    assert engine.consecutive_delete_count == 5

    result = engine.on_keystroke(Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier)
    assert result == ("valid", None)
    assert engine.consecutive_delete_count == 0, (
        f"Counter should reset to 0 after a char key, got {engine.consecutive_delete_count}"
    )


def test_10th_backspace_triggers_burn(engine):
    """Strokes 1-9 are valid; stroke 10 must return ('burn', 'delete_limit')."""
    for i in range(9):
        result = engine.on_keystroke(Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier)
        assert result == ("valid", None), f"Stroke {i + 1} should be valid, got {result}"

    tenth = engine.on_keystroke(Qt.Key.Key_Backspace, Qt.KeyboardModifier.NoModifier)
    assert tenth == ("burn", "delete_limit"), (
        f"10th backspace should return ('burn', 'delete_limit'), got {tenth}"
    )


# ---------------------------------------------------------------------------
# Paste detection
# ---------------------------------------------------------------------------


def test_paste_is_invalid(engine):
    """Ctrl+V (ControlModifier) and Cmd+V (MetaModifier) must both be rejected."""
    ctrl_paste = engine.on_keystroke(
        Qt.Key.Key_V, Qt.KeyboardModifier.ControlModifier
    )
    assert ctrl_paste == ("invalid", None), f"Ctrl+V should be invalid, got {ctrl_paste}"

    # Re-enable engine for the second check (burn/inactive state won't block — engine is still active)
    meta_paste = engine.on_keystroke(
        Qt.Key.Key_V, Qt.KeyboardModifier.MetaModifier
    )
    assert meta_paste == ("invalid", None), f"Cmd+V should be invalid, got {meta_paste}"


# ---------------------------------------------------------------------------
# Navigation keys
# ---------------------------------------------------------------------------


def test_arrow_keys_are_invalid(engine):
    """Arrow keys must return ('invalid', None) — they are navigation-only."""
    arrow_keys = [
        Qt.Key.Key_Left,
        Qt.Key.Key_Right,
        Qt.Key.Key_Up,
        Qt.Key.Key_Down,
    ]
    for key in arrow_keys:
        result = engine.on_keystroke(key, Qt.KeyboardModifier.NoModifier)
        assert result == ("invalid", None), f"Arrow key {key} should be invalid, got {result}"


# ---------------------------------------------------------------------------
# Modifier-only keys
# ---------------------------------------------------------------------------


def test_modifier_only_invalid(engine):
    """Standalone modifier keys (Shift, Control) must return ('invalid', None)."""
    modifier_keys = [
        Qt.Key.Key_Shift,
        Qt.Key.Key_Control,
    ]
    for key in modifier_keys:
        result = engine.on_keystroke(key, Qt.KeyboardModifier.NoModifier)
        assert result == ("invalid", None), f"Modifier key {key} should be invalid, got {result}"


# ---------------------------------------------------------------------------
# Valid typing keys
# ---------------------------------------------------------------------------


def test_char_key_is_valid(engine):
    """Ordinary character keys must return ('valid', None) and not burn."""
    char_keys = [
        Qt.Key.Key_A,
        Qt.Key.Key_Space,
        Qt.Key.Key_Return,
    ]
    for key in char_keys:
        result = engine.on_keystroke(key, Qt.KeyboardModifier.NoModifier)
        assert result == ("valid", None), f"Char key {key} should be valid, got {result}"
