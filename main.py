from PyQt6 import QtWidgets
import sys
from action import LoginDialog

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginDialog.LoginDialog()
    login_window.show()
    sys.exit(app.exec())
