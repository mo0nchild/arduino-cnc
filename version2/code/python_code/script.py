# cd C:\Users\Byter\AppData\Local\Programs\Python\Python37-32\
# python C:\Users\Byter\Desktop\QTtest\script.py
# python -m PyQt5.uic.pyuic -x "ваше_имя_фаила.ui" -o "ваше_имя_фаила.py"

import sys , PIL
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(304, 369)
        MainWindow.setFixedSize(304, 369)
        MainWindow.setStyleSheet("QMainWindow{\n"
        "    background-color:#555555   ;\n"
        "}\n"
        "\n"
        "QLineEdit{\n"
        "    background-color:#FF0049  ;\n"
        "    border-radius:28px;\n"
        "    color:#20FF00;\n"
        "    \n"
        "}\n"
        "\n"
        "QLabel{\n"
        "    color:#20FF00;\n"
        "}\n"
        "\n"
        "QPushButton{\n"
        "    background-color:#FF0049  ;\n"
        "    border-radius:28px;\n"
        "    display:inline-block;\n"
        "    cursor:pointer;\n"
        "    color:#20FF00;\n"
        "    font-family:Impact;\n"
        "    font-size:25px;\n"
        "    padding:16px 31px;\n"
        "    text-decoration:none;\n"
        "    text-shadow:0px 1px 0px #2f6627;    \n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    background-color:#FF5B8A ;\n"
        "}\n"
        "QPushButton:active {\n"
        "    position:relative;\n"
        "    top:1px;\n"
        "}\n"
        "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 160, 231, 81))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(-1)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 100, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(16)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 40, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Impact")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 304, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    def functionButtonClicked():
        filename = QFileDialog.getOpenFileName(None, 'Open file', 'C:\\Users\\Byter\\Desktop\\','Image files (*.jpg *.png)')
        filter = str(filename).split(",")[0].replace('(', '')
        filter = str(filter[1:len(filter)-1])
        
        if filter != '':
            print(filter)
            BUFFER = [];buffer, _buffer, B = 0, 0, 0
            img = Image.open(filter)
            img = img.resize((100, 100), PIL.Image.ANTIALIAS)
            px = img.load()

            for y in range(img.size[1]):
                _X = [];BUFFER.append("-")

                for x in range (img.size[0]):
                    cordinate = x, y;VALUE = int(100)
                    r ,g ,b = img.getpixel(cordinate)
                    if r <= VALUE and b <= VALUE and g <= VALUE:
                        px[x, y] = (0, 0, 0)
                        _X.append(x)
                        
                    else: px[x, y] = (255, 255, 255)
                
                if len(_X) != 0:
                    BUFFER.append("A" + str(_X[0]))
                    if (_X[2] - _X[1] != 1)&(_X[3] - _X[2] != 1):BUFFER.append("B0")
                    buffer = _X[0];_buffer += _X[0];

                    for i in range(1,len(_X)):
                        if i != len(_X)-1:
                            if _X[i] - _X[i-1] == 1: B+=1
                            else:
                                if B != 0:
                                    BUFFER.append("B" + str(B))
                                    _buffer += B;B = 0
                                BUFFER.append("A" + str(_X[i] - buffer))
                                if _X[i+1] - _X[i] != 1:BUFFER.append("B0")
                                _buffer += (_X[i] - buffer)
                            buffer = _X[i]
                        else:
                            if _X[len(_X)-1] - _X[len(_X)-2] == 1:
                                BUFFER.append("B" + str(B+1))
                                _buffer += (B+1);B = 0;
                    if _X[len(_X)-1] - _X[len(_X)-2] != 1:
                        BUFFER.append("A" + str(_X[len(_X)-1]))
                        BUFFER.append("B0")
                        _buffer += _X[len(_X)-1]
                    BUFFER.append("C" + str(-_buffer))
                    _buffer = 0    
            print(BUFFER)
            img.save("C:\\Users\\Byter\\Desktop\\IMG_pixelFILTER\\IMAGES\\dfsdfsd.jpg")

    ui.pushButton.clicked.connect(functionButtonClicked)

    sys.exit(app.exec_())
