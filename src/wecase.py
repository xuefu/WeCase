#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- Linux Sina Weibo Client, Since 4th, Feb, 2013.
#           This is the main file of WeCase.
# Copyright: GPL v3 or later.


import sys
import os
from PyQt4 import QtCore, QtGui
from LoginWindow import LoginWindow
import const
import traceback


def mkconfig():
    try:
        os.mkdir(const.config_path.replace("/config_db", ""))
    except OSError:
        pass

    try:
        os.mkdir(const.cache_path)
    except OSError:
        pass


def my_excepthook(type, value, tback):
    # TODO: Make it works.
    #if type == type(KeyboardInterrupt):
    #    QtGui.QApplication.quit()

    # Let Qt complains about it.
    exception = "".join(traceback.format_exception(type, value, tback))
    QtGui.QMessageBox.critical(None,
                               "Unknown Error",
                               "Oops, there is an unexcepted error: \n" +
                               exception)

    # Then call the default handler
    sys.__excepthook__(type, value, tback)


if __name__ == "__main__":
    mkconfig()

    app = QtGui.QApplication(sys.argv)
    sys.excepthook = my_excepthook

    # Qt's built-in string translator
    qt_translator = QtCore.QTranslator(app)
    qt_translator.load("qt_" + QtCore.QLocale.system().name(),
                       QtCore.QLibraryInfo.location(
                       QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qt_translator)

    # WeCase's own string translator
    my_translator = QtCore.QTranslator(app)
    my_translator.load("WeCase_" + QtCore.QLocale.system().name(),
                       const.myself_path + "locale")
    app.installTranslator(my_translator)

    wecase_login = LoginWindow()

    exit_status = app.exec_()

    # Cleanup code here.

    sys.exit(exit_status)
