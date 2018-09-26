import sys
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import serial
import numpy as np
from drawnow import *
import atexit
import threading
import time

values = []

plt.ion()
cnt = 0
control = False

__author__ = 'Miguel Gutierrez'

# Original ports
serPort1 = "COM19"  # Stim
baudRate = 2000000
file_name_out_lc = ""

#serialArduino = serial.Serial(serPort1, baudRate)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("Load_cell.ui", self)

        # Connect up the buttons.
        self.pushButton_s.clicked.connect(self.btn_s)
        self.pushButton_f.clicked.connect(self.btn_f)
        self.pushButton_pad.clicked.connect(self.btn_pad)
        self.letf = 10
        self.top = 100
        self.width = 312
        self.height = 112

        self.set_position()

        self.show()

    def set_position(self):
        self.setGeometry(self.letf, self.top, self.width, self.height)

    def btn_s(self):
        global control
        control = True
        start_capture()

    def btn_f(self):
        global control
        control = False
        print("Ends data capture")
        #exit()

    def btn_pad(self):
        ## file_name_out_lc = "load_cell Mon 24 21h50.txt"
        ## file_name_out_lc = "load_cell Mon 24 21h50.txt"
        plot_all_data(file_name_out_lc)

def plotValues():
    plt.title('Serial value from Arduino')
    plt.grid(True)
    plt.ylabel('Kg')
    plt.xlabel('samples * 100us')
    plt.plot(values, 'rx-', label='Kilos variation')
    plt.legend(loc='upper right')


def doAtExit():
    serialArduino.close()
    print("Close serial")
    print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))


def plot_data(port, baud):
    global file_name_out_lc

    atexit.register(doAtExit)

    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baud
    ser.timeout = 1
    ser.xonxoff = 1

    try:
        ser.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + "En -- plot_data --")
        print("Possibly the serial port is already open")
        exit()

    ini = 's'
    ini_b = str.encode(ini)

    hora = time.strftime("%H")
    n_dia = time.strftime("%a")
    dia = time.strftime("%d")
    mm = time.strftime("%M")
    file_name_out_lc = 'load_cell ' + n_dia + ' ' + dia + ' ' + hora + 'h' + mm + '.txt'
    load_cell_save = open(file_name_out_lc, 'w')

    # pre-load dummy data
    for i in range(0, 100):
        values.append(0)

    if ser.isOpen():
        plt.figure(1)
        try:
            ser.write(ini_b) ## manda el msng
            while control is True:
                c = ser.readline()
                if len(c) > 0:
                    str_msn = c.decode("utf-8")
                    str_msn = str_msn.rstrip()
                    values.append(float(str_msn))
                    load_cell_save.write(str_msn)
                    load_cell_save.write("\n")
                    values.pop(0)
                    drawnow(plotValues)
        except Exception as e1:
            print("Error communicating...: " + str(e1) + " En -- plot data while --")

        if control is False:
            ini = 'f'
            ini_b = str.encode(ini)
            ser.write(ini_b)  ## manda el msng
            ser.close()
            load_cell_save.close()
            plt.close(1)


def plot_all_data(file):
    try:
        data = np.loadtxt(file)
    except Exception as e:
        print("Error: " + str(e) + " in --" + file + "-- file")
        exit()

    n = len(data)

    plt.figure(2)
    t = np.arange(0, n)
    plt.title('Serial value from Arduino')
    plt.grid(True)
    plt.ylabel('Kg')
    plt.xlabel('samples * 100us')
    plt.plot(t, data, 'b', label='Kilogram values')
    plt.legend(loc=2)
    plt.show(2)


# Create two threads as follows
def start_capture():
    global serPort1, baudRate

    try:
        t1 = threading.Thread(target=plot_data, args=(serPort1, baudRate))
        t1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t1.start()

    except Exception as e1:
        print("Error: unable to start thread 1" + str(e1))


def exit_program_and_stim():
    global start_receiver

    start_receiver = False
    print("Aplication closed, Stop Stimulation")
    ex.btn_stop_stim()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(exit_program_and_stim)
    ex = MainWindow()
    sys.exit(app.exec_())
