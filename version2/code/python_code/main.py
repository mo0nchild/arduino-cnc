# TERMINAL COMMAND:
#   cd C:\Users\Byter\AppData\Local\Programs\Python\Python37-32\
#   python C:\Users\Byter\Desktop\ARDUINO_CNC_CODE\python_code\main.py
#   python -m PyQt5.uic.pyuic -x "C:\Users\Byter\Desktop\ARDUINO_CNC_CODE\python_code\interface.ui" -o "C:\Users\Byter\Desktop\ARDUINO_CNC_CODE\python_code\ui.py"

"""
    def __init__(self):self.tasktext = ""

    def TASK_INFOfunc(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.ui.textBrowser.setText(self.tasktext)
        print(self.tasktext)
        self.window.show()
"""

import sys , PIL, serial, threading, time, os
from functools import partial
from PIL import Image, ImageFilter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox

#from ui import Ui_MainWindow
#from taskinfo import Ui_Form
from PyQt5.QtCore import Qt, QThread, pyqtSignal

PORT_SPEED = ['1200','2400', '4800', '9600', '19200', '38400', '57600', '115200']
PORT_LIST = ['NONE'];TEXT_BUFFER = "";SERIALCONNECTION = False;STOP_CHECKER = False;BUFFER = []
IMG_X, IMG_Y = 0, 0;SEND_CHECKER = False;CORDINATE = [0,0]

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Task's Code")
        Form.resize(400, 300)
        Form.setFixedSize(400, 300)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 381, 271))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Task's Code", "Task's Code"))

class MyThread(QThread):
    change_value = pyqtSignal()
    def run(self):
        global arduino
        while True:
            data = str(arduino.readline())
            print(data)
            QApplication.processEvents()
            if data == str(b'ACCEPT\r\n'):
                self.change_value.emit()
                break
            
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.setFixedSize(639, 381)
        self.MainWindow.show()
        self.tasktext = ""
     
    def closeEvent(self):pass

    def TASK_INFOfunc(self):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.ui.textBrowser.setText(self.tasktext)
        self.window.show()

    def ARDUINO_REQUEST(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.get_requets)
        self.thread.start()
 
    def get_requets(self):
        global SEND_CHECKER, TEXT_BUFFER, CORDINATE
        SEND_CHECKER = True
        self.lcdNumber_2.display(CORDINATE[0])
        self.lcdNumber.display(CORDINATE[1])
        TEXT_BUFFER = TEXT_BUFFER + "[+] <<# TASK DONE!>>\n"
        self.textBrowser.setText(str(TEXT_BUFFER))
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(639, 381)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 219, 601, 61))
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 320, 601, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 311, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 30, 31, 21))
        self.pushButton.setObjectName("pushButton")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(370, 8, 21, 201))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.imagelabel = QtWidgets.QLabel(self.centralwidget)
        self.imagelabel.setGeometry(QtCore.QRect(20, 60, 111, 111))
        self.imagelabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.imagelabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imagelabel.setObjectName("imagelabel")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(390, 30, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 30, 71, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(390, 8, 161, 16))
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(320, 60, 51, 20))
        self.spinBox.setMinimum(150)
        self.spinBox.setMaximum(500)
        self.spinBox.setObjectName("spinBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(140, 60, 171, 21))
        self.label_4.setObjectName("label_4")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(320, 90, 51, 20))
        self.spinBox_2.setMinimum(150)
        self.spinBox_2.setMaximum(500)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(140, 90, 171, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(140, 120, 171, 21))
        self.label_6.setObjectName("label_6")
        self.spinBox_3 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_3.setGeometry(QtCore.QRect(320, 120, 51, 22))
        self.spinBox_3.setMaximum(255)
        self.spinBox_3.setProperty("value", 160)
        self.spinBox_3.setObjectName("spinBox_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(390, 58, 31, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(430, 58, 31, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(390, 180, 111, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(510, 180, 111, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(470, 58, 31, 23))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(510, 150, 111, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(20, 180, 121, 23))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(510, 60, 31, 23))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(570, 290, 51, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 290, 511, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setGeometry(QtCore.QRect(150, 180, 111, 23))
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_15 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_15.setGeometry(QtCore.QRect(270, 180, 101, 23))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_17 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_17.setGeometry(QtCore.QRect(520, 30, 23, 23))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_18.setGeometry(QtCore.QRect(540, 290, 21, 23))
        self.pushButton_18.setObjectName("pushButton_18")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(140, 140, 131, 31))
        self.checkBox.setObjectName("checkBox")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(550, 100, 71, 31))
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.Panel)
        self.lcdNumber.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(430, 100, 71, 31))
        self.lcdNumber_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.lcdNumber_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 100, 31, 31))
        self.label_3.setObjectName("label_3")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(520, 100, 31, 31))
        self.label_8.setObjectName("label_8")
        self.pushButton_20 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_20.setGeometry(QtCore.QRect(390, 150, 111, 23))
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_19 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_19.setGeometry(QtCore.QRect(590, 60, 31, 23))
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(550, 60, 31, 23))
        self.pushButton_13.setObjectName("pushButton_13")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        app.aboutToQuit.connect(self.closeEvent)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ARDUINO_CNC"))
        self.pushButton.setText(_translate("MainWindow", "..."))
        self.imagelabel.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Connect"))
        self.label.setText(_translate("MainWindow", "Choose image file:"))
        self.label_2.setText(_translate("MainWindow", "Set COM port:"))
        self.label_4.setText(_translate("MainWindow", "Width: (min=150 , max=500)"))
        self.label_5.setText(_translate("MainWindow", "Height:  (min=150 , max=500)"))
        self.label_6.setText(_translate("MainWindow", "Filter Value:(min=0 , max=255)"))
        self.pushButton_3.setText(_translate("MainWindow", "Y+"))
        self.pushButton_4.setText(_translate("MainWindow", "Y-"))
        self.pushButton_6.setText(_translate("MainWindow", "Start"))
        self.pushButton_7.setText(_translate("MainWindow", "Stop"))
        self.pushButton_9.setText(_translate("MainWindow", "X+"))
        self.pushButton_10.setText(_translate("MainWindow", "Test Size"))
        self.pushButton_11.setText(_translate("MainWindow", "Generate Task"))
        self.pushButton_12.setText(_translate("MainWindow", "X-"))
        self.pushButton_8.setText(_translate("MainWindow", "Send"))
        self.pushButton_14.setText(_translate("MainWindow", "Task Code"))
        self.pushButton_15.setText(_translate("MainWindow", "INFO"))
        self.pushButton_17.setText(_translate("MainWindow", "⟳"))
        self.pushButton_18.setText(_translate("MainWindow", "⟳"))
        self.checkBox.setText(_translate("MainWindow", "Keep Proportions"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">X:</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Y:</span></p></body></html>"))
        self.pushButton_20.setText(_translate("MainWindow", "Set Origin"))
        self.pushButton_19.setText(_translate("MainWindow", "OFF"))
        self.pushButton_13.setText(_translate("MainWindow", "ON"))

def serial_ports():
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):pass
    if len(result) == 0: result = ['NONE']
    return result

def serialPortRefresh():
    global PORT_LIST,arduino,SERIALCONNECTION,TEXT_BUFFER, SEND_CHECKER
    try:
        if SERIALCONNECTION == True: 
            arduino.close()
            SEND_CHECKER = True
            ui.pushButton_2.setText("Connect")
            TEXT_BUFFER += "[-] DISCONNECT SERIALPORT \n"
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            SERIALCONNECTION = False

            ui.comboBox.setEnabled(True)
            ui.pushButton_19.setEnabled(False)
            ui.pushButton_13.setEnabled(False)
            ui.pushButton_3.setEnabled(False)
            ui.pushButton_4.setEnabled(False)
            ui.pushButton_9.setEnabled(False)
            ui.pushButton_12.setEnabled(False)
            ui.pushButton_6.setEnabled(False)
            ui.pushButton_7.setEnabled(False)
            ui.pushButton_10.setEnabled(False)

        PORT_LIST = serial_ports()
        ui.comboBox.clear()
        ui.comboBox.addItems(PORT_LIST)
    except:print("NOT SUPPORT")

def imageFilePath():
    filename = QFileDialog.getOpenFileName(None, 'Open file', 'C:\\','Image files (*.jpg *.png)')
    _path = str(filename).split(",")[0].replace('(', '')
    _path = str(_path[1:len(_path)-1])
    ui.lineEdit.setText(_path)

def generateTASK():
    global TEXT_BUFFER,_ABS, BUFFER, SERIALCONNECTION,IMG_X,IMG_Y
    
    PATH = ui.lineEdit.text()
    if PATH != '':
        ui.imagelabel.clear()
        switch_side = False

        BUFFER = [];TASK_BUF = [];back_len,buffer, _buffer, B = 0, 0, 0, 0
        img = Image.open(PATH).convert('RGB')
        W, H = img.size

        _W = ui.spinBox.value()
        _H = ui.spinBox_2.value()
            #STEP_PIX = ui.spinBox_7.value()
            #PRINT_DELAY = ui.spinBox_4.value()

        if ui.checkBox.isChecked():
            if(W > H):_H = int(_W*H/W)
            elif(H > W):_W = int(_H/H*W)

        IMG_X = _W
        IMG_Y = _H
        img = img.resize((_W, _H), PIL.Image.ANTIALIAS)
        img = img.filter(ImageFilter.MedianFilter(1))
        px = img.load()

        BAR_STEP = _H/100
        BAR_PROGRESS = 0

            #BUFFER.append(int(STEP_PIX))
            #BUFFER.append(int(PRINT_DELAY))
        BUFFER.append("D0")
        for y in range(img.size[1]):
            _X = [];#BUFFER.append("Y1")

            for x in range (img.size[0]):
                cordinate = x, y;VALUE = int(ui.spinBox_3.value())
                r ,g ,b = img.getpixel(cordinate)
                sr = (r + g + b)//3
                if sr >= VALUE:
                    px[x, y] = (255, 255, 255)
                           
                else: 
                    px[x, y] = (0, 0, 0)
                    _X.append(x)  
            print(_X)
            if len(_X) > 0:
                BUFFER.append("X" + str(_X[0]))
                if(len(_X)) == 1:
                    BUFFER.append("D1")
                    BUFFER.append("D0")
                else:
                    if (_X[1] - _X[0] != 1):#&(_X[3] - _X[2] != 1):
                        BUFFER.append("D1")
                        BUFFER.append("D0")
                    buffer = _X[0];_buffer += _X[0];

                    #if(y==29):print(str(_X))
                for i in range(1,len(_X)):
                    if i != len(_X)-1:
                        if _X[i] - _X[i-1] == 1:B+=1
                        else:
                            if B != 0:
                                BUFFER.append("D1")
                                BUFFER.append("X" + str(B))
                                BUFFER.append("D0")
                                _buffer += B;B = 0
                            BUFFER.append("X" + str(_X[i] - buffer))
                            if _X[i+1] - _X[i] != 1:
                                BUFFER.append("D1")
                                BUFFER.append("D0")
                            _buffer += (_X[i] - buffer)
                        buffer = _X[i]
                    else:
                        if _X[len(_X)-1] - _X[len(_X)-2] == 1:
                            BUFFER.append("D1")
                            BUFFER.append("X" + str(B+1))
                            BUFFER.append("D0")
                            _buffer += (B+1);B = 0;
                if _X[len(_X)-1] - _X[len(_X)-2] != 1:
                    if(B!=0):
                        BUFFER.append("D1")
                        BUFFER.append("X" + str(B))
                        BUFFER.append("D0")
                        #_buffer += B;B = 0
                    BUFFER.append("X" + str(_X[len(_X)-1] - _X[len(_X)-2]))
                    #print(_X[len(_X)-1] - _X[len(_X)-2])
                    BUFFER.append("D1")
                    BUFFER.append("D0")
                    _buffer += _X[len(_X)-1]
                    #BUFFER.append("X" + str(-_X[len(_X)-1]))
                    #BUFFER.append("Y1")
                back_len = img.size[0] - _X[len(_X)-1]
                #print(str(y)+ "}  " + str(_buffer) + "   "+ str(B) + "    "+ str(_X[len(_X)-1]))
                B, _buffer = 0, 0

            if(switch_side):
                if(len(_X) > 0):
                    print(str(len(_X)))
                    if(back_len != 0):TASK_BUF.append("X-" + str(back_len))
                    for i in range (len(BUFFER)-1, -1,-1):
                        if(BUFFER[i] == "D1"):TASK_BUF.append("D0")
                        elif(BUFFER[i] == "D0"):TASK_BUF.append("D1")
                        else:TASK_BUF.append(BUFFER[i][0:1] + "-" + BUFFER[i][1:len(BUFFER)-1])
                    switch_side = False
                TASK_BUF.append("Y1")
                
            else:
                if(len(_X) > 0):
                    print(str(len(_X)))
                    for i in range (0,len(BUFFER),1):
                        TASK_BUF.append(BUFFER[i])
                    if(back_len != 0):TASK_BUF.append("X" + str(back_len))
                    switch_side = True 
                TASK_BUF.append("Y1")
                 
                #print(str(y)+")"+str(BUFFER) + "   " + str(back_len))
                
            BAR_PROGRESS += BAR_STEP
            ui.progressBar.setValue(BAR_PROGRESS)
            BUFFER = []

        for i in range(len(TASK_BUF)):BUFFER.append(TASK_BUF[i])
        print(BUFFER)
        TEXT_BUFFER += "[+] TASK WAS GENERATED\n"

            #F = PATH.split('/');_F = ""
            #for i in range(len(F)-1):_F = _F + str(F[i]) + "/"
        if(_W >= _H):
            _H = int(101*_H/_W)
            _W = int(101)
        elif(_H > _W):
            _W = int(91*_W/_H)
            _H = int(91)
        currdir = ""
        filedir = str(os.path.abspath(__file__)).split('\\')
        for i in range(len(filedir)-1):currdir = currdir + str(filedir[i]) + "\\"
        img = img.resize((_W, _H), PIL.Image.ANTIALIAS)
        #img = img.resize((500, 450), PIL.Image.ANTIALIAS)
        img.save(currdir + "BUFFER_IMG.jpg")
            
        ui.lineEdit.setText("")
        pixmap = QPixmap(currdir + "BUFFER_IMG.jpg")
        ui.imagelabel.setPixmap(pixmap)
        ui.imagelabel.repaint()
        QApplication.processEvents()
        ui.pushButton_14.setEnabled(True)
        if(SERIALCONNECTION == True):
            ui.pushButton_6.setEnabled(True)
            ui.pushButton_10.setEnabled(True)

    """except IndexError:
        TEXT_BUFFER += "[!] CAN'T GENERATE TASK, TRY TO CHANGE FILTER VALUE OR IMAGE\n"
        ui.imagelabel.clear()
        BUFFER = []
        ui.imagelabel.setText("        NO IMAGE")
        ui.pushButton_14.setEnabled(False)
        ui.pushButton_6.setEnabled(False)
        ui.pushButton_10.setEnabled(False)"""

    ui.progressBar.setValue(0)
    ui.textBrowser.setText(str(TEXT_BUFFER))
    ui.textBrowser.moveCursor(QtGui.QTextCursor.End)

def textBrowserRefresh():
    global TEXT_BUFFER,SERIALCONNECTION
    TEXT_BUFFER = ""
    ui.textBrowser.setText("")
    
def connectArduino():
    global SERIALCONNECTION,arduino, TEXT_BUFFER, BUFFER,SEND_CHECKER
    port = str(ui.comboBox.currentText())
    if (SERIALCONNECTION != True):
        try:
            ui.pushButton_2.setText("Close")
            arduino = serial.Serial(port, 115200, timeout=.1)
            TASK_TEST = " TEST "
            PROGRESSBAR_VALUE = 0
            for text in TASK_TEST:
                arduino.write(text.encode())
                time.sleep(.005)
                print(str(arduino.readline()))
                PROGRESSBAR_VALUE+=25
                ui.progressBar.setValue(PROGRESSBAR_VALUE)
                #QApplication.processEvents()
            time.sleep(.1)
            print(str(arduino.readline()))
            TEXT_BUFFER += "[+] CONNECT SERIALPORT \n"
            ui.progressBar.setValue(0)
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            SERIALCONNECTION = True
            SEND_CHECKER = True

            ui.pushButton_3.setEnabled(True)
            ui.pushButton_4.setEnabled(True)
            ui.pushButton_19.setEnabled(True)
            ui.pushButton_13.setEnabled(True)
            ui.pushButton_9.setEnabled(True)
            ui.pushButton_12.setEnabled(True)
            ui.pushButton_7.setEnabled(False)
            ui.comboBox.setEnabled(False)
            if len(BUFFER) != 0:
                ui.pushButton_6.setEnabled(True)
                ui.pushButton_10.setEnabled(True)

        except:
            ui.pushButton_2.setText("Connect")
            TEXT_BUFFER += "[!] CANT OPEN SERIALPORT\n"
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            SERIALCONNECTION = False
            SEND_CHECKER = False

            ui.comboBox.setEnabled(True)
            ui.pushButton_3.setEnabled(False)
            ui.pushButton_4.setEnabled(False)
            ui.pushButton_9.setEnabled(False)
            ui.pushButton_12.setEnabled(False)
            ui.pushButton_6.setEnabled(False)
            ui.pushButton_7.setEnabled(False)
            ui.pushButton_10.setEnabled(False)
    else:
        arduino.close()
        ui.pushButton_2.setText("Connect")
        TEXT_BUFFER += "[-] DISCONNECT SERIALPORT \n"
        ui.textBrowser.setText(str(TEXT_BUFFER))
        ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
        SERIALCONNECTION = False
        SEND_CHECKER = False

        ui.comboBox.setEnabled(True)
        ui.pushButton_3.setEnabled(False)
        ui.pushButton_4.setEnabled(False)
        ui.pushButton_9.setEnabled(False)
        ui.pushButton_12.setEnabled(False)
        ui.pushButton_6.setEnabled(False)
        ui.pushButton_7.setEnabled(False)
        ui.pushButton_10.setEnabled(False)

def funcSTARTTASK():
    global PORT_LIST,arduino,SERIALCONNECTION,TEXT_BUFFER, BUFFER,STOP_CHECKER,SEND_CHECKER,CORDINATE
    TASK_TEXT = ""
    #print(len(BUFFER))
    try:
        if(SERIALCONNECTION != False)and(STOP_CHECKER != True)and(SEND_CHECKER != False):
            if(len(BUFFER)==0):
                TEXT_BUFFER += "[!] TASK WASNT GENERATED \n"
                ui.textBrowser.setText(str(TEXT_BUFFER))
                ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            else:
                ui.pushButton_3.setEnabled(False)
                ui.pushButton_4.setEnabled(False)
                ui.pushButton_9.setEnabled(False)
                ui.pushButton_12.setEnabled(False)
                ui.pushButton_6.setEnabled(False)
                ui.pushButton_10.setEnabled(False)
                ui.pushButton_7.setEnabled(True)

                TEXT_BUFFER += "[+] PROCESSING... PLEASE WAIT\n"
                ui.textBrowser.setText(str(TEXT_BUFFER))
                ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
                PROGRESSBAR_VALUE = 0
                PROGRESSBAR_STEP = 100/len(BUFFER)
                for i in range(len(BUFFER)):
                    TASK_TEXT = str(BUFFER[i])+' '
                    if(STOP_CHECKER != False):break
                    SEND_CHECKER = True
                    SEND_DATA(TASK_TEXT)
                    while True:
                        QApplication.processEvents()
                        if SEND_CHECKER == True:
                            SEND_CHECKER = False
                            break   
                    PROGRESSBAR_VALUE += PROGRESSBAR_STEP
                    ui.progressBar.setValue(PROGRESSBAR_VALUE)
                SEND_CHECKER = True
                ui.progressBar.setValue(0)
                SEND_DATA("M0 ")
                ui.lcdNumber.display(0)
                ui.lcdNumber_2.display(0)
                CORDINATE = [0,0]

    except:
        TEXT_BUFFER += "[!] HAVE SOME PROBLEM WITH START TAST\n"
        ui.textBrowser.setText(str(TEXT_BUFFER))
        ui.textBrowser.moveCursor(QtGui.QTextCursor.End)  
    ui.pushButton_3.setEnabled(True)
    ui.pushButton_4.setEnabled(True)
    ui.pushButton_9.setEnabled(True)
    ui.pushButton_12.setEnabled(True)
    ui.pushButton_6.setEnabled(True)
    ui.pushButton_10.setEnabled(True)
    ui.pushButton_7.setEnabled(False)
    STOP_CHECKER = False
    SEND_CHECKER = True

def funcSTOPTASK():
    global STOP_CHECKER,arduino, TEXT_BUFFER
    ret = QMessageBox.question(None, 'MessageBox', "Are You Sure?", QMessageBox.Yes | QMessageBox.No | QMessageBox.No)
    if ret == QMessageBox.Yes:
        STOP_CHECKER = True
        QApplication.processEvents()

def CONTROL_AXIS(AXIS):
    global TEXT_BUFFER, SEND_CHECKER
    if(SEND_CHECKER != False):SEND_DATA(str(AXIS) + ' ')

def loadSettings():
    global SEND_CHECKER
    if(SEND_CHECKER != False):
        SETTINGS_DATA = "S."
        if str(ui.comboBox_3.currentText()) == "Servo":
            SETTINGS_DATA = "SERVO."+str(ui.spinBox_6.value())+"."
        else:SETTINGS_DATA = "LASER."+str(ui.spinBox_8.value())+"."
        SETTINGS_DATA = SETTINGS_DATA + str(ui.comboBox_4.currentText()) + "."
        SETTINGS_DATA = SETTINGS_DATA + str(ui.spinBox_7.value()) + "."
        SETTINGS_DATA = SETTINGS_DATA + str(ui.spinBox_4.value()) + " "
        print(SETTINGS_DATA)
        SEND_DATA(SETTINGS_DATA)
        SEND_CHECKER = True
"""
def GET_REQUEST():
    global TEXT_BUFFER, SEND_CHECKER, arduino
    while True:
        data = str(arduino.readline())
        QApplication.processEvents()
        if data == str(b'ACCEPT\r\n'):
            TEXT_BUFFER += "[+] <<DONE>>\n"
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            SEND_CHECKER = True
            break
"""
def SEND_DATA(DATA):
    global TEXT_BUFFER, SEND_CHECKER, CORDINATE
    try:
        if(SEND_CHECKER != False):
            SEND_CHECKER = False
            TEXT_BUFFER = TEXT_BUFFER + "[+] >>["+ DATA +"]PROCESSING... PLEASE WAIT<<\n"
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
            QApplication.processEvents()
            if DATA[0] == "X":CORDINATE[0] += int(DATA[1:len(DATA)-1])
            elif DATA[0] == "Y":CORDINATE[1] += int(DATA[1:len(DATA)-1])
            for text in DATA:
                arduino.write(text.encode())
                QApplication.processEvents()
                time.sleep(.005)
            ui.ARDUINO_REQUEST()
    except:
        SEND_CHECKER = True
        TEXT_BUFFER = TEXT_BUFFER + "[!] FAILED TO SEND DATA\n"
        ui.textBrowser.setText(str(TEXT_BUFFER))
        ui.textBrowser.moveCursor(QtGui.QTextCursor.End)

def CONTROL_SERVO(VALUE):
    global TEXT_BUFFER, SEND_CHECKER
    if(SEND_CHECKER != False):
        try:SEND_DATA("D" + str(VALUE) + " ")
        except:
            SEND_CHECKER = True
            TEXT_BUFFER = TEXT_BUFFER + "[!] FAILED TO SEND DATA\n"
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)

def funcTESTTASK():
    global TEXT_BUFFER, SEND_CHECKER
    if(SEND_CHECKER != False):
        try:
            TASK = ["D1 ","X" + str(IMG_X)+" ", "Y" + str(IMG_Y)+" ","X-" + str(IMG_X)+" ",
                "Y-" + str(IMG_Y)+" ","D0 "]
            for PROCESS in TASK:
                SEND_CHECKER = True
                print(PROCESS)
                SEND_DATA(PROCESS)
                while True:
                    QApplication.processEvents()
                    if SEND_CHECKER == True:
                        SEND_CHECKER = False
                        break   
            SEND_CHECKER = True
        except:
            SEND_CHECKER = True
            TEXT_BUFFER = TEXT_BUFFER + "[!] FAILED TO SEND DATA\n"
            ui.textBrowser.setText(str(TEXT_BUFFER))
            ui.textBrowser.moveCursor(QtGui.QTextCursor.End)

def func_toSEND_TASKTEXT():
    global BUFFER
    ui.tasktext = str(BUFFER)
    ui.TASK_INFOfunc()

def funcINFO():pass

def SET_ORIGIN():
    global CORDINATE, SEND_CHECKER
    if(SEND_CHECKER != False):
        ui.lcdNumber.display(0)
        ui.lcdNumber_2.display(0)
        CORDINATE = [0,0]
        SEND_DATA("R0 ")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    PORT_LIST = serial_ports()

    ui.imagelabel.setScaledContents(False)
    ui.imagelabel.setText("        NO IMAGE")
    ui.comboBox.addItems(PORT_LIST)

    ui.pushButton_17.clicked.connect(serialPortRefresh)
    ui.pushButton_11.clicked.connect(generateTASK)
    ui.pushButton.clicked.connect(imageFilePath)
    ui.pushButton_2.clicked.connect(connectArduino)
    ui.pushButton_18.clicked.connect(textBrowserRefresh)
    ui.pushButton_3.clicked.connect(partial(CONTROL_AXIS,'Y5'))
    ui.pushButton_4.clicked.connect(partial(CONTROL_AXIS,'Y-5'))
    ui.pushButton_6.clicked.connect(funcSTARTTASK)
    ui.pushButton_7.clicked.connect(funcSTOPTASK)
    ui.pushButton_9.clicked.connect(partial(CONTROL_AXIS,'X5'))
    ui.pushButton_12.clicked.connect(partial(CONTROL_AXIS,'X-5'))
    ui.pushButton_13.clicked.connect(partial(CONTROL_SERVO,1))
    ui.pushButton_19.clicked.connect(partial(CONTROL_SERVO,0))
    ui.pushButton_10.clicked.connect(funcTESTTASK)
    ui.pushButton_14.clicked.connect(func_toSEND_TASKTEXT)
    ui.pushButton_15.clicked.connect(funcINFO)
    ui.pushButton_20.clicked.connect(SET_ORIGIN)

    ui.pushButton_3.setEnabled(False)
    ui.pushButton_4.setEnabled(False)
    ui.pushButton_9.setEnabled(False)
    ui.pushButton_12.setEnabled(False)
    ui.pushButton_6.setEnabled(False)
    ui.pushButton_7.setEnabled(False)
    ui.pushButton_19.setEnabled(False)
    ui.pushButton_13.setEnabled(False)

    ui.pushButton_10.setEnabled(False)
    ui.pushButton_14.setEnabled(False)

    sys.exit(app.exec_())