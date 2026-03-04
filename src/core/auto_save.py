from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, QTimer

from core.config import get_save_folder


class AutoSaveManager(QObject):
    def __init__(self, session_start: datetime, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._session_start = session_start
        timestamp = session_start.strftime("%Y-%m-%d_%H-%M-%S")
        save_folder = Path(get_save_folder())
        self._draft_path: Path = save_folder / f"draft_{timestamp}.txt"
        self._finalized = False

        self._auto_save_timer = QTimer(self)
        self._auto_save_timer.setInterval(10_000)
        self._auto_save_timer.timeout.connect(self._on_auto_save_tick)
        self._pending_content: str = ""
        self._auto_save_timer.start()

    def _on_auto_save_tick(self) -> None:
        if self._pending_content is not None:
            self.save(self._pending_content)

    def set_content(self, content: str) -> None:
        self._pending_content = content

    def save(self, content: str) -> None:
        if self._finalized:
            return
        try:
            self._draft_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._draft_path, "w", encoding="utf-8") as fh:
                fh.write(content)
        except Exception:
            pass

    def finalize_clean(self, content: str) -> None:
        if self._finalized:
            return
        self._finalized = True
        self._auto_save_timer.stop()
        self.save(content)
        try:
            timestamp = self._session_start.strftime("%Y-%m-%d_%H-%M-%S")
            session_path = self._draft_path.parent / f"session_{timestamp}.txt"
            if self._draft_path.exists():
                os.rename(self._draft_path, session_path)
        except Exception:
            pass

    def finalize_burn(self, content: str) -> str:
        if self._finalized:
            return str(self._draft_path)
        self._finalized = True
        self._auto_save_timer.stop()
        self.save(content)
        return str(self._draft_path)

    def get_draft_path(self) -> str:
        return str(self._draft_path)
