from __future__ import annotations

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


class RangeSlider(QWidget):
    rangeChanged = Signal(int, int)

    def __init__(self, minimum: int = -1200, maximum: int = 3000, parent=None) -> None:
        super().__init__(parent)
        self._minimum = minimum
        self._maximum = maximum
        self._lower = -160
        self._upper = 240
        self._active_handle: str | None = None
        self.setMinimumHeight(36)
        self.setMouseTracking(True)

    def values(self) -> tuple[int, int]:
        return self._lower, self._upper

    def setValues(self, lower: int, upper: int) -> None:
        lower = max(self._minimum, min(lower, self._maximum))
        upper = max(self._minimum, min(upper, self._maximum))
        if lower > upper:
            lower, upper = upper, lower
        if (lower, upper) == (self._lower, self._upper):
            return
        self._lower = lower
        self._upper = upper
        self.rangeChanged.emit(self._lower, self._upper)
        self.update()

    def paintEvent(self, event) -> None:
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track = self._track_rect()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#d7dbe2"))
        painter.drawRoundedRect(track, 3, 3)

        low_x = self._x_for_value(self._lower)
        high_x = self._x_for_value(self._upper)
        selected = QRectF(low_x, track.y(), high_x - low_x, track.height())
        painter.setBrush(QColor("#2f6fed"))
        painter.drawRoundedRect(selected, 3, 3)

        for x, color in ((low_x, "#ffffff"), (high_x, "#ffffff")):
            painter.setBrush(QColor(color))
            painter.setPen(QPen(QColor("#1f2937"), 1))
            painter.drawEllipse(QRectF(x - 8, track.center().y() - 8, 16, 16))

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        x = event.position().x()
        low_distance = abs(x - self._x_for_value(self._lower))
        high_distance = abs(x - self._x_for_value(self._upper))
        self._active_handle = "lower" if low_distance <= high_distance else "upper"
        self._move_handle(x)

    def mouseMoveEvent(self, event) -> None:
        if self._active_handle:
            self._move_handle(event.position().x())

    def mouseReleaseEvent(self, event) -> None:
        del event
        self._active_handle = None

    def _move_handle(self, x: float) -> None:
        value = self._value_for_x(x)
        if self._active_handle == "lower":
            self.setValues(min(value, self._upper), self._upper)
        elif self._active_handle == "upper":
            self.setValues(self._lower, max(value, self._lower))

    def _track_rect(self) -> QRectF:
        margin = 14
        return QRectF(margin, self.height() / 2 - 3, self.width() - margin * 2, 6)

    def _x_for_value(self, value: int) -> float:
        track = self._track_rect()
        ratio = (value - self._minimum) / (self._maximum - self._minimum)
        return track.left() + ratio * track.width()

    def _value_for_x(self, x: float) -> int:
        track = self._track_rect()
        ratio = (x - track.left()) / max(1.0, track.width())
        ratio = max(0.0, min(1.0, ratio))
        return round(self._minimum + ratio * (self._maximum - self._minimum))
