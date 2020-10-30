import sys
import os
import commodity
import industry
from PyQt5.QtWidgets import QApplication,QLineEdit,QPushButton,QCheckBox,QWidget, QVBoxLayout,QHBoxLayout,QLabel, QRadioButton,QGridLayout, QButtonGroup, QFileDialog
from PyQt5.QtCore import QTimer

proxies = {}
class secondWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setFixedSize(300,340)
        self.setWindowTitle("PROXY LOGIN")
        label = QLabel(self)
        label.setText("Proxy Username: ")
        newTextbox = QLineEdit(self)
        label1 = QLabel(self)
        label1.setText("Proxy Password: ")
        newTextbox1 = QLineEdit(self)
        layout.addWidget(label)
        layout.addWidget(newTextbox)
        layout.addWidget(label1)
        layout.addWidget(newTextbox1)
        submitButton = QPushButton("Save")
        submitButton.clicked.connect(lambda:proxySet(newTextbox.text(),newTextbox1.text(),self))
        layout.addWidget(submitButton)
        self.setLayout(layout)
    def closeSecondWindow_OpenGUI(self):
        print("closeSecondWindow_OpenGUI")
        self.close()
        GUI()

class GUI(QWidget):
    def __init__(self):
        super(GUI,self).__init__()
        print("inint gui")
        self.win = QWidget()
        self.win.setFixedSize(300,340)  
        self.win.setWindowTitle("BLS Request")
        label = QLabel(self.win)
        label.setText("Which BLS dataset would you like to format? ")
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()

        bg1 = QButtonGroup(self.win)

        rb1 = QRadioButton("Commodity", self.win)
        rb2 = QRadioButton("Industry", self.win)

        hbox2 = QHBoxLayout()
        bg2 = QButtonGroup(self.win)
        label1 = QLabel(self.win)
        label1.setText("Time Period Format: ")
        label1.adjustSize()
        rb4 = QRadioButton("Yearly", self.win)
        rb5 = QRadioButton("Quarterly", self.win)
        rb6 = QRadioButton("Monthly", self.win)
        rb6.setChecked(True)
        label3 = QLabel(self.win)
        label3.setText("Other Options: ")
        label3.adjustSize()

        # c1-c3 must be disabled if not monthly
        c1 = QCheckBox("Drop M13")
        c2 = QCheckBox("Format Time Period as YYYY-MM-01")
        c3 = QCheckBox("Add Seasonal Codes")
        rb4.toggled.connect(lambda:disableMonthly(c1,c2,c3))
        rb5.toggled.connect(lambda:disableMonthly(c1,c2,c3))
        rb6.toggled.connect(lambda:enableMonthly(c1,c2,c3))

        c4 = QCheckBox("Add Year-Over-Year Changes")
        c5 = QCheckBox("Add Percentage Changes between Periods")
        c6 = QCheckBox("Add Labels for Each Level")
        c7 = QCheckBox("Split ID values")
        c8 = QCheckBox("Format Dataframe Wide")
        hbox3 = QHBoxLayout()
        submitButton = QPushButton("Save")
        submitButton.setEnabled(False)
        submitButton.setCheckable(True)
        rb1.toggled.connect(lambda:submitButton.setEnabled(True))
        rb2.toggled.connect(lambda:submitButton.setEnabled(True))
        submitButton.toggled.connect(lambda:performDataFuncs(rb1, rb2,rb4.isChecked(),rb5.isChecked(),rb6.isChecked(),c1.isChecked(),c2.isChecked(),c3.isChecked(),c4.isChecked(),c5.isChecked(),c6.isChecked(),c7.isChecked(),c8.isChecked()))
        hbox3.addWidget(submitButton)
        bg1.addButton(rb1)
        bg1.addButton(rb2)

        bg2.addButton(rb4)
        bg2.addButton(rb5)
        bg2.addButton(rb6)

        hbox1.addWidget(rb1)
        hbox1.addWidget(rb2)

        hbox2.addWidget(rb4)
        hbox2.addWidget(rb5)
        hbox2.addWidget(rb6)

        vbox.addWidget(label)
        vbox.addLayout(hbox1)
        vbox.addWidget(label1)
        vbox.addLayout(hbox2)
        vbox.addWidget(label3)
        vbox.addWidget(c1)
        vbox.addWidget(c2)
        vbox.addWidget(c3)
        vbox.addWidget(c4)
        vbox.addWidget(c5)
        vbox.addWidget(c6)
        vbox.addWidget(c7)
        vbox.addWidget(c8)
        vbox.addLayout(hbox3)
        self.win.setLayout(vbox)
        self.win.show()

def proxySet(Username,password,self):
    self.close()
    proxy_ip = "127.0.0.1"
    proxy_port = "5000"
    httpFull = "http://" + Username + ":" + password + "@" + proxy_ip + ":" + proxy_port
    print(httpFull)
    proxies["http"] = httpFull
    self.closeSecondWindow_OpenGUI()

def disableMonthly(c1,c2,c3):
    c1.setEnabled(False)
    c2.setEnabled(False)
    c3.setEnabled(False)

def enableMonthly(c1,c2,c3):
    c1.setEnabled(True)
    c2.setEnabled(True)
    c3.setEnabled(True)

def performDataFuncs(wpRB, pcRB,yearly,quarterly,monthly,c1,c2,c3,c4,c5,c6,c7,c8):
    print("_____________________")
    print(proxies)
    if wpRB.isChecked(): 
        inputArr = [yearly,quarterly,monthly,c1,c2,c3,c4,c5,c6,c7,c8,proxies]
        data = commodity.wpProcessing(inputArr)
        openFileSaveAs(data)
    elif pcRB.isChecked():
        inputArr = [yearly,quarterly,monthly,c1,c2,c3,c4,c5,c6,c7,c8,proxies]
        data = industry.pcProcessing(inputArr)
        openFileSaveAs(data)

def openFileSaveAs(data):
    dialogue = QFileDialog()
    result = dialogue.getSaveFileName(dialogue, "Save File",filter="*csv")
    writePath = result[0] + ".csv"
    data.to_csv(writePath,index=False)

app = QApplication([])
if __name__ == "__main__":
    w = secondWindow()
    win = GUI()
    w.show()
    app.exec_()

   

