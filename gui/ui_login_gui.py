# -*- coding: utf-8 -*-

import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import *

from crawler.eclassauth import EClass
from gui.login_fail import LoginFailWindow


class Login(QDialog):
    e_class = EClass()

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        uic.loadUi("gui/login_gui_dialog.ui", self)
        self.setFixedSize(680, 430)
        self.pwInput.setEchoMode(QLineEdit.Password)
        self.loginBtn.clicked.connect(self.loginButtonClicked)

    @staticmethod
    def open_error_dialog():
        win = LoginFailWindow()
        win.showModal()

    def loginButtonClicked(self):
        uid = self.idInput.text()
        upw = self.pwInput.text()
        if self.e_class.login(uid, upw):
            self.e_class.quit()
            self.accept()
        else:
            self.open_error_dialog()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()

    def closeEvent(self, QCloseEvent):
        self.e_class.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()

    login = Login()

    if login.exec_() == QDialog.Accepted:
        window.show()
        sys.exit(app.exec_())
