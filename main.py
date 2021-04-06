# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QDialog

from gui.ui_cs_gui import MainWindow
from gui.ui_login_gui import Login

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login_result = login.showModal()

    if login_result == QDialog.Accepted:
        uid, upw = login.idInput.text(), login.pwInput.text()
        window = MainWindow(uid, upw)
        window.show()
    else:
        sys.exit()

    sys.exit(app.exec_())
