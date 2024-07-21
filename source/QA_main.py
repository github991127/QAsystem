from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon

import QA
from list_themes import *


# import os
# envpath = r'E:\anaconda\Lib\site-packages\PySide2\plugins\platforms'
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = envpath


class Stats:
    def __init__(self):
        # 从ui文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('QA.ui')
        self.ui.pushButton.clicked.connect(self.handleCalc)
        self.ui.pushButton_2.clicked.connect(self.handleCalc2)
        self.ui.pushButton_3.clicked.connect(self.handleCalc3)
        self.ui.pushButton_4.clicked.connect(self.handleCalc4)

    def handleCalc(self):
        str = "字帖"
        self.printqa(str)

    def handleCalc2(self):
        str = "握笔"
        self.printqa(str)

    def handleCalc3(self):
        str = "间架结构"
        self.printqa(str)

    def handleCalc4(self):
        str = self.ui.plainTextEdit.toPlainText()
        self.printqa(str)

    def printqa(self, str):
        q, a = QA.QA(str)
        self.ui.textBrowser.clear()
        self.ui.textBrowser_2.clear()
        self.ui.textBrowser.append(q)
        self.ui.textBrowser_2.append(a)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('image.png'))
    apply_stylesheet(app, theme[25], extra=extra, invert_secondary=True)  # 默认False
    stats = Stats()
    stats.ui.show()
    app.exec_()
