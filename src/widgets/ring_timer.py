from __future__ import annotations

import math

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QSizePolicy, QWidget


_SAFE_COLOR = QColor("#FF6B1A")
_WARNING_COLOR = QColor("#FF4500")
_CRITICAL_COLOR = QColor("#FF2000")
_BACKGROUND_COLOR = QColor("#0A0705")
_TEXT_COLOR = QColor("#F0E0C8")

_RING_DIAMETER = 120
_PEN_WIDTH = 12
_FULL_DURATION = 5.0


def _color_for_remaining(seconds: float) -> QColor:
    if seconds > 3.0:
        return _SAFE_COLOR
    if seconds > 1.0:
        return _WARNING_COLOR
    return _CRITICAL_COLOR


def _glow_radius_for_remaining(seconds: float) -> float:
    if seconds > 3.0:
        return 6.0
    if seconds > 1.0:
        t = (3.0 - seconds) / 2.0
        return 6.0 + t * 14.0
    t = (1.0 - seconds) / 1.0
    return 20.0 + t * 20.0


class RingTimerWidget(QWidget):
    def __init__(self, mono_font: QFont | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._remaining: float = _FULL_DURATION
        self._mono_font = mono_font

        self.setFixedSize(_RING_DIAMETER + 40, _RING_DIAMETER + 40)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setOffset(0, 0)
        self._shadow.setBlurRadius(6)
        self._shadow.setColor(_SAFE_COLOR)
        self.setGraphicsEffect(self._shadow)

    def set_remaining(self, seconds: float) -> None:
        self._remaining = max(0.0, min(seconds, _FULL_DURATION))
        color = _color_for_remaining(self._remaining)
        self._shadow.setColor(color)
        self._shadow.setBlurRadius(_glow_radius_for_remaining(self._remaining))
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        margin = (_PEN_WIDTH // 2) + 4
        ring_rect = QRect(
            (w - _RING_DIAMETER) // 2,
            (h - _RING_DIAMETER) // 2,
            _RING_DIAMETER,
            _RING_DIAMETER,
        )

        painter.fillRect(0, 0, w, h, QColor(0, 0, 0, 0))

        track_pen = QPen(QColor("#1A1410"))
        track_pen.setWidth(_PEN_WIDTH)
        track_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(track_pen)
        painter.drawArc(ring_rect, 0, 360 * 16)

        fraction = self._remaining / _FULL_DURATION if _FULL_DURATION > 0 else 0.0
        span_degrees = fraction * 360.0
        span_angle = int(span_degrees * 16)

        if span_angle > 0:
            arc_color = _color_for_remaining(self._remaining)
            arc_pen = QPen(arc_color)
            arc_pen.setWidth(_PEN_WIDTH)
            arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(arc_pen)
            start_angle = 90 * 16
            painter.drawArc(ring_rect, start_angle, -span_angle)

        if self._mono_font is not None:
            label_font = QFont(self._mono_font)
        else:
            label_font = QFont("monospace")
        label_font.setPointSize(14)
        painter.setFont(label_font)
        painter.setPen(_TEXT_COLOR)

        display_text = f"{self._remaining:.1f}"
        painter.drawText(ring_rect, Qt.AlignmentFlag.AlignCenter, display_text)

        painter.end()
