from PyQt5 import QtCore, QtWidgets, QtGui
import sys

class QToaster(QtWidgets.QFrame):
    closed = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QToaster, self).__init__(*args, **kwargs)
        QtWidgets.QHBoxLayout(self)

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        self.setStyleSheet('''
            QToaster {
                border: 1px solid black;
                border-radius: 0px;
                color: rgb(255, 255, 255);
                background-color: rgb(57, 66, 81);
            }
        ''')

        # alternatively:
        # self.setAutoFillBackground(True)
        # self.setFrameShape(self.Box)

        self.timer = QtCore.QTimer(singleShot = True, timeout = self.hide)

        if self.parent():
            self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(opacity = 0)
            self.setGraphicsEffect(self.opacityEffect)
            self.opacityAnimation = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")

            # We have a parent, install an eventFilter so that when it's resized
            # the notification will be correctly moved to the right corner
            self.parent().installEventFilter(self)
        else:
            # There's no parent, use the window opacity property, assuming that
            # the window manager supports it; if it doesn't, this won'd do
            # anything (besides making the hiding a bit longer by half a second)
            self.opacityAnimation = QtCore.QPropertyAnimation(self, b'windowOpacity')

        self.opacityAnimation.setStartValue(0.0)
        self.opacityAnimation.setEndValue(1.0)
        self.opacityAnimation.setDuration(100)
        self.opacityAnimation.finished.connect(self.checkClosed)

        self.corner = QtCore.Qt.TopLeftCorner
        self.margin = 10

    def checkClosed(self):
        # If we have been fading out, we're closing the notification
        if self.opacityAnimation.direction() == self.opacityAnimation.Backward:
            self.close()

    def restore(self):
        # This is a "helper function", that can be called from mouseEnterEvent
        # and when the parent widget is resized. We will not close the
        # notification if the mouse is in or the parent is resized
        self.timer.stop()

        # Also, stop the animation if it's fading out...
        self.opacityAnimation.stop()

        # ...and restore the opacity
        if self.parent(): self.opacityEffect.setOpacity(1)
        else: self.setWindowOpacity(1)

    def hide(self):
        self.opacityAnimation.setDirection(self.opacityAnimation.Backward)
        self.opacityAnimation.setDuration(500)
        self.opacityAnimation.start()

    def eventFilter(self, source, event):
        if source == self.parent() and event.type() == QtCore.QEvent.Resize:
            self.opacityAnimation.stop()
            parentRect = self.parent().rect()
            geometry = self.geometry()

            if self.corner == QtCore.Qt.TopLeftCorner:
                geometry.moveTopLeft(parentRect.topLeft() + QtCore.QPoint(self.margin, self.margin))
            elif self.corner == QtCore.Qt.TopRightCorner:
                geometry.moveTopRight(parentRect.topRight() + QtCore.QPoint(-self.margin, self.margin))
            elif self.corner == QtCore.Qt.BottomRightCorner:
                geometry.moveBottomRight(parentRect.bottomRight() + QtCore.QPoint(-self.margin, -self.margin))
            else:
                geometry.moveBottomLeft(parentRect.bottomLeft() + QtCore.QPoint(self.margin, -self.margin))

            self.setGeometry(geometry)
            self.restore()
            self.timer.start()
        return super(QToaster, self).eventFilter(source, event)

    def enterEvent(self, event):
        self.restore()

    def leaveEvent(self, event):
        self.timer.start()

    def closeEvent(self, event):
        self.deleteLater()

    def resizeEvent(self, event):
        super(QToaster, self).resizeEvent(event)

        # If you don't set a stylesheet, you don't need any of the following!
        if not self.parent():

            # There's no parent, so we need to update the mask
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(self.rect()).translated(-0.5, -0.5), 4, 4)
            self.setMask(QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon()))
        else:
            self.clearMask()

    @staticmethod
    def showMessage(parent, message, timeout, corner, closable = True, margin = 10, desktop = False, parentWindow = True):

        if parent and parentWindow:
            parent = parent.window()

        if not parent or desktop:
            self = QToaster(None)
            windowFlags = self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.BypassWindowManagerHint
            self.setWindowFlags(windowFlags)

            # This is a dirty hack!
            # Parentless objects are garbage collected, so the widget will be
            # deleted as soon as the function that calls it returns, but if an
            # object is referenced to *any* other object it will not, at least
            # for PyQt (I didn't test it to a deeper level)
            self.__self = self

            currentScreen = QtWidgets.QApplication.primaryScreen()
            if parent and parent.window().geometry().size().isValid():

                # The notification is to be shown on the desktop, but there is a
                # parent that is (theoretically) visible and mapped, we'll try to
                # use its geometry as a reference to guess which desktop shows
                # most of its area; if the parent is not a top level window, use
                # that as a reference
                reference = parent.window().geometry()
            else:
                # The parent has not been mapped yet, let's use the cursor as a
                # reference for the screen
                reference = QtCore.QRect(QtGui.QCursor.pos() - QtCore.QPoint(1, 1), QtCore.QSize(3, 3))

            maxArea = 0

            for screen in QtWidgets.QApplication.screens():
                intersected = screen.geometry().intersected(reference)
                area = intersected.width() * intersected.height()

                if area > maxArea:
                    maxArea, currentScreen = area, screen
            parentRect = currentScreen.availableGeometry()
        else:
            self = QToaster(parent)
            parentRect = parent.rect()

        self.timer.setInterval(timeout)

        self.label = QtWidgets.QLabel(message)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")

        font = QtGui.QFont()
        font.setFamily("IRANYekanWeb")
        font.setPointSize(10)
        font.setWeight(100)

        self.label.setFont(font)
        self.layout().addWidget(self.label)

        if closable:
            self.closeButton = QtWidgets.QToolButton()

            self.layout().addWidget(self.closeButton)
            closeIcon = self.style().standardIcon(QtWidgets.QStyle.SP_TitleBarCloseButton)

            self.closeButton.setIcon(closeIcon)
            self.closeButton.setAutoRaise(True)
            self.closeButton.clicked.connect(self.close)

        self.timer.start()

        # Raise the widget and adjusts its size to the minimum
        self.raise_()
        self.adjustSize()

        self.corner = corner
        self.margin = margin

        geometry = self.geometry()

        # Now the widget should have the correct size hints, let's move it to the right place
        if corner == QtCore.Qt.TopLeftCorner:
            geometry.moveTopLeft(parentRect.topLeft() + QtCore.QPoint(margin, margin))
        elif corner == QtCore.Qt.TopRightCorner:
            geometry.moveTopRight(parentRect.topRight() + QtCore.QPoint(-margin, margin))
        elif corner == QtCore.Qt.BottomRightCorner:
            geometry.moveBottomRight(parentRect.bottomRight() + QtCore.QPoint(-margin, -margin))
        else:
            geometry.moveBottomLeft(parentRect.bottomLeft() + QtCore.QPoint(margin, -margin))

        self.setGeometry(geometry)
        self.show()
        self.opacityAnimation.start()


def show_message(message, duration = 5000, closable = False):
    parent, desktop = None, True
    corner = QtCore.Qt.BottomRightCorner
    QToaster.showMessage(parent, message, corner = corner, desktop = desktop, timeout = duration, closable = closable)
