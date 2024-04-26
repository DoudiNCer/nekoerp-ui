from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
import requests

import config
from window import addGoods


class AddGoods(QtWidgets.QWidget, addGoods.Ui_Dialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_ok.clicked.connect(self.add_goods)

    def add_goods(self):
        goods_name = self.lineEdit_goods_name.text()
        goods_price = self.lineEdit_goods_price.text()
        try:
            response = requests.post(config.server_address + "/nekoerp/goods",
                                     json={'token': config.token, 'name': goods_name, "price": goods_price})
            json_response = response.json()
            if response.status_code == 200:
                QMessageBox.information(self, "添加成功", "货物信息添加成功")
                self.close()

            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))
