import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import serial

__author__ = 'Miguel Gutierrez'

serPort1 = "COM8"  # Stim
baudRate = 2000000

msg_bytes = ''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("calibracion.ui", self)

        self.spinBox_cal_p.valueChanged.connect(self.update_varp)
        self.spinBox_cal_n.valueChanged.connect(self.update_varn)
        self.spinBox_cal_pn.valueChanged.connect(self.update_varpn)

        # Show interface
        self.show()

    def update_varp(self):
        global msg_bytes

        canal = self.spinBox_ch.value()
        valor_pos = self.spinBox_cal_p.value()
        valor_neg = self.spinBox_cal_n.value()
        msg = str(canal) + ">" + str(valor_pos) + ">" + str(valor_neg) + ">"

        msg_bytes = str.encode(msg)
        self.update_var()

    def update_varn(self):
        global msg_bytes

        canal = self.spinBox_ch.value()
        valor_pos = self.spinBox_cal_p.value()
        valor_neg = self.spinBox_cal_n.value()
        msg = str(canal) + ">" + str(valor_pos) + ">" + str(valor_neg) + ">"

        msg_bytes = str.encode(msg)
        self.update_var()

    def update_varpn(self):
        global msg_bytes

        canal = self.spinBox_ch.value()
        valor_posneg = self.spinBox_cal_pn.value()
        msg = str(canal) + ">" + str(valor_posneg) + ">" + str(valor_posneg) + ">"

        msg_bytes = str.encode(msg)
        self.update_var()

    def update_var(self):
        global msg_bytes

        ser = serial.Serial()
        ser.port = serPort1
        ser.timeout = 1
        ser.baudrate = baudRate
        ser.xonxoff = 1

        try:
            ser.open()
        except Exception as e:
            print("Error open serial port: " + str(e) + " En -- read_serial --")
            exit()

        if ser.isOpen():
            try:
                ser.write(msg_bytes)
            except Exception as e1:
                print("Error communicating...: " + str(e1) + "En -- read_serial --")
        else:
            print("Cannot open serial port " + str(port) + "En -- read_serial --")
            exit()

        print("End Thread Acel data")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
