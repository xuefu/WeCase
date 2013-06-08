import os
from time import sleep
import urllib.request
import http.client
from PyQt4 import QtCore, QtGui
from const import cache_path as down_path
from WeHack import async


class WAsyncLabel(QtGui.QLabel):

    clicked = QtCore.pyqtSignal()
    downloaded = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(WAsyncLabel, self).__init__(parent)
        self.url = ""
        self.timer = QtCore.QTimer(self)
        self.busy_icon = QtGui.QPixmap("./icon/busy.png")

    def setBusy(self, busy):
        if busy:
            self.degress = 0
            self.timer.timeout.connect(self.drawBusyIcon)
            self.timer.start(50)
        else:
            self.clearBusyIcon()

    def drawBusyIcon(self):
        image = QtGui.QPixmap(self._image)
        icon = self.busy_icon.transformed(QtGui.QTransform().rotate(self.degress))

        height = (image.height() - icon.height()) / 2
        width = (image.width() - icon.width()) / 2
        painter = QtGui.QPainter(image)
        painter.drawPixmap(width, height, icon)
        painter.end()
        super(WAsyncLabel, self).setPixmap(image)
        self.degress += 8

    def clearBusyIcon(self):
        self.timer.stop()
        super(WAsyncLabel, self).setPixmap(self._image)

    def url(self):
        return self.url

    def _setPixmap(self, path):
        image = QtGui.QPixmap(path)
        if image.width() < self.busy_icon.width():
            image = image.scaledToWidth(self.busy_icon.width())
        self._image = image
        super(WAsyncLabel, self).setPixmap(image)

    def setPixmap(self, url):
        if not ("http" in url):
            self._setPixmap(url)
            return
        self.url = url
        self.downloaded.connect(self._setPixmap)
        self._fetch_meta()

    def _fetch_meta(self):
        filename = "%s_%s" % (self.url.split('/')[-2],
                              self.url.split('/')[-1])
        self._fetch(self.url, filename)

    @async
    def _fetch(self, url, filename):
        while os.path.exists(down_path + filename + ".down"):
            sleep(0.5)
            continue

        if os.path.exists(down_path + filename):
            return self.downloaded.emit(down_path + filename)

        while 1:
            try:
                urllib.request.urlretrieve(url, down_path + filename + ".down")
                break
            except http.client.BadStatusLine:
                continue

        try:
            os.rename(down_path + filename + ".down",
                      down_path + filename)
        except FileNotFoundError:
            pass

        return self.downloaded.emit(down_path + filename)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()
