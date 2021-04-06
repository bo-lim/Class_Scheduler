from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton


class MyButton(QPushButton):
    clickedCourse = pyqtSignal(str)  # 발생하는 int type 시그널을 저장하는 시그널 객체

    def __init__(self, gird):
        super(MyButton, self).__init__(gird)
        self.init_ui()

    def init_ui(self):
        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        ori_text = str(self.text()).replace('\n', ' ')
        self.clickedCourse.emit(ori_text)
