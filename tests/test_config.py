"""
Tests for src/core/config.py

config.py builds _CONFIG_DIR and _CONFIG_FILE at module-load time using
Path.home(), so we must patch the module-level names directly rather than
patching Path.home itself.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _patch_config_paths(tmp_path: Path):
    """Return a context manager that redirects config I/O to tmp_path."""
    import core.config as cfg_mod

    fake_dir = tmp_path / ".pyre"
    fake_file = fake_dir / "config.json"
    fake_default_save = tmp_path / "Documents" / "pyre"

    return patch.multiple(
        cfg_mod,
        _CONFIG_DIR=fake_dir,
        _CONFIG_FILE=fake_file,
        _DEFAULT_SAVE_FOLDER=fake_default_save,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_load_config_creates_defaults(tmp_path):
    """load_config() with no existing file must return a dict that contains
    the 'save_folder' key and must write the defaults to disk."""
    import core.config as cfg_mod

    with _patch_config_paths(tmp_path):
        # Ensure no pre-existing config file
        assert not cfg_mod._CONFIG_FILE.exists()

        config = cfg_mod.load_config()

    assert isinstance(config, dict), "load_config() should return a dict"
    assert "save_folder" in config, "'save_folder' key must be present in default config"


def test_save_and_reload_config(tmp_path):
    """Values written by save_config() must survive a round-trip through
    load_config()."""
    import core.config as cfg_mod

    original = {
        "save_folder": str(tmp_path / "my_sessions"),
        "theme": "dark",
        "font_size": 18,
    }

    with _patch_config_paths(tmp_path):
        cfg_mod.save_config(original)
        reloaded = cfg_mod.load_config()

    # The core contract: save_folder must round-trip correctly
    assert reloaded["save_folder"] == original["save_folder"], (
        f"save_folder mismatch: expected {original['save_folder']!r}, got {reloaded['save_folder']!r}"
    )
    # Extra keys written directly via save_config should also survive
    assert reloaded.get("theme") == "dark"
    assert reloaded.get("font_size") == 18
