from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.config import load_config, save_config


class SettingsScreen(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PYRE — Settings")
        self.setModal(True)
        self.setFixedSize(520, 260)
        self._config = load_config()
        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet(
            """
            QDialog {
                background-color: #1A1410;
                color: #F0E0C8;
            }
            QLabel {
                color: #F0E0C8;
                background: transparent;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        title = QLabel("SETTINGS")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #FF6B1A; background: transparent;")

        folder_label = QLabel("Save Folder")
        folder_label.setStyleSheet("color: #A09080; font-size: 12px; background: transparent;")

        self._folder_display = QLabel(self._config.get("save_folder", ""))
        self._folder_display.setStyleSheet(
            "color: #F0E0C8; background-color: #0A0705; padding: 8px; border: 1px solid #3A2A20;"
        )
        self._folder_display.setWordWrap(True)
        self._folder_display.setMinimumHeight(36)

        change_btn = QPushButton("Change Folder")
        change_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        change_btn.setFixedHeight(36)
        change_btn.setStyleSheet(
            """
            QPushButton {
                color: #F0E0C8;
                background-color: transparent;
                border: 1px solid #FF6B1A;
                padding: 0 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #FF6B1A;
                background-color: rgba(255, 107, 26, 0.08);
            }
            """
        )
        change_btn.clicked.connect(self._on_change_folder)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        back_btn = QPushButton("Close")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setFixedHeight(36)
        back_btn.setStyleSheet(
            """
            QPushButton {
                color: #6B5A4E;
                background-color: transparent;
                border: 1px solid #3A2A20;
                padding: 0 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #F0E0C8;
                border-color: #6B5A4E;
            }
            """
        )
        back_btn.clicked.connect(self.accept)
        btn_row.addWidget(back_btn)

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(folder_label)
        layout.addWidget(self._folder_display)
        layout.addWidget(change_btn)
        layout.addStretch()
        layout.addLayout(btn_row)

    def _on_change_folder(self) -> None:
        current = self._config.get("save_folder", "")
        chosen = QFileDialog.getExistingDirectory(
            self,
            "Select Save Folder",
            current,
            QFileDialog.Option.ShowDirsOnly,
        )
        if chosen:
            self._config["save_folder"] = chosen
            save_config(self._config)
            self._folder_display.setText(chosen)
