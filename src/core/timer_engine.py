from __future__ import annotations

import time

from PyQt6.QtCore import QObject, Qt, QTimer, pyqtSignal


_BURN_DURATION_MS = 5_000
_TICK_INTERVAL_MS = 50
_DELETE_LIMIT = 10

_DELETE_KEYS = {
    Qt.Key.Key_Backspace,
    Qt.Key.Key_Delete,
}

_MODIFIER_ONLY_KEYS = {
    Qt.Key.Key_Shift,
    Qt.Key.Key_Control,
    Qt.Key.Key_Meta,
    Qt.Key.Key_Alt,
    Qt.Key.Key_AltGr,
    Qt.Key.Key_CapsLock,
    Qt.Key.Key_NumLock,
    Qt.Key.Key_ScrollLock,
    Qt.Key.Key_Super_L,
    Qt.Key.Key_Super_R,
}

_NAVIGATION_KEYS = {
    Qt.Key.Key_Left,
    Qt.Key.Key_Right,
    Qt.Key.Key_Up,
    Qt.Key.Key_Down,
    Qt.Key.Key_Home,
    Qt.Key.Key_End,
    Qt.Key.Key_PageUp,
    Qt.Key.Key_PageDown,
    Qt.Key.Key_Tab,
    Qt.Key.Key_Escape,
    Qt.Key.Key_F1,
    Qt.Key.Key_F2,
    Qt.Key.Key_F3,
    Qt.Key.Key_F4,
    Qt.Key.Key_F5,
    Qt.Key.Key_F6,
    Qt.Key.Key_F7,
    Qt.Key.Key_F8,
    Qt.Key.Key_F9,
    Qt.Key.Key_F10,
    Qt.Key.Key_F11,
    Qt.Key.Key_F12,
    Qt.Key.Key_Insert,
    Qt.Key.Key_Menu,
    Qt.Key.Key_Print,
}


class TimerEngine(QObject):
    tick = pyqtSignal(float)
    burn = pyqtSignal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.consecutive_delete_count: int = 0
        self._active = False
        self._deadline_monotonic: float = 0.0
        self._burned = False

        self._countdown_timer = QTimer(self)
        self._countdown_timer.setSingleShot(True)
        self._countdown_timer.timeout.connect(self._on_timer_expired)

        self._tick_timer = QTimer(self)
        self._tick_timer.setInterval(_TICK_INTERVAL_MS)
        self._tick_timer.timeout.connect(self._on_tick)

    def start(self) -> None:
        self._burned = False
        self._active = True
        self.consecutive_delete_count = 0
        self._reset_countdown()
        self._tick_timer.start()

    def stop(self) -> None:
        self._active = False
        self._countdown_timer.stop()
        self._tick_timer.stop()

    def _reset_countdown(self) -> None:
        self._deadline_monotonic = time.monotonic() + (_BURN_DURATION_MS / 1000.0)
        self._countdown_timer.start(_BURN_DURATION_MS)

    def _remaining_seconds(self) -> float:
        remaining = self._deadline_monotonic - time.monotonic()
        return max(0.0, min(remaining, _BURN_DURATION_MS / 1000.0))

    def _on_tick(self) -> None:
        if not self._active:
            return
        self.tick.emit(self._remaining_seconds())

    def _on_timer_expired(self) -> None:
        if not self._active or self._burned:
            return
        self._burned = True
        self._active = False
        self._tick_timer.stop()
        self.tick.emit(0.0)
        self.burn.emit("timer")

    def on_keystroke(
        self,
        key: Qt.Key,
        modifiers: Qt.KeyboardModifier,
    ) -> tuple[str, str | None]:
        if self._burned or not self._active:
            return ("invalid", None)

        ctrl_or_meta = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier
        if modifiers & ctrl_or_meta:
            if key in (Qt.Key.Key_V,):
                return ("invalid", None)

        if key in _MODIFIER_ONLY_KEYS:
            return ("invalid", None)

        if key in _NAVIGATION_KEYS:
            return ("invalid", None)

        if key in _DELETE_KEYS:
            self.consecutive_delete_count += 1
            if self.consecutive_delete_count >= _DELETE_LIMIT:
                self._burned = True
                self._active = False
                self._countdown_timer.stop()
                self._tick_timer.stop()
                self.tick.emit(0.0)
                self.burn.emit("delete_limit")
                return ("burn", "delete_limit")
            self._reset_countdown()
            return ("valid", None)

        self.consecutive_delete_count = 0
        self._reset_countdown()
        return ("valid", None)
