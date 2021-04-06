# -*- coding: utf-8 -*-

import time

from PyQt5.QtCore import QThread, pyqtSignal

from crawler.controller import Controller


class Worker(QThread):
    fetch_finished = pyqtSignal(dict)

    def __init__(self, parent, uid, upw):
        super().__init__(parent)
        self.parent = parent
        self.isRunning = False
        self.init = True
        self.controller = Controller(uid, upw)

    def run(self):
        self.isRunning = True
        self.parent.titleButton.setText("사자가 열심히 정글을 뒤지고 있어요..!")

        if self.init:
            self.init = False
            self.fetch_finished.emit(self.controller.get_course_info())

        data = self.controller.get_all_assignments()
        self.fetch_finished.emit(data)
        self.parent.titleButton.setText("밀림의 왕")
        self.isRunning = False

