# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Estimulema.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(747, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 291, 41))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(15)
        font.setKerning(True)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(440, 10, 291, 31))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(15)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setCheckable(True)
        self.groupBox_2.setChecked(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.Freq_Lb_2 = QtWidgets.QLabel(self.centralwidget)
        self.Freq_Lb_2.setGeometry(QtCore.QRect(300, 240, 31, 31))
        self.Freq_Lb_2.setTextFormat(QtCore.Qt.AutoText)
        self.Freq_Lb_2.setObjectName("Freq_Lb_2")
        self.TherapyTimeSlider = QtWidgets.QSlider(self.centralwidget)
        self.TherapyTimeSlider.setGeometry(QtCore.QRect(20, 110, 261, 22))
        self.TherapyTimeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.TherapyTimeSlider.setObjectName("TherapyTimeSlider")
        self.Pw_Lb_3 = QtWidgets.QLabel(self.centralwidget)
        self.Pw_Lb_3.setGeometry(QtCore.QRect(300, 380, 31, 31))
        self.Pw_Lb_3.setTextFormat(QtCore.Qt.AutoText)
        self.Pw_Lb_3.setObjectName("Pw_Lb_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 361, 21))
        self.label_3.setObjectName("label_3")
        self.Pw_MinusBtn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Pw_MinusBtn_3.setGeometry(QtCore.QRect(110, 430, 75, 23))
        self.Pw_MinusBtn_3.setObjectName("Pw_MinusBtn_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 350, 361, 31))
        self.label_2.setObjectName("label_2")
        self.Pw_PlusBtn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Pw_PlusBtn_3.setGeometry(QtCore.QRect(20, 430, 75, 23))
        self.Pw_PlusBtn_3.setObjectName("Pw_PlusBtn_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 210, 361, 31))
        self.label.setObjectName("label")
        self.Freq_MinusBtn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.Freq_MinusBtn_2.setGeometry(QtCore.QRect(110, 290, 75, 23))
        self.Freq_MinusBtn_2.setObjectName("Freq_MinusBtn_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 470, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.PulseWidthSlider = QtWidgets.QSlider(self.centralwidget)
        self.PulseWidthSlider.setGeometry(QtCore.QRect(20, 390, 261, 22))
        self.PulseWidthSlider.setOrientation(QtCore.Qt.Horizontal)
        self.PulseWidthSlider.setObjectName("PulseWidthSlider")
        self.FreqSlider = QtWidgets.QSlider(self.centralwidget)
        self.FreqSlider.setGeometry(QtCore.QRect(20, 250, 261, 22))
        self.FreqSlider.setOrientation(QtCore.Qt.Horizontal)
        self.FreqSlider.setObjectName("FreqSlider")
        self.Freq_PlusBtn = QtWidgets.QPushButton(self.centralwidget)
        self.Freq_PlusBtn.setGeometry(QtCore.QRect(20, 290, 75, 23))
        self.Freq_PlusBtn.setObjectName("Freq_PlusBtn")
        self.Tht_Lb = QtWidgets.QLabel(self.centralwidget)
        self.Tht_Lb.setGeometry(QtCore.QRect(300, 100, 31, 31))
        self.Tht_Lb.setTextFormat(QtCore.Qt.AutoText)
        self.Tht_Lb.setObjectName("Tht_Lb")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(20, 40, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.TheT_PlusBtn = QtWidgets.QPushButton(self.centralwidget)
        self.TheT_PlusBtn.setGeometry(QtCore.QRect(20, 150, 75, 23))
        self.TheT_PlusBtn.setObjectName("TheT_PlusBtn")
        self.TheT_MinusBtn = QtWidgets.QPushButton(self.centralwidget)
        self.TheT_MinusBtn.setGeometry(QtCore.QRect(110, 150, 75, 23))
        self.TheT_MinusBtn.setObjectName("TheT_MinusBtn")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(440, 210, 361, 31))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(440, 350, 361, 31))
        self.label_6.setObjectName("label_6")
        self.FreqSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.FreqSlider_2.setGeometry(QtCore.QRect(440, 250, 261, 22))
        self.FreqSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.FreqSlider_2.setObjectName("FreqSlider_2")
        self.Freq_MinusBtn_3 = QtWidgets.QPushButton(self.centralwidget)
        self.Freq_MinusBtn_3.setGeometry(QtCore.QRect(530, 290, 75, 23))
        self.Freq_MinusBtn_3.setObjectName("Freq_MinusBtn_3")
        self.Tht_Lb_2 = QtWidgets.QLabel(self.centralwidget)
        self.Tht_Lb_2.setGeometry(QtCore.QRect(720, 100, 31, 31))
        self.Tht_Lb_2.setTextFormat(QtCore.Qt.AutoText)
        self.Tht_Lb_2.setObjectName("Tht_Lb_2")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(440, 40, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.Pw_MinusBtn_4 = QtWidgets.QPushButton(self.centralwidget)
        self.Pw_MinusBtn_4.setGeometry(QtCore.QRect(530, 430, 75, 23))
        self.Pw_MinusBtn_4.setObjectName("Pw_MinusBtn_4")
        self.TherapyTimeSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.TherapyTimeSlider_2.setGeometry(QtCore.QRect(440, 110, 261, 22))
        self.TherapyTimeSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.TherapyTimeSlider_2.setObjectName("TherapyTimeSlider_2")
        self.PulseWidthSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.PulseWidthSlider_2.setGeometry(QtCore.QRect(440, 390, 261, 22))
        self.PulseWidthSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.PulseWidthSlider_2.setObjectName("PulseWidthSlider_2")
        self.Pw_Lb_4 = QtWidgets.QLabel(self.centralwidget)
        self.Pw_Lb_4.setGeometry(QtCore.QRect(720, 380, 31, 31))
        self.Pw_Lb_4.setTextFormat(QtCore.Qt.AutoText)
        self.Pw_Lb_4.setObjectName("Pw_Lb_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(440, 80, 361, 21))
        self.label_5.setObjectName("label_5")
        self.Pw_PlusBtn_4 = QtWidgets.QPushButton(self.centralwidget)
        self.Pw_PlusBtn_4.setGeometry(QtCore.QRect(440, 430, 75, 23))
        self.Pw_PlusBtn_4.setObjectName("Pw_PlusBtn_4")
        self.TheT_MinusBtn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.TheT_MinusBtn_2.setGeometry(QtCore.QRect(530, 150, 75, 23))
        self.TheT_MinusBtn_2.setObjectName("TheT_MinusBtn_2")
        self.Freq_Lb_3 = QtWidgets.QLabel(self.centralwidget)
        self.Freq_Lb_3.setGeometry(QtCore.QRect(720, 240, 31, 31))
        self.Freq_Lb_3.setTextFormat(QtCore.Qt.AutoText)
        self.Freq_Lb_3.setObjectName("Freq_Lb_3")
        self.TheT_PlusBtn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.TheT_PlusBtn_2.setGeometry(QtCore.QRect(440, 150, 75, 23))
        self.TheT_PlusBtn_2.setObjectName("TheT_PlusBtn_2")
        self.Freq_PlusBtn_2 = QtWidgets.QPushButton(self.centralwidget)
        self.Freq_PlusBtn_2.setGeometry(QtCore.QRect(440, 290, 75, 23))
        self.Freq_PlusBtn_2.setObjectName("Freq_PlusBtn_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 470, 101, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 747, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Estimulema"))
        self.groupBox.setTitle(_translate("MainWindow", "Channel 1"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Channel 2"))
        self.Freq_Lb_2.setText(_translate("MainWindow", "00"))
        self.Pw_Lb_3.setText(_translate("MainWindow", "00"))
        self.label_3.setText(_translate("MainWindow", "Therapy time"))
        self.Pw_MinusBtn_3.setText(_translate("MainWindow", "-"))
        self.label_2.setText(_translate("MainWindow", "Pulse width"))
        self.Pw_PlusBtn_3.setText(_translate("MainWindow", "+"))
        self.label.setText(_translate("MainWindow", "Frequency"))
        self.Freq_MinusBtn_2.setText(_translate("MainWindow", "-"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.Freq_PlusBtn.setText(_translate("MainWindow", "+"))
        self.Tht_Lb.setText(_translate("MainWindow", "00"))
        self.radioButton.setText(_translate("MainWindow", "Ramp"))
        self.TheT_PlusBtn.setText(_translate("MainWindow", "+"))
        self.TheT_MinusBtn.setText(_translate("MainWindow", "-"))
        self.label_4.setText(_translate("MainWindow", "Frequency"))
        self.label_6.setText(_translate("MainWindow", "Pulse width"))
        self.Freq_MinusBtn_3.setText(_translate("MainWindow", "-"))
        self.Tht_Lb_2.setText(_translate("MainWindow", "00"))
        self.radioButton_2.setText(_translate("MainWindow", "Ramp"))
        self.Pw_MinusBtn_4.setText(_translate("MainWindow", "-"))
        self.Pw_Lb_4.setText(_translate("MainWindow", "00"))
        self.label_5.setText(_translate("MainWindow", "Therapy time"))
        self.Pw_PlusBtn_4.setText(_translate("MainWindow", "+"))
        self.TheT_MinusBtn_2.setText(_translate("MainWindow", "-"))
        self.Freq_Lb_3.setText(_translate("MainWindow", "00"))
        self.TheT_PlusBtn_2.setText(_translate("MainWindow", "+"))
        self.Freq_PlusBtn_2.setText(_translate("MainWindow", "+"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

