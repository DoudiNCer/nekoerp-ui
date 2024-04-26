from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
import requests

from config import server_address, token, role, username
from action.AddDi import AddDi
from action.AddTiao import AddTiao
from action.AddGoods import AddGoods
from action.AddUser import AddUser
from window import mainWindow
from datetime import datetime


class MainWindow(QtWidgets.QWidget, mainWindow.Ui_ManagementSystem):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.userInfoLabel.setText("用户名: [" + username + "] 权限: [" + role + "]")
        self.tableWidget_goods.setHorizontalHeaderLabels(["ID", "名称", "单价"])
        self.tableWidget_storage.setHorizontalHeaderLabels(["ID", "名称", "数量", "单价"])
        self.tableWidget_di.setHorizontalHeaderLabels(["ID", "名称", "数量", "单价", "操作员", "时间"])
        self.tableWidget_tiao.setHorizontalHeaderLabels(["ID", "名称", "数量", "单价", "操作员", "时间"])
        self.tableWidget_users.setHorizontalHeaderLabels(["ID", "账户", "权限", "创建时间", "编辑时间", "是否已禁用"])
        if role != "admin":
            self.userInfoLabel.setEnabled(False)

        self.tabWidget.currentChanged.connect(self, self.table_changed)
        self.pushButton_searchGoods.clicked.connect(self.draw_goods)
        self.pushButton_searchStorage.clicked.connect(self.draw_storage)
        self.pushButton_searchDi.clicked.connect(self.draw_di)
        self.pushButton_searchTiao.clicked.connect(self.draw_tiao)
        self.pushButton_searchUser.clicked.connect(self.draw_user)

        self.pushButton_addGoods.clicked.connect(self.add_goods)
        self.pushButton_addUser.clicked.connect(self.addUser)
        self.pushButton_addDi.clicked.connect(self.di)
        self.pushButton_addTiao.clicked.connect(self.tiao)

    def table_changed(self, index):
        {
            0: self.draw_goods,
            1: self.draw_storage,
            2: self.draw_di,
            3: self.draw_tiao,
            4: self.draw_user
        }[index]()

    def draw_goods(self):
        keyword = self.lineEdit_searchGoods.text()
        try:
            response = requests.get(server_address + "/goods", json={'token': token, 'keyword': keyword})
            json_response = response.json()
            if response.status_code == 200:
                list_data = json_response.get("list", [])
                self.tableWidget_goods.setRowCount(0)
                for row_index, item in enumerate(list_data):
                    self.tableWidget_goods.insertRow(row_index)
                    self.tableWidget_goods.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item.get("id"))))
                    self.tableWidget_goods.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.get("name")))
                    self.tableWidget_goods.setItem(row_index, 2,
                                                   QtWidgets.QTableWidgetItem(f"{item.get('price', 0):0.2f}"))

            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))

    def draw_storage(self):
        keyword = self.lineEdit_searchStorage.text()
        try:
            response = requests.get(server_address + "/storage",
                                    json={'token': token, 'keyword': keyword})
            json_response = response.json()
            if response.status_code == 200:
                list_data = json_response.get("list", [])
                self.tableWidget_storage.setRowCount(0)
                for row_index, item in enumerate(list_data):
                    self.tableWidget_storage.insertRow(row_index)
                    self.tableWidget_storage.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item.get("id"))))
                    self.tableWidget_storage.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.get("name")))
                    self.tableWidget_storage.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(item.get("count"))))
                    self.tableWidget_storage.setItem(row_index, 3,
                                                     QtWidgets.QTableWidgetItem(f"{item.get('price', 0):0.2f}"))
            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))

    def draw_di(self):
        keyword = self.lineEdit_searchDi.text()
        try:
            response = requests.get(server_address + "/di", json={'token': token, 'keyword': keyword})
            json_response = response.json()
            if response.status_code == 200:
                list_data = json_response.get("list", [])
                self.tableWidget_di.setRowCount(0)
                for row_index, item in enumerate(list_data):
                    self.tableWidget_di.insertRow(row_index)
                    self.tableWidget_di.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item.get("id"))))
                    self.tableWidget_di.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.get("name")))
                    self.tableWidget_di.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(item.get("role"))))
                    created_at = item.get("createdAt")
                    if created_at != "":
                        created_at = datetime.fromisoformat(created_at).strftime("'%Y/%m/%d %H:%M:%S")

                    self.tableWidget_di.setItem(row_index, 3, QtWidgets.QTableWidgetItem(created_at))
                    updated_at = item.get("updatedAt")
                    if updated_at != "":
                        updated_at = datetime.fromisoformat(updated_at).strftime("'%Y/%m/%d %H:%M:%S")

                    self.tableWidget_di.setItem(row_index, 4, QtWidgets.QTableWidgetItem(updated_at))
                    self.tableWidget_users.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(item.get("blocked"))))
            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))

    def draw_tiao(self):
        keyword = self.lineEdit_searchDi.text()
        try:
            response = requests.get(server_address + "/tiao", json={'token': token, 'keyword': keyword})
            json_response = response.json()
            if response.status_code == 200:
                list_data = json_response.get("list", [])
                self.tableWidget_tiao.setRowCount(0)
                for row_index, item in enumerate(list_data):
                    self.tableWidget_tiao.insertRow(row_index)
                    self.tableWidget_tiao.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item.get("id"))))
                    self.tableWidget_tiao.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.get("name")))
                    self.tableWidget_tiao.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(item.get("count"))))
                    self.tableWidget_tiao.setItem(row_index, 3,
                                                  QtWidgets.QTableWidgetItem(f"{item.get('price', 0):0.2f}"))
                    self.tableWidget_tiao.setItem(row_index, 4, QtWidgets.QTableWidgetItem(item.get("account")))
                    created_at = item.get("createdAt")
                    if created_at != "":
                        created_at = datetime.fromisoformat(created_at).strftime("'%Y/%m/%d %H:%M:%S")

                    self.tableWidget_tiao.setItem(row_index, 5, QtWidgets.QTableWidgetItem(created_at))
            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))

    def draw_user(self):
        keyword = self.lineEdit_searchDi.text()
        try:
            response = requests.get(server_address + "/user", json={'token': token, 'keyword': keyword})
            json_response = response.json()
            if response.status_code == 200:
                list_data = json_response.get("list", [])
                self.tableWidget_tiao.setRowCount(0)
                for row_index, item in enumerate(list_data):
                    self.tableWidget_tiao.insertRow(row_index)
                    self.tableWidget_tiao.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(item.get("id"))))
                    self.tableWidget_tiao.setItem(row_index, 1, QtWidgets.QTableWidgetItem(item.get("account")))
                    self.tableWidget_tiao.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(item.get("count"))))
                    self.tableWidget_tiao.setItem(row_index, 3,
                                                  QtWidgets.QTableWidgetItem(f"{item.get('price', 0):0.2f}"))
                    self.tableWidget_tiao.setItem(row_index, 4, QtWidgets.QTableWidgetItem(item.get("account")))
                    created_at = item.get("createdAt")
                    if created_at != "":
                        created_at = datetime.fromisoformat(created_at).strftime("'%Y/%m/%d %H:%M:%S")

                    self.tableWidget_tiao.setItem(row_index, 5, QtWidgets.QTableWidgetItem(created_at))
            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))

    def add_goods(self):
        self.addGoods = AddGoods()
        self.addGoods.show()
        self.draw_goods()

    def add_user(self):
        self.addUser = AddUser()
        self.addUser.show()
        self.draw_user()

    def di(self):
        self.addDi = AddDi()
        self.addDi.show()
        self.draw_di()

    def tiao(self):
        self.addTiao = AddTiao()
        self.addTiao.show()
        self.draw_tiao()
