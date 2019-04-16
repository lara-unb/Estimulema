import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import serial
import threading
import time
import numpy as np
from scipy.signal import butter, lfilter
from os import remove
import matplotlib.pyplot as plt

__author__ = 'Miguel Gutierrez'

# Warning --- Setup configurations
teste_training = 0  # 0 - teste de exitabilidade **** 1 - Training
t_s = 1  # 0 - teste simple **** 1 - teste con estimulador

if t_s == 0:
    # portas teste simple
    serPort1 = "COM3"  # Stim
    serPort2 = "COM4"  # Accel
    serPort3 = "COM10"  # load
else:
    # Portas estimulador y loadcell
    serPort1 = "COM3"  # Stim
    serPort2 = "COM4"  # Accel
    serPort3 = "COM11"  # load  >>> ver no nipo

tex_min = 5
tex_max = 30
# exemplo 2>50>500>1.0>5>2.0>2.0>0>4.0>1>0.5>0.5>0>1>5>500>0>0>0>0>0>1>
tex = ""

# Variaveis estimulacion
ts = 1
fq = 50
pw = 500
tn = 5
tf = 5
ru = 0.5
rd = 0.5
ma = 50

# exemplo 2.0>50>500>1.0>5>2.0>2.0>10>4.0>1>0.5>0.5>0>1>5>500>0>0>1>0>1>0>
tng = ""

baudRate = 2000000

# datos de acel y load
array_stim = []
array_acel = []
array_load = []

# lock to serialize console output
lock = threading.Lock()

start_thread_acel = True
start_thread_load = True
captura_load = False
stim = False

# valores para la sequencia
start_tex_seq = False
start_stim_seq = False

# Para escoger el nombre entre calibrar y Tex
cal_tex = False

# Variable de threshold para teste de excitabilidade
ths_tex = 0.0
med_tex = 0.0
val_std = 6 ########## >>>>>>>>>>>>>>>> Este valor da el desvio para el threshold esta entre 4 y 8

seq_name = 1


# Teste de comunicacion de las pueras seriales
com1 = 0
com2 = 0
com3 = 0

############# Variable que guarda los resultados del TEX
tex_values = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        uic.loadUi("teste_total.ui", self)

        self.pb_start_tex.clicked.connect(self.btn_start_tex)
        self.pb_start_stim.clicked.connect(self.btn_start_stim)
        self.pb_calibrar.clicked.connect(self.btn_calibrar)
        self.pb_stop.clicked.connect(self.btn_stop)
        self.pb_thread.clicked.connect(self.thread_view)

        self.pb_seq.clicked.connect(self.sequencia)
        self.pb_conx.clicked.connect(self.test_conx)

        self.pb_export.clicked.connect(self.export_tex_values)

        # Show interface
        self.show()

    @staticmethod
    def export_tex_values():
        global tex_values

        horaa = time.strftime("%H")
        n_diaa = time.strftime("%a")
        diaa = time.strftime("%d")
        mma = time.strftime("%M")

        file_name_out_a = 'Tex values ' + n_diaa + ' ' + diaa + ' ' + horaa + 'h' + mma + '.txt'

        tv_ar = open(file_name_out_a, 'w+')
        ctv = 1

        for texv in tex_values:
            tv_ar.write(texv)
            tv_ar.write("\n")
            print(str(ctv) + " " + texv)
            ctv = ctv + 1

        tv_ar.close()

        print("End generation of tex values file")

    def test_conx(self):
        test_communication()

    def mess(self):
        global com1, com2, com3, serPort1, serPort2, serPort3

        if com1 == 1:
            QMessageBox.warning(self, "Error", "No se puede comunicar con el Teensy de Stim: " + serPort1)
        elif com1 == 2:
            QMessageBox.information(self, "Conexion", "Conectado con Teensy de Stim: " + serPort1)

        if com2 == 1:
            QMessageBox.warning(self, "Error", "No se puede comunicar con el Teensy de Acel: " + serPort2)
        elif com2 == 2:
            QMessageBox.information(self, "Conexion", "Conectado con Teensy de Acel: " + serPort2)

        if com3 == 1:
            QMessageBox.warning(self, "Error", "No se puede comunicar con el Teensy de Load: " + serPort3)
        elif com3 == 2:
            QMessageBox.information(self, "Conexion", "Conectado con Teensy de Load: " + serPort3)

    def btn_start_tex(self):
        global tex, tng, teste_training, tex_min, tex_max, captura_load, \
            start_thread_acel, start_thread_load, stim, seq_name

        start_thread_acel = True
        start_thread_load = True
        stim = False

        seq_name = 2

        captura_load = False

        self.thread_view()
        time.sleep(1)

        tex = "2>50>500>1.0>5>2.0>2.0>0>4.0>1>0.5>0.5>0>" \
              + str(tex_min) + \
              ">" \
              + str(tex_max) + \
              ">500>1>0>0>0>1>0>"

        print("\n\n\n")
        print("Comenzando TEX >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(tex)

        self.start_training()

    def btn_start_stim(self):
        global tex, tng, captura_load, start_thread_acel, start_thread_load, stim, seq_name

        start_thread_acel = True
        start_thread_load = True
        stim = True

        seq_name = 3

        captura_load = True

        concatenar_training()
        tex = tng

        print("\n\n\n")
        print("Comenzando STIM >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(tex)

        self.start_training()

    @staticmethod
    def start_training():
        start_test()

    @staticmethod
    def btn_calibrar():
        global tex, start_thread_acel, start_thread_load, seq_name

        start_thread_acel = True
        start_thread_load = True

        seq_name = 1

        # tex = "0>50>500>1.0>5>2.0>2.0>0>4.0>1>0.5>0.5>0>1>5>500>0>0>0>0>0>1>"  # Para dar un Stop
        tex = "2>50>500>1.0>5>2.0>2.0>0>4.0>1>0.5>0.5>0>1>5>500>0>1>0>0>1>0>"  # para calibrar

        print("\n\n\n")
        print("Comenzando Calibation >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(tex)

        calibrate_acel()

    @staticmethod
    def btn_stop():
        global tex

        # Para dar un Stop
        tex = "0>50>500>1.0>5>2.0>2.0>0>4.0>1>0.5>0.5>0>1>5>500>0>0>0>0>0>1>"

        print("\n\n\n")
        print("STOP >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(tex)

        stop_stim()

    @staticmethod
    def thread_view():
        print(threading.active_count())
        print(threading.enumerate())
        print(threading.current_thread())

    def upd_terminal(self, msn):
        self.le_terminal.setText(msn)

    def sequencia(self):
        # fazer thred para fazer sequencia
        sequencia_thread()


def sequencia_thread():
    global start_tex_seq, start_stim_seq

    ex.btn_calibrar()
    seq_t = True
    sc = 1
    while seq_t is True:

        if start_tex_seq is True:
            ex.btn_start_tex()
        elif start_stim_seq is True:
            ex.btn_start_tex()

        if sc == 4:
            seq_t = False


def test_communication():
    global serPort1, serPort2, serPort3, baudRate

    com_group(serPort1, baudRate, "n")
    ex.mess()
    time.sleep(1)
    com_group(serPort2, baudRate, "n")
    ex.mess()
    time.sleep(1)
    com_group(serPort3, baudRate, "n")
    ex.mess()
    time.sleep(1)


######################################################################################################
def stop_stim():
    global serPort1, serPort2, serPort3, baudRate, tex, start_thread_load, start_thread_acel

    com_group(serPort1, baudRate, tex)
    com_group(serPort2, baudRate, "f")
    com_group(serPort3, baudRate, "f")

    start_thread_load = False
    start_thread_acel = False


def com_group(port, baud, str_send):
    global com1, com2, com3, serPort2, serPort3, serPort1

    serSs = serial.Serial()
    serSs.port = port
    serSs.timeout = 1
    serSs.baudrate = baud
    serSs.xonxoff = 1

    try:
        serSs.open()
        if port is serPort1:
            com1 = 2
            com2 = 0
            com3 = 0

        if port is serPort2:
            com1 = 0
            com2 = 2
            com3 = 0

        if port is serPort3:
            com1 = 0
            com2 = 0
            com3 = 2

    except Exception as e:
        print("Error open serial port: " + str(e) + " En -- read_serial group--")
        print("Pasando a enviar stop forzado <<<<>>>>>")
        if port is serPort1:
            com1 = 1
            com2 = 0
            com3 = 0

        if port is serPort2:
            com1 = 0
            com2 = 1
            com3 = 0

        if port is serPort3:
            com1 = 0
            com2 = 0
            com3 = 1

    if serSs.isOpen():
        try:
            serSs.write(str.encode(str_send))
            print("Enviando comando Stop")
        except Exception as e1:
            print("Error communicating...: " + str(e1) + " En -- read_serial Stop--")

        serSs.close()
    else:
        print("Cannot open serial port " + str(serPort1) + "En -- read_serial Stop--")


###############################################################################################################
# para hacer calibracion
def calibrate_acel():
    global serPort1, serPort2, baudRate, cal_tex

    cal_tex = True

    try:
        t1 = threading.Thread(target=read_serial_stim, args=(serPort1, baudRate))
        t1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t1.start()

    except Exception as e1:
        print("Error: unable to start thread 1" + str(e1))

    try:
        t2 = threading.Thread(target=read_serial_acel, args=(serPort2, baudRate))
        t2.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t2.start()
    except Exception as e1:
        print("Error: unable to start thread 2" + str(e1))


###############################################################################################################
# para hacer tex
def start_test():
    global serPort1, serPort2, serPort3, baudRate, cal_tex, captura_load

    cal_tex = False

    try:
        t1 = threading.Thread(target=read_serial_stim, args=(serPort1, baudRate))
        t1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t1.start()

    except Exception as e1:
        print("Error: unable to start thread 1" + str(e1))

    try:
        t2 = threading.Thread(target=read_serial_acel, args=(serPort2, baudRate))
        t2.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t2.start()
    except Exception as e1:
        print("Error: unable to start thread 2" + str(e1))

    if captura_load is True:
        try:
            t3 = threading.Thread(target=read_serial_load, args=(serPort3, baudRate))
            t3.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            t3.start()
        except Exception as e1:
            print("Error: unable to start thread 3" + str(e1))


def read_serial_stim(port, baud):
    global tex

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
            ser.write(str.encode(tex))
        except Exception as e1:
            print("Error communicating...: " + str(e1) + "En -- read_serial --")

        ser.close()
    else:
        print("Cannot open serial port " + str(port) + "En -- read_serial --")
        exit()

    print("End Thread Stim data")


###############################################################################################################
def read_serial_acel(port, baud):
    global tex, array_acel, start_thread_load, start_thread_acel, med_tex, ths_tex, \
        cal_tex, stim, start_tex_seq, start_stim_seq, tex_min, tex_max, tex_values

    array_acel = []  # array for stim data
    bits_dac = 65536  # 2 ^ 16

    ser2 = serial.Serial()
    ser2.port = port
    ser2.timeout = 1
    ser2.baudrate = baud
    ser2.xonxoff = 1

    ct = 1
    ctr1 = 0
    ct_ma = tex_min

    try:
        ser2.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + " En -- read_serial --")
        exit()

    str_t = ""

    if ser2.isOpen():
        try:
            print("Start capture for Acel data")
            while start_thread_acel is True:
                ca = ser2.readline()
                with lock:
                    if len(ca) > 0:
                        str_msn2 = ca.decode("utf-8")
                        str_msn2 = str_msn2.rstrip()
                        # print("RAW > " + str(ct) + " " + str_msn2)
                        ct = ct + 1
                        if ct == 31:
                            print("RAW > " + str(ct) + " " + str_msn2)
                            str_msn2 = str_t
                        else:
                            str_t = str_msn2

                        if cal_tex is False:
                            acel_data = np.fromstring(str_msn2, dtype=int, sep=";")

                            # Normalize the axis from digital to g(m/s^2)
                            eje_x = acel_data[1] / bits_dac
                            eje_y = acel_data[2] / bits_dac
                            eje_z = acel_data[3] / bits_dac
                            sinal = acel_data[4]

                            if sinal == 1 and ctr1 == 0:
                                ctr1 = 1

                            if sinal == 0 and ctr1 == 1:
                                ct_ma = ct_ma + 1
                                ctr1 = 0

                            eje_x2 = eje_x ** 2
                            eje_y2 = eje_y ** 2
                            eje_z2 = eje_z ** 2

                            # Magnitude of the resulting vector
                            xyz = np.sqrt(eje_x2 + eje_y2 + eje_z2)
                            xyz = xyz - med_tex

                            if xyz > ths_tex and stim is False and sinal == 1:
                                start_thread_acel = False
                                ex.btn_stop()
                                tex_min = ct_ma - 1
                                tex_max = ct_ma + 10
                                print("Vibracion detectada en " + str(ct_ma) + " mA")
                                tex_values.append(ct_ma)
                                ser2.write(str.encode("f"))
                                ser2.close()

                            #print("Valor de xyz: " + str(xyz))
                            # str_msn2 = str(xyz)

                        # print(str_msn2)
                        if str_msn2 == '>':
                            start_thread_acel = False
                            start_thread_load = False
                            print("End capture about Acel data en send Value for end load cell capture data")
                        else:
                            array_acel.append(str_msn2)
            ser2.close()

        except Exception as e1:
            print("Error communicating...: " + str(e1) + " No se puede mandar el mensaje al acel")

    else:
        print("Cannot open serial port " + str(port) + " No se puede abrir la puerta del acel")
        exit()

    # start_thread_load = False  #  Funcionando
    save_data_acel()  # Thread for acel data

    print("End Thread Acel data")

    if cal_tex is False:
        start_tex_seq = False
        start_stim_seq = True


# salva los datos del stim
def save_data_acel():
    global array_acel, cal_tex, seq_name

    horaa = time.strftime("%H")
    n_diaa = time.strftime("%a")
    diaa = time.strftime("%d")
    mma = time.strftime("%M")

    if cal_tex is True:
        file_name_out_a = str(seq_name) + 'cal_acel_data ' + n_diaa + ' ' + diaa + ' ' + horaa + 'h' + mma + '.txt'
    else:
        file_name_out_a = str(seq_name) + 'acel_data ' + n_diaa + ' ' + diaa + ' ' + horaa + 'h' + mma + '.txt'

    ar_acel = open(file_name_out_a, 'w+')
    c = 1

    for xa in array_acel:
        #ar_acel.write("%s\n" % xa)
        ar_acel.write(xa)
        ar_acel.write("\n")
        # print(str(c) + " " + xa)
        c = c + 1

    ar_acel.close()

    print("End generation of Acel file")

    if cal_tex is True:
        print("Pasando a calcular o desvio padrao base para limear")
        cal_std(file_name_out_a)
        cal_tex = False


def cal_std(name_file_cal):
    global med_tex, ths_tex, val_std, array_acel, start_tex_seq

    """c = 1
    for x in array_acel:
        print(str(c) + x)
        c = c + 1"""

    data = []
    val = False

    try:
        data = np.loadtxt(name_file_cal, delimiter=';')
        val = True
    except Exception as e:
        print("Error: " + str(e) + " in --" + name_file_cal + " El archivo esta con error")
        val = False

    if len(data) == 0:
        print("Lista vacia: " + str(data.all()))

    if val is True:
        eje_x = data[:, 1]
        eje_y = data[:, 2]
        eje_z = data[:, 3]
        signal_pulse = data[:, 4]

        n = len(signal_pulse)  # Tamanho del vector

        t = np.arange(0, n)  # Crea un vector del tamanho del la serie

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
        med_xyz = np.mean(eje_xyz)
        med_tex = med_xyz
        print("valor medio: " + str(med_tex))
        eje_xyz = eje_xyz - med_xyz

        std_xyz = np.std(eje_xyz)
        print("La desviacion standard es: " + str(std_xyz))

        # Threshold calculation based on standard deviations
        num_std = val_std
        thsdxyz = num_std * std_xyz
        print("El valor de threshold es: " + str(thsdxyz))
        ths_tex = thsdxyz

        print("End Thread Calibration process")
        start_tex_seq = True

        """
        # linea del threshold
        lin_thsdxyz = np.ones((n, 1)) * thsdxyz

        # Parameters used in the filter
        cut_off = 30
        fs = round(n / 2)
        order = 10

        acxyz_fil = butter_lowpass_filter(eje_xyz, cut_off, fs, order)
        # plt.plot(t, acxyz_fil, 'r', linewidth=1, label='Butterworth Filter Accel Signal')

        plt.figure(1)

        plt.subplot(211)
        plt.title = '2s of gross Acceleration Data for calibration'
        plt.xlabel = 'time (ms)'
        plt.ylabel = 'm/s^2 - median data'
        plt.plot(t, lin_thsdxyz, 'y', label='Threshold')
        plt.plot(t, eje_xyz, 'b', linewidth=0.5)
        print("Valor del desvio: " + str(thsdxyz))

        plt.subplot(212)
        plt.plot(t, lin_thsdxyz, 'y', label='Threshold')
        plt.plot(t, acxyz_fil, 'b', linewidth=0.5)
        print("Valor del desvio: " + str(med_xyz + thsdxyz))

        plt.show()
        stop_stim()"""


def butter_lowpass_filter(data, cut_off, fs, order=5):
    b, a = butter_lowpass(cut_off, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_lowpass(cut_off, fs, order=5):
    nyq = 0.5 * fs
    normal_cut_off = cut_off / nyq
    b, a = butter(order, normal_cut_off, btype='low', analog=False)
    return b, a


###############################################################################################################
def read_serial_load(port, baud):
    global tex, array_load, start_thread_load

    array_load = []  # array for stim data

    ser3 = serial.Serial()
    ser3.port = port
    ser3.timeout = 1
    ser3.baudrate = baud
    ser3.xonxoff = 1

    try:
        ser3.open()
    except Exception as e:
        print("Error open serial port: " + str(e) + " En -- read_serial --")
        exit()

    if ser3.isOpen():
        try:
            ser3.write(str.encode("s"))
            #  ex.upd_terminal("s load cell")
            print("Start capture for Load data")
            while start_thread_load is True:
                cl = ser3.readline()
                with lock:
                    if len(cl) > 0:
                        str_msn3 = cl.decode("utf-8")
                        str_msn3 = str_msn3.rstrip()
                        print(str_msn3)
                        array_load.append(str_msn3)

            ser3.write(str.encode("f"))
            ser3.close()
            print("End capture about load data - saliendo de capturar datos de la celula de carga -")

        except Exception as e1:
            print("Error communicating...: " + str(e1) + " No se puede abror la puerta ")

    else:
        print("Cannot open serial port " + str(port) + " La puerta no está abierta")
        exit()

    save_data_load()  # Thread for acel data
    print("End Thread Load data")


# salva los datos del stim
def save_data_load():
    global array_load, start_thread_stim, start_thread_acel, start_thread_load, seq_name

    horal = time.strftime("%H")
    n_dial = time.strftime("%a")
    dial = time.strftime("%d")
    mml = time.strftime("%M")

    file_name_out_l = str(seq_name) + 'load_data ' + n_dial + ' ' + dial + ' ' + horal + 'h' + mml + '.txt'

    ar_load = open(file_name_out_l, 'w+')
    col = 1

    for xl in array_load:
        ar_load.write("%s\n" % xl)
        print(str(col) + " " + xl)
        col = col + 1

    ar_load.close()

    print("End generation of Load file")
    # ex.upd_terminal("End generation of Load file")

    start_thread_acel = True
    start_thread_load = True


def concatenar_training():
    global ts, fq, pw, tn, tf, ru, rd, ma, tng
    # exemplo 2>50>500>1.0>5>2.0>2.0>10>4.0>1>0.5>0.5>0>1>5>500>0>0>1>0>1>0>
    tnt = tn
    tn = tn - (ru + rd)

    tng = str(ts) + ">" + str(fq) + ">" + str(pw) + ">" + str(tn) + ">" + str(tf) + ">" \
          + str(ru) + ">" + str(rd) + ">" + str(ma) + ">" + "4.0>1>0.5>0.5>0>1>5>500>0>0>1>0>1>0>"

    tn = tnt


def exit_program_and_stim():
    print(">>>>>>>>>> Aplication closed, Stop Stimulation <<<<<<<<<<<<")
    ex.btn_stop()
    exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(exit_program_and_stim)
    ex = MainWindow()
    sys.exit(app.exec_())
