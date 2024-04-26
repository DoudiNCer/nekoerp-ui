import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
import requests

import config
from action.MainWindow import MainWindow
from window import loginDialog

class LoginDialog(QtWidgets.QWidget, loginDialog.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 使用loginDialog.py中的setupUi方法

        self.loginButton.clicked.connect(self.login)
        self.exitButton.clicked.connect(sys.exit)

    def login(self):
        config.server_address = self.serverAddress.text()
        config.username = self.username.text()
        password = self.password.text()

        try:
            response = requests.post(config.server_address + "/nekoerp/user/login",
                                     json={'username': config.username, 'password': password})
            json_response = response.json()
            if response.status_code == 200:
                data = json_response.get("data")
                config.token = data.get('token')
                config.role = data.get('role')

                # 关闭登录窗口
                self.close()

                # 加载并展示主窗口，替换为你的MainWindow类
                self.mainWindow = MainWindow()
                self.mainWindow.show()
            else:
                QMessageBox.warning(self, "登录失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))
