from __future__ import annotations

import os
import sys
from pathlib import Path

from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication

_ASSETS_DIR = Path(__file__).parent.parent / "assets" / "fonts"

_FONT_FILES = {
    "display": ("Anton-Regular.ttf", "serif"),
    "button": ("BebasNeue-Regular.ttf", "sans-serif"),
    "body": ("Inter-Variable.ttf", "sans-serif"),
    "mono": ("JetBrainsMono-Regular.ttf", "monospace"),
}


def _load_fonts() -> dict[str, QFont]:
    fonts: dict[str, QFont] = {}
    for role, (filename, fallback) in _FONT_FILES.items():
        path = _ASSETS_DIR / filename
        family = fallback
        if path.exists():
            font_id = QFontDatabase.addApplicationFont(str(path))
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    family = families[0]
        fonts[role] = QFont(family)
    return fonts


def main() -> None:
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("PYRE")
    app.setOrganizationName("OPST")

    from core.config import get_save_folder
    get_save_folder()

    fonts = _load_fonts()

    from app import PyreApp
    window = PyreApp(
        display_font=fonts.get("display"),
        button_font=fonts.get("button"),
        body_font=fonts.get("body"),
        mono_font=fonts.get("mono"),
    )
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
