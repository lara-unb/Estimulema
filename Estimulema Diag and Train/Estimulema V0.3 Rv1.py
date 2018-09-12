import sys
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import serial
import threading
import numpy as np
import time
from scipy.signal import butter, lfilter, medfilt

__author__ = 'Miguel Gutierrez'

# Original ports
serPort1 = "COM14"
serPort2 = "COM13"

# Ports for teste
# serPort1 = "COM8"  # Stim
# serPort2 = "COM3"  # Accel


baudRate = 2000000

arrayt = []
arrayt2 = []
file_name_out_s = ''
file_name_out_a = ''

rh_acx = []
rh_acy = []
rh_acz = []
cr_acx = []
cr_acy = []
cr_acz = []

cont_fig = 1
plot_show = True
sel_test = True
start_receiver = False

# lock to serialize console output
lock = threading.Lock()

# lock to serialize console output
start = False
start_thread_a = False
start_thread_s = False

rh = False  # activate test
cr = False  # activate test
s_ch1 = False  # Start Channel 1  = true
s_ch2 = False  # Start Channel 2  = true
s_c = False  # Start capture
upd = False  # update value
ctr_upd = 0
stop_chx = True

solo_mode = 0  # to control test 0 - Open communication !-! 1 Just print data
# to change the name os stim and acel file
# 0 stim_(rh and rh) and acel_(rh and rh) in .txt
# 1 stim_(rh and rh) and acel_(rh and rh) plus data .txt
plot_xyz = False
name_file = False
start_tread = True

msg_bytes = ''
limit_ma_ini = 0
limit_ma_fin = 0
limit_pw = 0
limit_start = 0  # To count the final message

# Stim parameters
ts = 0
freq = 0
pw = 0
msg = ""

cs = ">"


# First String communication - global variables
class stim_param_channel:
    def __init__(self):
        pass


# For channel 1
ch1 = stim_param_channel()
ch1.tn = 0  # Save de Frequency value
ch1.tf = 0  # Save de PulseWidth value
ch1.ri = 0  # Save de TOff value
ch1.rf = 0  # Save de TOff value
ch1.ma = 0  # Save de Current value

# For channel 2
ch2 = stim_param_channel()
ch2.tn = 0  # Save de Frequency value
ch2.tf = 0  # Save de PulseWidth value
ch2.ri = 0  # Save de TOff value
ch2.rf = 0  # Save de TOff value
ch2.ma = 0  # Save de Current value


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("Estimulema V0.3 Rv1.ui", self)

        # Connect up the buttons.
        self.pushButton_rh.clicked.connect(self.btn_start_rh)
        self.pushButton_cr.clicked.connect(self.btn_start_cr)
        self.pushButton_sp.clicked.connect(self.btn_stop_stim)
        self.pushButton_ch1.clicked.connect(self.btn_start_ch1)
        self.pushButton_ch2.clicked.connect(self.btn_start_ch2)
        self.pushButton_fil_plot.clicked.connect(self.btn_fil_plot)

        # for two channels
        self.pushButton_ch1_ch2.clicked.connect(self.btn_start_ch1_ch2)

        # Stop buttons
        self.pushButton_sp_ch1.clicked.connect(self.btn_stop_ch1)
        self.pushButton_sp_ch2.clicked.connect(self.btn_stop_ch2)

        # limits for tests
        self.spinBox_limit_ini_mA.valueChanged.connect(self.update_var)
        self.spinBox_limit_fin_mA.valueChanged.connect(self.update_var)
        self.spinBox_limit_pW.valueChanged.connect(self.update_var)

        # for general parameters
        self.spinBox_ts.valueChanged.connect(self.update_var)
        self.spinBox_f.valueChanged.connect(self.update_var)
        self.spinBox_pw.valueChanged.connect(self.update_var)

        # for channel 1
        self.spinBox_tn_1.valueChanged.connect(self.update_var)
        self.spinBox_tf_1.valueChanged.connect(self.update_var)
        self.spinBox_ri_1.valueChanged.connect(self.ramp_check)
        self.spinBox_rf_1.valueChanged.connect(self.ramp_check)
        self.spinBox_ma_1.valueChanged.connect(self.btn_change_ma1)

        # for channel 2
        self.spinBox_tn_2.valueChanged.connect(self.update_var)
        self.spinBox_tf_2.valueChanged.connect(self.update_var)
        self.spinBox_ri_2.valueChanged.connect(self.ramp_check)
        self.spinBox_rf_2.valueChanged.connect(self.ramp_check)
        self.spinBox_ma_2.valueChanged.connect(self.btn_change_ma2)

        # Show interface
        self.show()

    # buttons ---------------------------------------------------------------
    def btn_start_rh(self):
        global rh, cr, s_c, start, limit_start, s_ch1, s_ch2
        global start_thread_a, start_thread_s, msg_bytes, solo_mode

        rh = True
        start_thread_s = start_thread_a = True  # To control the threads
        cr = s_c = s_ch1 = s_ch2 = start = False

        self.spinBox_ma_1.setValue(0)
        self.spinBox_ma_2.setValue(0)
        self.update_var()

        if solo_mode == 0:
            start_test()

        self.lineEdit_terminal.setText("Start capture data for Rh -- Stim and Acel --")

    def btn_start_cr(self):
        global rh, cr, s_c, start, limit_pw, s_ch1, s_ch2
        global start_thread_a, start_thread_s

        cr = True
        rh = s_c = s_ch1 = s_ch2 = start = False
        start_thread_s = start_thread_a = True  # To control the threads

        self.spinBox_ma_1.setValue(0)
        self.spinBox_ma_2.setValue(0)
        self.update_var()

        if solo_mode == 0:
            start_test()

        self.lineEdit_terminal.setText("Start capture data for Cr -- Stim and Acel --")

    def btn_start_ch1(self):
        global s_ch1, s_c, start, s_ch2, ctr_upd, stop_chx, rh, cr

        s_ch1 = start = stop_chx = True
        s_c = s_ch2 = rh = cr = False

        self.update_var()
        s_c = s_ch2 = rh = cr = start = False

    def btn_start_ch2(self):
        global s_ch2, s_c, start, s_ch1, ctr_upd, stop_chx, rh, cr

        s_ch2 = start = stop_chx = True
        s_c = s_ch1 = rh = cr = False

        self.update_var()
        s_c = s_ch2 = rh = cr = start = False

    def btn_start_ch1_ch2(self):
        global s_ch2, s_c, start, s_ch1, ctr_upd, stop_chx, rh, cr

        s_ch2 = s_ch1 = start = stop_chx = True
        s_c = rh = cr = False

        self.update_var()
        s_c = s_ch2 = rh = cr = start = False
        self.btn_stop_stim()

    def btn_stop_stim(self):
        global rh, cr, s_ch1, s_ch2, s_c, start, upd, stop_chx, start_tread

        upd = False
        start = True
        start_tread = True

        rh = cr = s_ch1 = s_ch2 = False
        s_c = stop_chx = upd = True

        self.spinBox_ma_1.setValue(0)
        self.spinBox_ma_2.setValue(0)
        self.update_var()
        upd = start = False

    def btn_stop_ch1(self):
        global upd, start, stop_chx
        upd = stop_chx = False
        start = True

        self.spinBox_ma_1.setValue(0)
        self.update_var()
        upd = start = False

    def btn_stop_ch2(self):
        global upd, start, stop_chx
        upd = stop_chx = False
        start = True

        self.spinBox_ma_2.setValue(0)
        self.update_var()
        upd = start = False

    def btn_change_ma1(self):
        global upd, start, stop_chx

        if start is True:
            upd = True

        if stop_chx is True:
            self.update_var()
        else:
            stop_chx = True

    def btn_change_ma2(self):
        global start, upd, stop_chx

        if start is True:
            upd = True

        if stop_chx is True:
            self.update_var()
        else:
            stop_chx = True

    @staticmethod
    def btn_fil_plot():
        plot_and_filt()

    def ramp_check(self):
        global ch1, ch2

        ch1.ri = self.spinBox_ri_1.value()
        ch1.rf = self.spinBox_rf_1.value()
        ch2.ri = self.spinBox_ri_2.value()
        ch2.rf = self.spinBox_rf_2.value()

        ch1.tn = self.spinBox_tn_1.value()
        ch2.tn = self.spinBox_tn_2.value()

        # parameters for channel 1 = 4
        if (ch1.ri + ch1.rf) > ch1.tn:
            self.message_box(1)

        # parameters for channel 1 = 4
        if (ch2.ri + ch2.rf) > ch2.tn:
            self.message_box(2)

        self.update_var()

    def upd_terminal(self, msn):
        self.lineEdit_terminal.setText(msn)

    def upd_val_rh(self, new_val_rh):
        self.spinBox_limit_ini_mA.setValue(new_val_rh)
        self.spinBox_limit_fin_mA.setValue(new_val_rh)

    def update_var(self):
        global limit_ma_ini, limit_ma_fin, limit_pw, ch1, ch2, ts, freq, pw, msg, cs
        global rh, cr, s_ch1, s_ch2, s_c, msg_bytes, upd, ctr_upd, start

        # general parameters
        ts = self.spinBox_ts.value()
        freq = self.spinBox_f.value()
        pw = self.spinBox_pw.value()

        # for channel 1
        ch1.tn = self.spinBox_tn_1.value()
        ch1.tf = self.spinBox_tf_1.value()
        ch1.ri = self.spinBox_ri_1.value()
        ch1.rf = self.spinBox_rf_1.value()
        ch1.ma = self.spinBox_ma_1.value()

        # for channel 2
        ch2.tn = self.spinBox_tn_2.value()
        ch2.tf = self.spinBox_tf_2.value()
        ch2.ri = self.spinBox_ri_2.value()
        ch2.rf = self.spinBox_rf_2.value()
        ch2.ma = self.spinBox_ma_2.value()

        # limits for tests
        limit_ma_ini = self.spinBox_limit_ini_mA.value()
        limit_ma_fin = self.spinBox_limit_fin_mA.value()
        limit_pw = self.spinBox_limit_pW.value()

        # general parameters = 3
        msg = str(ts) + cs + str(freq) + cs + str(pw)

        msg = msg + cs + str(ch1.tn) + cs + str(ch1.tf) + cs + str(ch1.ri) + cs + str(ch1.rf) + cs + str(ch1.ma)

        # parameters for channel 2 = 4
        msg = msg + cs + str(ch2.tn) + cs + str(ch2.tf) + cs + str(ch2.ri) + cs + str(ch2.rf) + cs + str(ch2.ma)

        # parameters for tests = 2
        msg = msg + cs + str(limit_ma_ini) + cs + str(limit_ma_fin) + cs + str(limit_pw) + cs

        # msg of activation control = 4
        if rh is True:
            rh_str = "1"
        else:
            rh_str = "0"

        if cr is True:
            cr_str = "1"
        else:
            cr_str = "0"

        if s_ch1 is True:
            s_ch1_str = "1"
        else:
            s_ch1_str = "0"

        if s_ch2 is True:
            s_ch2_str = "1"
        else:
            s_ch2_str = "0"

        if s_c is True:
            s_c_str = "0"
        else:
            s_c_str = "1"

        if upd is True:
            upd_str = "1"
        else:
            upd_str = "0"

        msg = msg + rh_str + cs + cr_str + cs + s_ch1_str + cs + s_ch2_str + cs + s_c_str + cs + upd_str + cs

        if ctr_upd == 0 and start is True:
            upd = True
            ctr_upd = 2

        self.lineEdit_terminal.setText(msg)
        print("Para enviar: " + msg)
        msg_bytes = str.encode(msg)

        if start is True:
            # print("Change value")
            stim_training()
        elif solo_mode == 0 and start_thread_a is True and start_thread_s is True:
            print("Excitability tests start")
        else:
            print("Solo mode:   " + msg + "<<<<")

    def message_box(self, sel):
        global msg
        msg = ""
        if sel == 1:
            QMessageBox.about(self, "Error", "Ramp value erro")
            if ch1.ri > ch1.rf:
                ch1.ri = ch1.ri - 0.5
                self.spinBox_ri_1.setValue(ch1.ri)
            else:
                ch1.rf = ch1.rf - 0.5
                self.spinBox_rf_1.setValue(ch1.rf)

        if sel == 2:
            QMessageBox.about(self, "Error", "Ramp value erro")
            if ch2.ri > ch2.rf:
                ch2.ri = ch2.ri - 0.5
                self.spinBox_ri_2.setValue(ch2.ri)
            else:
                ch2.rf = ch2.rf - 0.5
                self.spinBox_rf_2.setValue(ch2.rf)




        """
        m.setIcon(QMessageBox.Critical)
        m.setText("Error")
        m.setInformativeText(e)
        m.setWindowTitle("Error")"""


def read_serial(port, baud):
    global msg_bytes, arrayt
    global start_thread_s

    arrayt = []  # array for stim data

    ser = serial.Serial()
    ser.port = port
    ser.timeout = 1
    ser.baudrate = baud
    ser.xonxoff = 1

    try:
        ser.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + " En -- read_serial --")
        exit()

    if ser.isOpen():
        try:
            while start_thread_s is False:
                pass

            ser.write(msg_bytes)
            print("Start capture for Stim data")
            while start_thread_s is True:
                c = ser.readline()
                with lock:
                    if len(c) > 0:
                        str_msn = c.decode("utf-8")
                        str_msn = str_msn.rstrip()
                        print(str_msn)
                        if str_msn == '>':
                            start_thread_s = False
                            print("End capture about Stim data")
                        else:
                            arrayt.append(str_msn)
            ser.close()

        except Exception as e1:
            print("Error communicating...: " + str(e1) + "En -- read_serial --")

    else:
        print("Cannot open serial port " + str(port) + "En -- read_serial --")
        exit()

    save_data()  # Thread for acel data
    print("End Thread Acel data")


def read_serial2(port, baud):
    global msg_bytes, start, arrayt2
    global start_thread_a

    arrayt2 = []  # Array for acel data

    ser2 = serial.Serial()
    ser2.port = port
    ser2.timeout = 1
    ser2.baudrate = baud
    ser2.xonxoff = 1

    try:
        ser2.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + " En -- read_serial2 --")
        exit()

    if ser2.isOpen():
        try:
            while start_thread_a is False:
                pass

            ser2.write(msg_bytes)
            print("Start capture for Accelerometer data")
            while start_thread_a:
                c = ser2.readline()
                with lock:
                    if len(c) > 0:
                        str_msn = c.decode("utf-8")
                        str_msn = str_msn.rstrip()
                        print(str_msn)
                        if str_msn == '>':
                            start_thread_a = False
                            print("End capture about Accelerometer data")
                        else:
                            arrayt2.append(str_msn)

            ser2.close()

        except Exception as e1:
            print("Error communicating...: " + str(e1) + " En -- read_serial2 --")

    else:
        print("Cannot open serial port " + str(port) + " En -- read_serial2 --")
        exit()

    save_data2()  # Thread for acel data
    print("End Thread Acel data2")


def save_data():
    global arrayt, rh, cr, name_file, file_name_out_s

    if rh is True:
        if name_file is True:
            hora = time.strftime("%H")
            n_dia = time.strftime("%a")
            dia = time.strftime("%d")
            mm = time.strftime("%M")
            file_name_out_s = 'stim_r ' + n_dia + ' ' + dia + ' ' + hora + 'h' + mm + '.txt'
        else:
            file_name_out_s = 'stim_r.txt'
    elif cr is True:
        if name_file is True:
            hora = time.strftime("%H")
            n_dia = time.strftime("%a")
            dia = time.strftime("%d")
            mm = time.strftime("%M")
            file_name_out_s = 'stim_c ' + n_dia + ' ' + dia + ' ' + hora + 'h' + mm + '.txt'
        else:
            file_name_out_s = 'stim_c.txt'

    stim = open(file_name_out_s, 'w')

    for x in arrayt:
        if rh is True:
            stim.write(x)
            stim.write("\n")
        elif cr is True:
            stim.write(x)
            stim.write("\n")
        # print(x)

    stim.close()

    print("End generation of Stim file")
    ex.upd_terminal("End generation of Stim file")


def save_data2():
    global arrayt2, rh, cr, cont_fig, plot_show, sel_test, file_name_out_a
    # global rh_acx, rh_acy, rh_acz, cr_acx, cr_acy, cr_acz
    global name_file

    if rh is True:
        if name_file is True:
            hora = time.strftime("%H")
            n_dia = time.strftime("%a")
            dia = time.strftime("%d")
            mm = time.strftime("%M")
            file_name_out_a = 'acel_r ' + n_dia + ' ' + dia + ' ' + hora + 'h' + mm + '.txt'
        else:
            file_name_out_a = 'acel_r.txt'
    elif cr is True:
        if name_file is True:
            hora = time.strftime("%H")
            n_dia = time.strftime("%a")
            dia = time.strftime("%d")
            mm = time.strftime("%M")
            file_name_out_a = 'acel_c ' + n_dia + ' ' + dia + ' ' + hora + 'h' + mm + '.txt'
        else:
            file_name_out_a = 'acel_c.txt'

    acel = open(file_name_out_a, 'w')

    for x in arrayt2:
        if rh is True:
            acel.write(x)
            acel.write("\n")
            # save array for filter and plot
            # y = np.array(x.rstrip().split(';')).astype(int)
            # rh_acx.append(int(y[1]))
            # rh_acy.append(int(y[2]))
            # rh_acz.append(int(y[3]))
            sel_test = True
        elif cr is True:
            acel.write(x)
            acel.write("\n")
            # save array for filter and plot
            # y = np.array(x.rstrip().split(';')).astype(int)
            # cr_acx.append(y[1])
            # cr_acy.append(y[2])
            # cr_acz.append(y[3])
            sel_test = False
        # print(x)

    acel.close()

    print("End generation of Acel file")
    ex.upd_terminal("End generation of Acel file, (Plot enable)")


def stim_training():
    global serPort1, serPort2, baudRate, msg_bytes, start, start_tread

    if start_tread is True:
        start_tread = False
        try:
            t3 = threading.Thread(target=read_while_stim, args=(serPort2, baudRate))
            t3.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            t3.start()

        except Exception as e1:
            print("Error: unable to start thread 1" + str(e1))

    ser = serial.Serial()
    ser.port = serPort1
    ser.timeout = 1
    ser.baudrate = baudRate
    ser.xonxoff = 1

    try:
        ser.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + "En -- Stim_training -- ")
        exit()

    if ser.isOpen():
        try:
            ser.write(msg_bytes)

        except Exception as e1:
            print("Error communicating...: " + str(e1) + " En -- Stim_training --")


def read_while_stim(port, baud):
    global start, start_receiver, ts, start_tread

    start_receiver = True
    cont = 0

    ser = serial.Serial()
    ser.port = port
    ser.timeout = 1
    ser.baudrate = baud
    ser.xonxoff = 1

    try:
        ser.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + "En -- read_while_stim --")
        print("Possibly the serial port is already open")
        exit()

    if ser.isOpen():
        try:
            print("Count Minutes")
            print("Remaining minutes: " + str(ts - cont))
            ex.upd_terminal("Remaining minutes: " + str(ts - cont))
            while start_receiver is True:
                c = ser.readline()
                if len(c) > 0:
                    str_msn = c.decode("utf-8")
                    str_msn = str_msn.rstrip()
                    print(str_msn)
                    if str_msn == "f":
                        start_receiver = False
                        print("End therapy time")
                        ex.upd_terminal("End therapy time")
                    else:
                        cont = cont + 1
                        print("Remaining minutes: " + str(ts - cont))
                        ex.upd_terminal("Remaining minutes: " + str(ts - cont))

            ser.close()
            start_tread = True
            ex.upd_terminal("End therapy time")

        except Exception as e1:
            print("Error communicating...: " + str(e1) + " En -- read_while_stim --")

        ex.upd_terminal("Ends Stimulation ...")


# Create two threads as follows
def start_test():
    global serPort1, serPort2, baudRate

    try:
        t1 = threading.Thread(target=read_serial, args=(serPort1, baudRate))
        t1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t1.start()

    except Exception as e1:
        print("Error: unable to start thread 1" + str(e1))

    try:
        t1 = threading.Thread(target=read_serial2, args=(serPort2, baudRate))
        t1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t1.start()
    except Exception as e1:
        print("Error: unable to start thread 2" + str(e1))


def plot_and_filt():
    global arrayt, arrayt2, rh, cr, plot_xyz, file_name_out_a, file_name_out_s

    global rh_acx, rh_acy, rh_acz, cr_acx, cr_acy, cr_acz

    # aqui testo las saludas
    # rh = False
    # rh = True

    if rh is True:
        print("Vamos plotar para Reobase")
        cr = False
    else:
        cr = True
        print("Vamos plotar para Cronaxia")

    file = ""

    if rh is True:
        file = 'acel_r.txt'
        # file = file_name_out_a
    elif cr is True:
        file = 'acel_c.txt'
        # file = file_name_out_s

    try:
        data = np.loadtxt(file, delimiter=';')
    except Exception as e:
        print("Error: " + str(e) + " in --" + file + "-- file")
        exit()

    # data = np.loadtxt(file, delimiter=';')
    # data = np.array(arrayt.rstrip().split(';')).astype(int)

    # data of signal
    eje_x = data[:, 1]
    eje_y = data[:, 2]
    eje_z = data[:, 3]
    signal_pulse = data[:, 4]

    n = len(signal_pulse)

    plt.figure()
    t = np.arange(0, n)

    # Normalize the axis from digital to g(m/s^2)
    bits_dac = 65536  # 2 ^ 16
    eje_x = eje_x / bits_dac
    eje_y = eje_y / bits_dac
    eje_z = eje_z / bits_dac

    eje_x2 = eje_x ** 2
    eje_y2 = eje_y ** 2
    eje_z2 = eje_z ** 2

    xyz = eje_x2 + eje_y2 + eje_z2
    # Magnitude of the resulting vector
    eje_xyz = np.sqrt(xyz)

    # take 500 samples to calculate the average value
    in_sxyz = eje_xyz[:500]
    med_xyz = np.mean(in_sxyz)
    print("valor medio: " + str(med_xyz))
    std_xyz = np.std(in_sxyz)
    print("La desviacion standard es: " + str(std_xyz))

    # Threshold calculation based on standard deviations
    num_std = 4
    thsdxyz = num_std * std_xyz
    lin_thsdxyz = np.ones((n, 1)) * (med_xyz + thsdxyz)

    # Plot the threshold signal
    plt.plot(t, lin_thsdxyz, 'b')
    if plot_xyz is True:
        plt.plot(t, eje_x, 'b')
        plt.plot(t, eje_y, 'b')
        plt.plot(t, eje_z, 'b')
    #  plt.plot(t, eje_xyz, 'b', linewidth=0.5)

    # Parameters used in the filter
    cut_off = 30
    fs = 1000
    order = 10

    acxyz_fil = butter_lowpass_filter(eje_xyz, cut_off, fs, order)
    plt.plot(t, acxyz_fil, 'r', linewidth=1)

    xyz_mf = medfilt(eje_xyz, 5)
    plt.plot(t, xyz_mf, 'y', linewidth=1)

    val_max = np.max(acxyz_fil)
    print("Valor maximo del vector: " + str(val_max))
    # signal_pulse = signal_pulse * val_max

    # read stim data
    if rh is True:
        file = 'stim_r.txt'
    elif cr is True:
        file = 'stim_c.txt'

    try:
        data_s = np.loadtxt(file, delimiter=';')
    except Exception as e:
        print("Error: " + str(e) + " in --" + file + "-- file")
        print("Please review the file and check the internal format")
        exit()

    # data_s = np.loadtxt(file, delimiter=';')
    data_ma = data_s[:, 1]
    max_ma = np.max(data_ma)

    # split stimulation signal
    div = val_max / max_ma
    div_signal = div
    new_stim_signal = np.ones((n, 1))
    c1 = 0

    if cr is True:
        div_signal = val_max

    for i in range(n):
        # contar milies
        if signal_pulse[i] == 1:
            c1 = 1
            new_stim_signal[i] = signal_pulse[i] * div_signal
        else:
            new_stim_signal[i] = 0

        if c1 == 1 and signal_pulse[i] == 0:
            if rh is True:
                div_signal = div_signal + div
            elif cr is True:
                div_signal = val_max
            c1 = 0

    # Stimulation signal
    # plt.plot(t, signal_pulse[i], 'g')
    plt.plot(t, new_stim_signal, 'g')

    # plt.title = 'Acceleration magnitude resulting from the XYZ axis'
    # plt.xlabel = 'time (s)'
    # plt.ylabel = 'g(m/s^2)'

    # Spike detection
    th = med_xyz + thsdxyz

    if rh is True:
        for j in range(500, n):
            # contar milies
            val_ac = acxyz_fil[j]
            if val_ac >= th:
                print("Indice de interceptacion: " + str(j))
                val_int = new_stim_signal[j]
                val_int = int(val_int / div)
                print("Div miliamps: " + str(val_int))
                if val_int > 0:
                    # val_int = val_int + 1
                    break
    elif cr is True:
        c_dx = 0  # contador de delta x
        c_ind = []  # index count
        for i in range(n):
            if signal_pulse[i] == 1:
                c_dx = 1
            if signal_pulse[i] == 0 and c_dx == 1:
                # c_ind[i] = 0
                print("sumando")

        for j in range(3000, n):
            val_ac = acxyz_fil[j]
            if val_ac >= th:
                print("Indice de interceptacion: " + str(j))
                val_int = new_stim_signal[j]
                val_int = int(val_int / div)
                print("Div miliamps: " + str(val_int))
                if val_int > 0:
                    # val_int = val_int + 1
                    break

    print("Ends plot desde archivo para aceleracion")
    val_int = 4;
    ex.upd_val_rh(val_int * 2)
    ex.upd_terminal("Valor de Reobase: " + str(val_int) + " Setando: " + str(val_int * 2))
    plt.show()


def butter_lowpass(cut_off, fs, order=5):
    nyq = 0.5 * fs
    normal_cut_off = cut_off / nyq
    b, a = butter(order, normal_cut_off, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cut_off, fs, order=5):
    b, a = butter_lowpass(cut_off, fs, order=order)
    y = lfilter(b, a, data)
    return y


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
