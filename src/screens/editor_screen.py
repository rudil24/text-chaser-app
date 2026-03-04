from __future__ import annotations

import time
from datetime import datetime

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QKeyEvent, QTextCursor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.auto_save import AutoSaveManager
from core.timer_engine import TimerEngine
from widgets.ring_timer import RingTimerWidget


class _NopasteTextEdit(QTextEdit):
    def insertFromMimeData(self, source) -> None:  # type: ignore[override]
        pass


class EditorScreen(QWidget):
    burn_triggered = pyqtSignal(str, int, int)

    def __init__(
        self,
        body_font: QFont | None = None,
        mono_font: QFont | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._body_font = body_font
        self._mono_font = mono_font
        self._session_start: datetime | None = None
        self._auto_save: AutoSaveManager | None = None
        self._timer_engine = TimerEngine(self)
        self._blink_state = False
        self._current_remaining: float = 5.0

        self._build_ui()
        self._wire_signals()

    def _build_ui(self) -> None:
        self.setStyleSheet("background-color: #0A0705;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("background-color: #0A0705;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(24, 12, 24, 12)

        self._word_count_label = QLabel("0 words")
        wc_font = QFont(self._mono_font) if self._mono_font else QFont("monospace")
        wc_font.setPointSize(12)
        self._word_count_label.setFont(wc_font)
        self._word_count_label.setStyleSheet("color: #6B5A4E; background: transparent;")

        self._write_now_label = QLabel("WRITE NOW")
        wn_font = QFont(self._body_font) if self._body_font else QFont("sans-serif")
        wn_font.setPointSize(16)
        wn_font.setBold(True)
        self._write_now_label.setFont(wn_font)
        self._write_now_label.setStyleSheet("color: #FF2000; background: transparent; letter-spacing: 4px;")
        self._write_now_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._write_now_label.setVisible(False)

        self._ring = RingTimerWidget(mono_font=self._mono_font, parent=self)

        top_layout.addWidget(self._word_count_label)
        top_layout.addStretch()
        top_layout.addWidget(self._write_now_label)
        top_layout.addStretch()
        top_layout.addWidget(self._ring)

        editor_container = QWidget()
        editor_container.setStyleSheet("background-color: #0A0705;")
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(80, 40, 80, 60)

        self._editor = _NopasteTextEdit()
        editor_font = QFont(self._body_font) if self._body_font else QFont("sans-serif")
        editor_font.setPointSize(16)
        self._editor.setFont(editor_font)
        self._editor.setStyleSheet(
            """
            QTextEdit {
                color: #F0E0C8;
                background-color: #0A0705;
                border: none;
                selection-background-color: rgba(255, 107, 26, 0.3);
            }
            """
        )
        self._editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._editor.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        doc = self._editor.document()
        doc.setDocumentMargin(0)
        block_fmt = self._editor.textCursor().blockFormat()
        block_fmt.setLineHeight(175, 1)
        cursor = self._editor.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setBlockFormat(block_fmt)

        editor_layout.addWidget(self._editor)

        root.addWidget(top_bar)
        root.addWidget(editor_container, stretch=1)

        self._blink_timer = QTimer(self)
        self._blink_timer.setInterval(300)
        self._blink_timer.timeout.connect(self._on_blink_tick)

    def _wire_signals(self) -> None:
        self._timer_engine.tick.connect(self._on_timer_tick)
        self._timer_engine.burn.connect(self._on_burn_signal)
        self._editor.textChanged.connect(self._on_text_changed)
        self._editor.installEventFilter(self)

    def eventFilter(self, watched, event) -> bool:  # type: ignore[override]
        if watched is self._editor and isinstance(event, QKeyEvent):
            return self._handle_key_event(event)
        return super().eventFilter(watched, event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self._handle_key_event(event)

    def _handle_key_event(self, event: QKeyEvent) -> bool:
        key = Qt.Key(event.key())
        modifiers = event.modifiers()

        ctrl_or_meta = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier
        if modifiers & ctrl_or_meta:
            if key == Qt.Key.Key_V:
                return True

        result, cause = self._timer_engine.on_keystroke(key, modifiers)

        if result == "burn":
            return True

        return False

    def _on_text_changed(self) -> None:
        text = self._editor.toPlainText()
        count = len(text.split()) if text.strip() else 0
        self._word_count_label.setText(f"{count} word{'s' if count != 1 else ''}")
        if self._auto_save:
            self._auto_save.set_content(text)

    def _on_timer_tick(self, remaining: float) -> None:
        self._current_remaining = remaining
        self._ring.set_remaining(remaining)
        self._apply_heat_creep(remaining)

        if remaining < 1.0:
            if not self._blink_timer.isActive():
                self._blink_timer.start()
        else:
            if self._blink_timer.isActive():
                self._blink_timer.stop()
            self._write_now_label.setVisible(False)

    def _on_blink_tick(self) -> None:
        self._blink_state = not self._blink_state
        self._write_now_label.setVisible(self._blink_state)

    def _apply_heat_creep(self, remaining: float) -> None:
        if remaining > 3.0:
            self.setStyleSheet("background-color: #0A0705;")
            self._editor.setStyleSheet(
                """
                QTextEdit {
                    color: #F0E0C8;
                    background-color: #0A0705;
                    border: none;
                    selection-background-color: rgba(255, 107, 26, 0.3);
                }
                """
            )
        elif remaining > 1.0:
            t = (3.0 - remaining) / 2.0
            alpha = int(t * 28)
            self.setStyleSheet(f"background-color: #0A0705;")
            self._editor.setStyleSheet(
                f"""
                QTextEdit {{
                    color: #F0E0C8;
                    background-color: rgba(20, 8, 4, 1);
                    border: none;
                    border-left: {int(t * 3)}px solid #FF4500;
                    selection-background-color: rgba(255, 107, 26, 0.3);
                }}
                """
            )
        else:
            t = (1.0 - remaining) / 1.0
            self._editor.setStyleSheet(
                f"""
                QTextEdit {{
                    color: #F0E0C8;
                    background-color: rgba(26, 8, 4, 1);
                    border: none;
                    border-left: {int(3 + t * 4)}px solid #FF2000;
                    border-right: {int(t * 3)}px solid #8B1500;
                    selection-background-color: rgba(255, 107, 26, 0.3);
                }}
                """
            )

    def _on_burn_signal(self, cause: str) -> None:
        content = self._editor.toPlainText()
        word_count = len(content.split()) if content.strip() else 0

        duration_seconds = 0
        if self._session_start:
            duration_seconds = int(time.time() - self._session_start.timestamp())

        if self._auto_save:
            self._auto_save.finalize_burn(content)

        self.burn_triggered.emit(cause, word_count, duration_seconds)

    def start_session(self) -> None:
        self._session_start = datetime.now()
        self._auto_save = AutoSaveManager(session_start=self._session_start, parent=self)
        self._editor.clear()
        self._editor.setFocus()
        self._blink_state = False
        self._write_now_label.setVisible(False)
        self._ring.set_remaining(5.0)
        self._apply_heat_creep(5.0)
        self._timer_engine.start()

    def stop_session(self) -> None:
        self._timer_engine.stop()
        if self._blink_timer.isActive():
            self._blink_timer.stop()
        self._write_now_label.setVisible(False)

    def finalize_clean_exit(self) -> None:
        content = self._editor.toPlainText()
        if self._auto_save and content.strip():
            self._auto_save.finalize_clean(content)

    def get_draft_path(self) -> str:
        if self._auto_save:
            return self._auto_save.get_draft_path()
        return ""

    def get_word_count(self) -> int:
        text = self._editor.toPlainText()
        return len(text.split()) if text.strip() else 0

    def get_session_duration(self) -> int:
        if self._session_start:
            return int(time.time() - self._session_start.timestamp())
        return 0
