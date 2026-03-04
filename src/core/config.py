from __future__ import annotations

import json
import os
from pathlib import Path


_CONFIG_DIR = Path.home() / ".pyre"
_CONFIG_FILE = _CONFIG_DIR / "config.json"
_DEFAULT_SAVE_FOLDER = Path.home() / "Documents" / "pyre"


def _default_config() -> dict:
    return {"save_folder": str(_DEFAULT_SAVE_FOLDER)}


def load_config() -> dict:
    try:
        if _CONFIG_FILE.exists():
            with open(_CONFIG_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if "save_folder" not in data:
                data["save_folder"] = str(_DEFAULT_SAVE_FOLDER)
            return data
    except Exception:
        pass

    config = _default_config()
    save_config(config)
    return config


def save_config(config: dict) -> None:
    try:
        _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(_CONFIG_FILE, "w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=2)
    except Exception:
        pass


def get_save_folder() -> str:
    config = load_config()
    folder = Path(config.get("save_folder", str(_DEFAULT_SAVE_FOLDER)))
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return str(folder)
