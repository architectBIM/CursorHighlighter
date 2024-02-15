import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pyautogui
from pynput import mouse
import threading
import keyboard  # Import the keyboard library

class TransparentCircle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.normal_brush = QtGui.QColor(255, 255, 128, 127)  # Normal state
        self.flicker_brush = QtGui.QColor(255, 0, 0, 127)  # Flicker state
        self.current_brush = self.normal_brush
        self.diameter = 150  # Circle diameter in pixels
        self.flickering = False

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)
        self.show()

    def paintEvent(self, event):
        mouse_x, mouse_y = pyautogui.position()
        qp = QtGui.QPainter(self)
        qp.setBrush(self.current_brush)
        qp.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        qp.drawEllipse(int(mouse_x - self.diameter / 2), int(mouse_y - self.diameter / 2), self.diameter, self.diameter)
        self.update()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.current_brush = self.flicker_brush
            self.flickering = True
        else:
            self.current_brush = self.normal_brush
            self.flickering = False
        self.update()

    def start_listening(self):
        # Mouse click listener
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        # Keyboard shortcut listener
        keyboard.add_hotkey('ctrl+q', self.exit_application)

    def exit_application(self):
        QtWidgets.QApplication.quit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = TransparentCircle()
    ex.start_listening()
    sys.exit(app.exec_())
