from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QStackedWidget, QWidget

from screens.burn_screen import BurnScreen
from screens.editor_screen import EditorScreen
from screens.start_screen import StartScreen


_SCREEN_START = 0
_SCREEN_EDITOR = 1
_SCREEN_BURN = 2


class PyreApp(QWidget):
    def __init__(
        self,
        display_font: QFont | None = None,
        button_font: QFont | None = None,
        body_font: QFont | None = None,
        mono_font: QFont | None = None,
    ) -> None:
        super().__init__()
        self._display_font = display_font
        self._button_font = button_font
        self._body_font = body_font
        self._mono_font = mono_font
        self._burn_screen: BurnScreen | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #0A0705;")

        from PyQt6.QtWidgets import QVBoxLayout

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._stack = QStackedWidget(self)

        self._start_screen = StartScreen(
            display_font=self._display_font,
            button_font=self._button_font,
            body_font=self._body_font,
            parent=self._stack,
        )

        self._editor_screen = EditorScreen(
            body_font=self._body_font,
            mono_font=self._mono_font,
            parent=self._stack,
        )

        self._stack.addWidget(self._start_screen)
        self._stack.addWidget(self._editor_screen)
        self._stack.setCurrentIndex(_SCREEN_START)

        layout.addWidget(self._stack)

        self._start_screen.session_started.connect(self._on_session_started)
        self._editor_screen.burn_triggered.connect(self._on_burn_triggered)

    def _on_session_started(self) -> None:
        self._stack.setCurrentIndex(_SCREEN_EDITOR)
        self._editor_screen.start_session()

    def _on_burn_triggered(self, cause: str, word_count: int, duration_seconds: int) -> None:
        self._editor_screen.stop_session()
        draft_path = self._editor_screen.get_draft_path()

        if self._burn_screen is not None:
            self._burn_screen.stop_animation()
            self._stack.removeWidget(self._burn_screen)
            self._burn_screen.deleteLater()
            self._burn_screen = None

        self._burn_screen = BurnScreen(
            cause=cause,
            word_count=word_count,
            duration_seconds=duration_seconds,
            draft_path=draft_path,
            display_font=self._display_font,
            button_font=self._button_font,
            body_font=self._body_font,
            parent=self._stack,
        )
        self._burn_screen.restart.connect(self._on_restart)
        self._burn_screen.quit_app.connect(self._on_quit)

        self._stack.addWidget(self._burn_screen)
        self._stack.setCurrentWidget(self._burn_screen)

    def _on_restart(self) -> None:
        if self._burn_screen:
            self._burn_screen.stop_animation()
        self._stack.setCurrentIndex(_SCREEN_START)

    def _on_quit(self) -> None:
        QApplication.quit()

    def closeEvent(self, event) -> None:  # type: ignore[override]
        current = self._stack.currentWidget()
        if current is self._editor_screen:
            self._editor_screen.stop_session()
            self._editor_screen.finalize_clean_exit()
        if self._burn_screen:
            self._burn_screen.stop_animation()
        event.accept()
