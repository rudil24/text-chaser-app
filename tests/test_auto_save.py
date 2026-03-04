"""
Tests for src/core/auto_save.py — AutoSaveManager

AutoSaveManager:
  - Uses QTimer, so it requires a QApplication (provided by the `qapp` fixture
    from pytest-qt).
  - Calls core.config.get_save_folder() in __init__, so we mock that to direct
    all I/O to tmp_path instead of ~/Documents/pyre.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_manager(tmp_path: Path, session_start: datetime, qapp):
    """Instantiate AutoSaveManager with all I/O redirected to tmp_path."""
    save_dir = tmp_path / "sessions"
    save_dir.mkdir(parents=True, exist_ok=True)

    from core.auto_save import AutoSaveManager

    with patch("core.auto_save.get_save_folder", return_value=str(save_dir)):
        mgr = AutoSaveManager(session_start)

    return mgr, save_dir


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_draft_filename_format(tmp_path, qapp):
    """The draft path must follow the pattern draft_YYYY-MM-DD_HH-MM-SS.txt."""
    session_start = datetime(2026, 3, 3, 14, 30, 55)
    mgr, save_dir = _make_manager(tmp_path, session_start, qapp)

    draft_path = Path(mgr.get_draft_path())
    expected_name = "draft_2026-03-03_14-30-55.txt"
    assert draft_path.name == expected_name, (
        f"Expected draft filename {expected_name!r}, got {draft_path.name!r}"
    )
    assert draft_path.parent == save_dir, (
        f"Draft should be inside save_dir {save_dir}, got {draft_path.parent}"
    )


def test_finalize_burn_writes_file(tmp_path, qapp):
    """finalize_burn() must write the given content to the draft file on disk."""
    session_start = datetime(2026, 3, 3, 9, 0, 0)
    mgr, save_dir = _make_manager(tmp_path, session_start, qapp)

    content = "Some burned writing content."
    returned_path = mgr.finalize_burn(content)
    draft_path = Path(returned_path)

    assert draft_path.exists(), f"Draft file should exist after finalize_burn: {draft_path}"
    assert draft_path.read_text(encoding="utf-8") == content, (
        "Draft file content does not match what was passed to finalize_burn()"
    )


def test_finalize_clean_renames_file(tmp_path, qapp):
    """finalize_clean() must rename the draft to session_*.txt and the draft
    must no longer exist afterwards."""
    session_start = datetime(2026, 3, 3, 10, 15, 30)
    mgr, save_dir = _make_manager(tmp_path, session_start, qapp)

    content = "A clean, complete writing session."
    draft_path = Path(mgr.get_draft_path())

    mgr.finalize_clean(content)

    # Draft file should be gone
    assert not draft_path.exists(), (
        f"Draft file should not exist after finalize_clean, but found: {draft_path}"
    )

    # A session_*.txt file should exist in the same directory
    session_files = list(save_dir.glob("session_*.txt"))
    assert len(session_files) == 1, (
        f"Expected exactly one session_*.txt file, found: {session_files}"
    )

    # Its content must match what was passed in
    assert session_files[0].read_text(encoding="utf-8") == content, (
        "session_*.txt content does not match what was passed to finalize_clean()"
    )


def test_double_finalize_is_safe(tmp_path, qapp):
    """Calling finalize_burn then finalize_clean must not raise and must not
    double-write (the _finalized flag should prevent the second operation)."""
    session_start = datetime(2026, 3, 3, 11, 0, 0)
    mgr, save_dir = _make_manager(tmp_path, session_start, qapp)

    burn_content = "Burned content."
    clean_content = "Should not overwrite."

    # First finalize — burn
    mgr.finalize_burn(burn_content)

    # Second finalize — clean: should be a no-op, must not raise
    try:
        mgr.finalize_clean(clean_content)
    except Exception as exc:
        pytest.fail(f"finalize_clean after finalize_burn raised an exception: {exc}")

    # The draft file was written by finalize_burn and should NOT have been
    # renamed (finalize_clean was a no-op due to _finalized=True)
    draft_path = Path(mgr.get_draft_path())
    assert draft_path.exists(), (
        "Draft file should still exist — finalize_clean should have been a no-op"
    )
    assert draft_path.read_text(encoding="utf-8") == burn_content, (
        "Draft file content should be from the first finalize_burn, not overwritten"
    )

    # No session_*.txt should have been created
    session_files = list(save_dir.glob("session_*.txt"))
    assert len(session_files) == 0, (
        f"No session_*.txt should exist when finalize_clean was a no-op, found: {session_files}"
    )
