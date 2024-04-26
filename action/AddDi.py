from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
import requests

import config
from window import addDi

class AddDi(QtWidgets.QWidget, addDi.Ui_Dialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.button_cancel.clicked.connect(self.close)
        self.button_confirm.clicked.connect(self.add_di)

    def add_di(self):
        goods_id = self.lineEdit_goodsId.text()
        goods_count = self.lineEdit_goodsNum.text()
        if not (goods_id.isdigit() and goods_count.isdigit()):
            QMessageBox.warning(self, "输入错误", "货物ID和数量应为数字")
            return

        goods_id = int(goods_id)
        goods_count = int(goods_count)
        if goods_id < 1 or goods_count < 1:
            QMessageBox.warning(self, "输入错误", "货物ID和数量应大于0")
            return

        try:
            response = requests.post(config.server_address + "/nekoerp/di",
                                     json={'token': config.token, 'type': goods_id, "count": goods_count})
            json_response = response.json()
            if response.status_code == 200:
                QMessageBox.information(self, "入库成功", "货物入库成功")
                self.close()

            else:
                QMessageBox.warning(self, "请求失败", json_response.get("message"))

        except requests.RequestException as e:
            QMessageBox.warning(self, "请求错误", str(e))