# -*- coding: utf-8 -*-

import random
import sys
import time
import webbrowser

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.mybutton import MyButton
from worker import Worker


class MainWindow(QMainWindow):
    def __init__(self, uid, upw):
        self.uid = uid
        self.upw = upw
        self.lecture_list = list()
        self.assignment_list = list()
        self.course_info = None

        super().__init__()
        uic.loadUi("gui/cs_gui.ui", self)
        self.lecture_table.horizontalHeader().setStretchLastSection(True)
        self.assignment_table.horizontalHeader().setStretchLastSection(True)

        self.th = Worker(self, self.uid, self.upw)
        self.th.fetch_finished.connect(self.update_assignments)

        # 이벤트 연결
        self.titleButton.clicked.connect(self.set_assignments)

    def set_assignments(self):
        if self.th.isRunning:
            return
        self.th.start()
        self.titleButton.setText("밀림의 왕")


    @pyqtSlot(dict)
    def update_assignments(self, data):
        if set(data.keys()) != {'assignment', 'lecture'}:
            self.course_info = data
            self.set_course_container(data)
        elif set(data.keys()) == {'assignment', 'lecture'}:
            self.assignment_table.setRowCount(0)  # clear
            for assignment in data['assignment']:
                self.add_assignment_list(assignment)

            self.lecture_table.setRowCount(0)  # clear
            for lecture in data['lecture']:
                self.add_lecture_table(lecture)

    # args: course_dict
    # type: dict
    # contents: {... <course_id>: <course_name> ...}
    def set_course_container(self, course_dict):
        # 컬러 튜플
        color_tuple = ["#f38181", "#fce38a", "#a8d8ea", "#aa96da", "#bce6eb",
                       "#cca8e9", "#ffa45b", "#fcbad3", "#eaffd0", "#95e1d3"]
        random.shuffle(color_tuple)

        for i, course_id in enumerate(course_dict):
            button = MyButton(self.scroll_dashboard_widget)
            button.setObjectName(f"{course_dict[course_id]}_button")
            button.setText(course_dict[course_id])
            button.setMinimumSize(QSize(300, 50))
            button.setStyleSheet("background-color : " + color_tuple[i % len(color_tuple)])
            button.clickedCourse.connect(self.open_course_page)
            self.gridLayout_2.addWidget(button, i // 3, i % 3)

    # args: lecture
    # type: list
    # contents: course_name, due_date, lecture_name
    def add_lecture_table(self, lecture):
        self.lecture_list.append(lecture)
        self.refresh_lecture_table()

    def refresh_lecture_table(self):
        self.lecture_table.setRowCount(len(self.lecture_list))
        for i, lecture in enumerate(self.lecture_list):
            self.lecture_table.setItem(i, 0, QTableWidgetItem(lecture[0]))
            self.lecture_table.setItem(i, 1, QTableWidgetItem(lecture[1]))
            self.lecture_table.setItem(i, 2, QTableWidgetItem(lecture[2]))

    # args: assignment
    # type: list
    # contents: course_name, due_date, assignment_name
    def add_assignment_list(self, lecture):
        self.assignment_list.append(lecture)
        self.refresh_assignment_list()

    def refresh_assignment_list(self):
        self.assignment_table.setRowCount(len(self.assignment_list))
        for i, assignment in enumerate(self.assignment_list):
            self.assignment_table.setItem(i, 0, QTableWidgetItem(assignment[0]))
            self.assignment_table.setItem(i, 1, QTableWidgetItem(assignment[1]))
            self.assignment_table.setItem(i, 2, QTableWidgetItem(assignment[2]))

    def open_course_page(self, course_name):
        key_list = list(self.course_info.keys())
        val_list = list(self.course_info.values())
        course_id = key_list[val_list.index(course_name)]
        webbrowser.open(f"https://eclass3.cau.ac.kr/courses/{course_id}")

    def test(self):
        print(123)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("eclass id", "eclass pw")

    window.show()
    sys.exit(app.exec_())
