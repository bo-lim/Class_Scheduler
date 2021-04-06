# -*- coding: utf-8 -*-

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *


class LoginFailWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('밀림의 왕 - 로그인 실패')
        self.setWindowIcon(QIcon("lion.png"))
        self.setStyleSheet("color : black; background-color: #59886B")
        self.setFixedSize(400, 180)

        errorLabel = QLabel(self)
        errorLabel.setText("잘못된 로그인 정보입니다.\n아이디 또는 비밀번호를 확인해주세요.")
        errorLabel.setStyleSheet("color : black; background-color: #59886B")
        errorLabel.setObjectName(u"errorLabel")
        errorLabel.setStyleSheet(
            "background-color : #d9c6a5; border-style: solid; border-color : black; border-width : 1px;")
        errorLabel.setGeometry(QRect(50, 40, 300, 70))
        font = QFont('고딕')
        font.setPointSize(10)
        errorLabel.setFont(font)
        errorLabel.setAlignment(Qt.AlignCenter)
        errorOKButton = QPushButton(self)
        errorOKButton.setText("확인")
        errorOKButton.setObjectName(u"errorOKButton")
        errorOKButton.setStyleSheet("background-color : #dbf6e9")
        errorOKButton.setGeometry(QRect(160, 130, 80, 25))
        errorOKButton.clicked.connect(self.onOKButtonClicked)

    def onOKButtonClicked(self):
        self.accept()

    def showModal(self):
        return super().exec_()
