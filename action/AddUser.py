from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
import requests

from config import server_address, token
from window import addUser


class AddUser(QtWidgets.QWidget, addUser.Ui_Dialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.buttonBox_Cancel.clicked.connect(self.close)
        self.buttonBox_OK.clicked.connect(self.add_user)

    def add_user(self):
        account = self.lineEdit_account.text()
        password = self.lineEdit_password.text()
        role = self.comboBox_role.currentIndex() + 1
        try:
            response = requests.post(server_address + "/user",
                                     json={'token': token, 'account': account, "password": password, "role": role})
            json_response = response.json()
            if response.status_code == 200:
                QMessageBox.information(self, "添加成功", "用户添加成功")
                self.close()

            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))
