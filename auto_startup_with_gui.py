from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QPushButton, QCheckBox, QHeaderView, QLineEdit, QSpinBox, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
import psutil
import os
import shutil
import sys


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Startup Program Selector'
        self.dark_mode = True
        self.exclude_list = ['Registry']  # 排除列表
        self.initUI()
        self.timer = QTimer(self)  # 创建一个新的定时器对象
        self.timer.timeout.connect(self.on_timer_timeout)  # 连接定时器的超时信号到处理函数
        self.auto_start_timer = True  # 控制是否自动开始定时器
        self.timer.start(20000)  # 自动开始20秒倒计时  
        self.timer.timeout.connect(self.update_msg_box_text)  # 连接定时器的超时信号到更新文本的方法
        self.update_timer = QTimer(self)  # 创建一个新的定时器对象来更新消息框文本
        self.update_timer.timeout.connect(self.update_msg_box_text)
        self.update_timer.start(1000)  # 每秒更新一次
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 700, 400)
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)

        self.selection_buttons_layout = QVBoxLayout()

        self.select_all_button = QPushButton('Select All', self)
        self.select_all_button.clicked.connect(self.on_select_all)
        self.selection_buttons_layout.addWidget(self.select_all_button)

        self.deselect_all_button = QPushButton('Deselect All', self)
        self.deselect_all_button.clicked.connect(self.on_deselect_all)
        self.selection_buttons_layout.addWidget(self.deselect_all_button)

        self.layout.addLayout(self.selection_buttons_layout)

        self.add_to_startup_button = QPushButton('Add to Startup', self)
        self.add_to_startup_button.clicked.connect(self.on_add_to_startup)
        self.layout.addWidget(self.add_to_startup_button)

        self.refresh_button = QPushButton('Refresh', self)
        self.refresh_button.clicked.connect(self.on_refresh)
        self.layout.addWidget(self.refresh_button)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.on_search)
        self.layout.addWidget(self.search_input)

        self.toggle_theme_button = QPushButton('Toggle Theme', self)
        self.toggle_theme_button.clicked.connect(self.on_toggle_theme)
        self.layout.addWidget(self.toggle_theme_button)

        self.setLayout(self.layout)
        self.on_toggle_theme()  # 默认暗黑模式
        self.on_select_all()  # 默认全选
        self.show()
        self.timer_layout = QVBoxLayout()

        self.timer_label = QLabel("Auto-add to startup in (seconds):", self)
        self.timer_layout.addWidget(self.timer_label)

        self.timer_input = QSpinBox(self)
        self.timer_input.setRange(10, 600)  # 设置最小和最大值
        self.timer_input.setValue(60)  # 设置默认值
        self.timer_layout.addWidget(self.timer_input)

        self.start_timer_button = QPushButton("Start Timer", self)
        self.start_timer_button.clicked.connect(self.on_start_timer)
        self.timer_layout.addWidget(self.start_timer_button)

        self.pause_timer_button = QPushButton("Pause Timer", self)
        self.pause_timer_button.clicked.connect(self.on_pause_timer)
        self.timer_layout.addWidget(self.pause_timer_button)
        

        # 弹出消息框让用户选择是否取消倒计时
        self.msg_box = QMessageBox(self)
        self.msg_box.setIcon(QMessageBox.Question)
        self.msg_box.setWindowTitle("Auto-start Timer")
        self.msg_box.setText(f"The timer has started. Auto-add to startup in {self.timer_input.value()} seconds.")
        self.msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msg_box.buttonClicked.connect(self.on_msg_box_button_clicked)
        self.msg_box.show()


        

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['', 'PID', 'Name', 'Executable Path'])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.setSortingEnabled(True)

        main_programs = self.get_main_programs()
        for program in main_programs:
            if any(exclude in program['name'] for exclude in self.exclude_list):  # 排除特定程序
                continue
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(Qt.Checked)  # 默认选中
            self.tableWidget.setItem(row_position, 0, chkBoxItem)
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(str(program['pid'])))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(program['name']))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(program['exe']))

    def get_main_programs(self):
        main_programs = {}
        for process in psutil.process_iter(['pid', 'name', 'exe']):
            if process.info['exe'] and "System32" not in process.info['exe'] and process.info['exe'] not in main_programs:
                main_programs[process.info['exe']] = process.info
        return list(main_programs.values())

    def on_select_all(self):
        for row in range(self.tableWidget.rowCount()):
            chkBoxItem = self.tableWidget.item(row, 0)
            chkBoxItem.setCheckState(Qt.Checked)

    def on_deselect_all(self):
        for row in range(self.tableWidget.rowCount()):
            chkBoxItem = self.tableWidget.item(row, 0)
            chkBoxItem.setCheckState(Qt.Unchecked)

    def on_add_to_startup(self):
        for row in range(self.tableWidget.rowCount()):
            chkBoxItem = self.tableWidget.item(row, 0)
            if chkBoxItem.checkState() == Qt.Checked:
                program_name = self.tableWidget.item(row, 2).text()
                program_path = self.tableWidget.item(row, 3).text()
                self.create_shortcut(program_name, program_path)
                self.add_to_startup(program_name)

    def create_shortcut(self, program_name, program_path):
        with open(f'{program_name}.bat', 'w') as file:
            file.write(f'start "" "{program_path}"\n')

    def add_to_startup(self, program_name):
        startup_path = os.path.expanduser(r'~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
        shutil.copy(f'{program_name}.bat', os.path.join(startup_path, f'{program_name}.bat'))

    def on_toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")
            self.dark_mode = False
        else:
            self.setStyleSheet("QWidget { background-color: #2E2E2E; }"
                               "QTableWidget { background-color: #525252; color: #F0F0F0; }"
                               "QHeaderView::section { background-color: #525252; color: #F0F0F0; }"
                               "QPushButton { background-color: #525252; color: #F0F0F0; }"
                               "QLineEdit { background-color: #525252; color: #F0F0F0; }")
            self.dark_mode = True
    def on_refresh(self):
        self.tableWidget.setRowCount(0)  # 清除现有的行
        main_programs = self.get_main_programs()  # 重新获取主程序列表
        for program in main_programs:
            if any(exclude in program['name'] for exclude in self.exclude_list):  # 排除特定程序
                continue
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(Qt.Checked)  # 默认选中
            self.tableWidget.setItem(row_position, 0, chkBoxItem)
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(str(program['pid'])))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(program['name']))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(program['exe']))

    def on_search(self):
        search_text = self.search_input.text().lower()
        for row in range(self.tableWidget.rowCount()):
            program_name = self.tableWidget.item(row, 2).text().lower()
            program_path = self.tableWidget.item(row, 3).text().lower()
            if search_text in program_name or search_text in program_path:
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)
    def on_start_timer(self):
        self.timer.start(self.timer_input.value() * 1000)  # 将用户输入的秒数转换为毫秒

    def on_pause_timer(self):
        self.timer.stop()  # 停止定时器

    def on_timer_timeout(self):
        self.on_add_to_startup()  # 当定时器超时时，调用 on_add_to_startup 方法
    def on_msg_box_button_clicked(self, button):
        if button.text() == "Yes":
            self.timer.stop()  # 停止定时器
            self.auto_start_timer = False  # 更新标志以表示定时器已被取消
        elif button.text() == "No" and not self.auto_start_timer:
            self.timer.start(self.timer_input.value() * 1000)  # 如果用户之前取消了定时器，但现在想重新开始，就重启定时器
    def update_msg_box_text(self):
        remaining_seconds = self.timer_input.value() - (self.timer.remainingTime() / 1000)
        self.msg_box.setText(f"The timer has started. Auto-add to startup in {int(remaining_seconds)} seconds.")
        if remaining_seconds <= 0:
            self.msg_box.close()
            self.update_timer.stop()  # 停止更新定时器

    def on_timer_timeout(self):
        self.on_add_to_startup()  # 当定时器超时时，调用 on_add_to_startup 方法
        self.msg_box.close()  # 关闭消息框
    def on_msg_box_button_clicked(self, button):
        if button.text() == "Yes":
            self.timer.stop()  # 停止定时器
            self.update_timer.stop()  # 停止更新定时器
            self.auto_start_timer = False  # 更新标志以表示定时器已被取消
        elif button.text() == "No" and not self.auto_start_timer:
            self.timer.start(self.timer_input.value() * 1000)  # 如果用户之前取消了定时器，但现在想重新开始，就重启定时器
            self.update_timer.start(1000)  # 重启更新定时器


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
