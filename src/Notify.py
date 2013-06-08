#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file implemented Notify.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


from PyQt4 import QtCore, QtGui
import const


class Notify(QtCore.QObject):
    image = const.myself_path + "/ui/img/WeCase 80.png"

    def __init__(self, appname=QtCore.QObject().tr("WeCase"), timeout=5):
        super(Notify, self).__init__()
        try:
            import notify2 as pynotify
        except ImportError:
            QtGui.QMessageBox.warning(None, self.tr("Notification disabled"),
                self.tr("notify2 is not found. Notification will disable."))
            import nullNotify as pynotify

        pynotify.init(appname)
        self.timeout = timeout
        self.n = pynotify.Notification(appname)

    def showMessage(self, title, text):
        self.n.update(title, text, self.image)
        self.n.set_timeout(self.timeout * 1000)
        self.n.show()
