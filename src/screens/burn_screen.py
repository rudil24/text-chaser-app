from __future__ import annotations

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


_CAUSE_LABELS = {
    "timer": "timer expired",
    "delete_limit": "deleted too much",
}


class _PulseBorderWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._border_alpha: int = 255
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setStyleSheet("background-color: #0A0705;")

    def get_border_alpha(self) -> int:
        return self._border_alpha

    def set_border_alpha(self, value: int) -> None:
        self._border_alpha = value
        self.update()

    border_alpha = pyqtProperty(int, fget=get_border_alpha, fset=set_border_alpha)

    def paintEvent(self, event) -> None:  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(255, 107, 26, self._border_alpha)
        pen = QPen(color)
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
        painter.end()


class BurnScreen(QWidget):
    restart = pyqtSignal()
    quit_app = pyqtSignal()

    def __init__(
        self,
        cause: str,
        word_count: int,
        duration_seconds: int,
        draft_path: str,
        display_font: QFont | None = None,
        button_font: QFont | None = None,
        body_font: QFont | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._cause = cause
        self._word_count = word_count
        self._duration_seconds = duration_seconds
        self._draft_path = draft_path
        self._display_font = display_font
        self._button_font = button_font
        self._body_font = body_font
        self._animation: QPropertyAnimation | None = None
        self._build_ui()
        self._start_animation()

    def _format_duration(self, seconds: int) -> str:
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"

    def _build_ui(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self._border_widget = _PulseBorderWidget(self)
        self._border_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        inner_layout = QVBoxLayout(self._border_widget)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.setContentsMargins(60, 60, 60, 60)
        inner_layout.setSpacing(24)

        burned_label = QLabel("BURNED.")
        display_font = QFont(self._display_font) if self._display_font else QFont("serif")
        display_font.setPointSize(96)
        burned_label.setFont(display_font)
        burned_label.setStyleSheet("color: #FF6B1A; background: transparent;")
        burned_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        cause_text = _CAUSE_LABELS.get(self._cause, self._cause)
        cause_label = QLabel(f"cause of death: {cause_text}")
        cause_font = QFont(self._body_font) if self._body_font else QFont("sans-serif")
        cause_font.setPointSize(14)
        cause_label.setFont(cause_font)
        cause_label.setStyleSheet("color: #8B1500; background: transparent;")
        cause_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stats_text = (
            f"{self._word_count} word{'s' if self._word_count != 1 else ''} lost  |  "
            f"{self._format_duration(self._duration_seconds)} in session"
        )
        stats_label = QLabel(stats_text)
        stats_font = QFont(self._body_font) if self._body_font else QFont("sans-serif")
        stats_font.setPointSize(13)
        stats_label.setFont(stats_font)
        stats_label.setStyleSheet("color: #F0E0C8; background: transparent;")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        path_display = self._draft_path
        if path_display.startswith(str(__import__("pathlib").Path.home())):
            path_display = "~" + path_display[len(str(__import__("pathlib").Path.home())):]
        save_label = QLabel(f"Last draft saved to: {path_display}")
        save_font = QFont(self._body_font) if self._body_font else QFont("sans-serif")
        save_font.setPointSize(11)
        save_label.setFont(save_font)
        save_label.setStyleSheet("color: #6B5A4E; background: transparent;")
        save_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        save_label.setWordWrap(True)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ignite_btn = QPushButton("IGNITE AGAIN")
        btn_font = QFont(self._button_font) if self._button_font else QFont("sans-serif")
        btn_font.setPointSize(20)
        ignite_btn.setFont(btn_font)
        ignite_btn.setFixedSize(240, 56)
        ignite_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ignite_btn.setStyleSheet(
            """
            QPushButton {
                color: #F0E0C8;
                background-color: transparent;
                border: 2px solid #FF6B1A;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                color: #FF6B1A;
                background-color: rgba(255, 107, 26, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(255, 107, 26, 0.2);
            }
            """
        )
        ignite_btn.clicked.connect(self.restart)

        quit_btn = QPushButton("QUIT")
        quit_btn.setFont(btn_font)
        quit_btn.setFixedSize(160, 56)
        quit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        quit_btn.setStyleSheet(
            """
            QPushButton {
                color: #6B5A4E;
                background-color: transparent;
                border: 2px solid #3A2A20;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                color: #F0E0C8;
                border-color: #6B5A4E;
            }
            QPushButton:pressed {
                background-color: rgba(107, 90, 78, 0.15);
            }
            """
        )
        quit_btn.clicked.connect(self.quit_app)

        btn_row.addWidget(ignite_btn)
        btn_row.addWidget(quit_btn)

        inner_layout.addWidget(burned_label)
        inner_layout.addWidget(cause_label)
        inner_layout.addSpacing(8)
        inner_layout.addWidget(stats_label)
        inner_layout.addWidget(save_label)
        inner_layout.addSpacing(24)
        inner_layout.addLayout(btn_row)

        outer_layout.addWidget(self._border_widget)

    def _start_animation(self) -> None:
        self._animation = QPropertyAnimation(self._border_widget, b"border_alpha", self)
        self._animation.setDuration(900)
        self._animation.setStartValue(60)
        self._animation.setEndValue(255)
        self._animation.setEasingCurve(QEasingCurve.Type.SineCurve)
        self._animation.setLoopCount(-1)
        self._animation.start()

    def stop_animation(self) -> None:
        if self._animation:
            self._animation.stop()
