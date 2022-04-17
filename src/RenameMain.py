import Gui.MainFrame as MF
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MF.UiMainWindow()
    sys.exit(app.exec_())