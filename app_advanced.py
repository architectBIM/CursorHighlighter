import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pyautogui
from pynput import mouse
import threading
import keyboard

class TransparentCircle(QtWidgets.QWidget):
    trigger_animation = QtCore.pyqtSignal()  # Define a custom signal

    def __init__(self):
        super().__init__()
        self.initUI()
        self.opacity = 127  # Starting opacity for the animation
        self.static_diameter = 135  # Diameter for the static cursor highlight
        self.dynamic_diameter = 120  # Starting diameter for the animated effect
        self.growing = False  # Animation state
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.animation_step = 0
        self.trigger_animation.connect(self.start_animation)  # Connect signal to slot

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        mouse_x, mouse_y = pyautogui.position()

        # Always draw a static circle for cursor highlighting
        # qp.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 127), 2, QtCore.Qt.SolidLine))
        qp.setBrush(QtGui.QColor(255, 255, 0, 127))
        qp.setPen(QtCore.Qt.NoPen)
        qp.drawEllipse(QtCore.QPoint(mouse_x, mouse_y), self.static_diameter // 2, self.static_diameter // 2)

        # If an animation is active, draw the animated circle
        if self.growing:
            qp.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, self.opacity), 3, QtCore.Qt.SolidLine))
            qp.setBrush(QtCore.Qt.NoBrush)
            qp.drawEllipse(QtCore.QPoint(mouse_x, mouse_y), self.dynamic_diameter // 2, self.dynamic_diameter // 2)

        self.update()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.trigger_animation.emit()  # Emit signal to start the animation

    def start_animation(self):
        self.growing = True
        self.opacity = 127
        self.dynamic_diameter = 120  # Reset diameter to start size for the animation
        self.animation_step = 0
        self.timer.start(35)  # Start the animation timer

    def animate(self):
        self.animation_step -= 1
        self.dynamic_diameter -= 5  # Increase the diameter for the animation
        self.opacity = max(0, self.opacity - 5)  # Decrease the opacity for the animation
        if self.opacity == 0:
            self.timer.stop()
            self.growing = False

    def start_listening(self):
        def on_click(x, y, button, pressed):
            if pressed:
                self.trigger_animation.emit()  # Use signal to communicate with the main thread

        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()
        keyboard.add_hotkey('ctrl+q', QtWidgets.QApplication.quit)
        keyboard.add_hotkey('esc', QtWidgets.QApplication.quit)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = TransparentCircle()
    ex.start_listening()
    sys.exit(app.exec_())
