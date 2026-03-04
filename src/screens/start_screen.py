from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StartScreen(QWidget):
    session_started = pyqtSignal()

    def __init__(
        self,
        display_font: QFont | None = None,
        button_font: QFont | None = None,
        body_font: QFont | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._display_font = display_font
        self._button_font = button_font
        self._body_font = body_font
        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet("background-color: #0A0705;")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        center_container = QWidget()
        center_layout = QVBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.setSpacing(20)
        center_layout.setContentsMargins(40, 40, 40, 40)

        wordmark = QLabel("PYRE")
        wordmark_font = QFont(self._display_font) if self._display_font else QFont("serif")
        wordmark_font.setPointSize(96)
        wordmark.setFont(wordmark_font)
        wordmark.setStyleSheet("color: #FF6B1A; background: transparent;")
        wordmark.setAlignment(Qt.AlignmentFlag.AlignCenter)

        tagline = QLabel("Every word keeps the fire alive.\nStop typing and it all burns down.")
        tagline_font = QFont(self._body_font) if self._body_font else QFont("sans-serif")
        tagline_font.setPointSize(14)
        tagline.setFont(tagline_font)
        tagline.setStyleSheet("color: #F0E0C8; background: transparent;")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ignite_btn = QPushButton("IGNITE SESSION")
        btn_font = QFont(self._button_font) if self._button_font else QFont("sans-serif")
        btn_font.setPointSize(24)
        ignite_btn.setFont(btn_font)
        ignite_btn.setFixedSize(320, 64)
        ignite_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ignite_btn.setStyleSheet(
            """
            QPushButton {
                color: #F0E0C8;
                background-color: transparent;
                border: 2px solid #FF6B1A;
                letter-spacing: 3px;
            }
            QPushButton:hover {
                color: #FF6B1A;
                border: 2px solid #FF6B1A;
                background-color: rgba(255, 107, 26, 0.08);
            }
            QPushButton:pressed {
                background-color: rgba(255, 107, 26, 0.18);
            }
            """
        )
        ignite_btn.clicked.connect(self.session_started)

        center_layout.addWidget(wordmark)
        center_layout.addWidget(tagline)
        center_layout.addSpacing(24)
        center_layout.addWidget(ignite_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        bottom_bar = QWidget()
        bottom_bar.setFixedHeight(52)
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(16, 8, 16, 8)
        bottom_layout.addStretch()

        gear_btn = QPushButton("⚙")
        gear_btn.setFixedSize(36, 36)
        gear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        gear_btn.setToolTip("Settings")
        gear_btn.setStyleSheet(
            """
            QPushButton {
                color: #6B5A4E;
                background: transparent;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                color: #FF6B1A;
            }
            """
        )
        gear_btn.clicked.connect(self._open_settings)
        bottom_layout.addWidget(gear_btn)

        root_layout.addWidget(center_container, stretch=1)
        root_layout.addWidget(bottom_bar)

    def _open_settings(self) -> None:
        from screens.settings_screen import SettingsScreen

        dialog = SettingsScreen(parent=self)
        dialog.exec()
