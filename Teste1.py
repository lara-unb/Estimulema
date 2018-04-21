from PyQt5 import QtWidgets, uic
import serial
import struct

# Enable serial communication
serPort = "COM11"
# baudRate = 2000000
baudRate = 57600
ser = serial.Serial(serPort, baudRate, timeout=1, xonxoff=1)
print("Serial port: " + serPort + ", Baud rate:" + str(baudRate))

# First String communication - global variables
valT_CH1 = 0  # Save de Therapy value
valF_CH1 = 0  # Save de Frequency value
valPw_CH1 = 0  # Save de PulseWidth value
valTn_CH1 = 0  # Save de TOn value
valTf_CH1 = 0  # Save de TOff value
valC_CH1 = 0  # Save de Current value

# Character for initialize, finalize and separate message
ini_char = '<'
end_char = '!>'
separate_char = ';'

# Variables for flow control
# StrBtn has 3 options
# 1 = Start Button was press to send data
# 2 = Individuals Buttons for stimulate parameters are enable to send data
# 3 = All buttons are disable to send data - the program initialize whit this option
FC_StrBtn_CH1 = 0


# ###################################################### Function for Controls of CH1
# ---------------------------- Therapy time
def the_plus1():
    # This function enable button interaction to increase the Therapy time
    global valT_CH1
    global FC_StrBtn_CH1
    data = interface.Label_TherapyValCH1.text()
    val = int(data)
    if val < 100:
        val = val + 1
        interface.Label_TherapyValCH1.setText(str(val))
        interface.Slider_TherapyCH1.setValue(val)
    else:
        val = 100
        interface.Label_TherapyValCH1.setText(str(val))
        interface.Slider_TherapyCH1.setValue(val)

    valT_CH1 = val

    if FC_StrBtn_CH1 == 1:
        data_out = msg_ini(0)  # "0" for single data
        data_out = data_out + "T" + str(val)
        print("data from T_M btn: " + data_out)
        send_data(data_out)


def the_minus1():
    # This function enable button interaction to decrease the Therapy time
    global valT_CH1
    global FC_StrBtn_CH1
    data = interface.Label_TherapyValCH1.text()
    val = int(data)
    if val > 0 & val < 100:
        val = val - 1
        interface.Label_TherapyValCH1.setText(str(val))
        interface.Slider_TherapyCH1.setValue(val)
    else:
        val = 0
        interface.Label_TherapyValCH1.setText(str(val))
        interface.Slider_TherapyCH1.setValue(val)

    valT_CH1 = val

    if FC_StrBtn_CH1 == 1:
        data_out = msg_ini(0)  # "0" for single data
        data_out = data_out + "T" + str(val)
        print("data from T_M btn: " + data_out)
        send_data(data_out)


def the_slider1():
    # This function enable slider interaction to increase/decrease the Therapy time
    global valT_CH1
    val = interface.Slider_TherapyCH1.value()
    valT_CH1 = val
    interface.Label_TherapyValCH1.setText(str(val))


# ---------------------------- Frequency
def frequency_plus1():
    # This function enable button interaction to increase the Frequency
    # and return the period time in milliseconds
    global valF_CH1
    global FC_StrBtn_CH1
    data = interface.Label_FrequencyValCH1.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_FrequencyValCH1.setText(str(val))
        interface.Slider_FrequencyCH1.setValue(val)
    else:
        val = 10
        interface.Label_FrequencyValCH1.setText(str(val))
        interface.Slider_FrequencyCH1.setValue(val)

    valF_CH1 = val

    if FC_StrBtn_CH1 == 1:
        data_out = msg_ini(0)  # "0" for single data
        data_out = data_out + "F" + str(val)
        print("data about Therapy time: " + data_out)
        send_data(data_out)


def frequency_minus1():
    # This function enable button interaction to decrease the Frequency
    # and return the period time in milliseconds
    global valF_CH1
    global FC_StrBtn_CH1
    data = interface.Label_FrequencyValCH1.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_FrequencyValCH1.setText(str(val))
        interface.Slider_FrequencyCH1.setValue(val)
    else:
        val = 0
        interface.Label_FrequencyValCH1.setText(str(val))
        interface.Slider_FrequencyCH1.setValue(val)

    valF_CH1 = val

    if FC_StrBtn_CH1 == 1:
        data_out = msg_ini(0)  # "0" for single data
        data_out = data_out + "F" + str(val)
        print("data about Frequency: " + data_out)
        send_data(data_out)


def frequency_slider1():
    # This function enable slider interaction to increase/decrease the Frequency
    # and return the period time in milliseconds
    global valF_CH1
    val = interface.Slider_FrequencyCH1.value()
    valF_CH1 = val
    interface.Label_FrequencyValCH1.setText(str(val))


# ---------------------------- Pulse Witdth
def pulsewidth_plus1():
    data = interface.Label_PulseWidthValCH1.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_PulseWidthValCH1.setText(str(val))
        interface.Slider_PulseWidthCH1.setValue(val)
    else:
        val = 10
        interface.Label_PulseWidthValCH1.setText(str(val))
        interface.Slider_PulseWidthCH1.setValue(val)


def pulsewidth_minus1():
    data = interface.Label_PulseWidthValCH1.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_PulseWidthValCH1.setText(str(val))
        interface.Slider_PulseWidthCH1.setValue(val)
    else:
        val = 0
        interface.Label_PulseWidthValCH1.setText(str(val))
        interface.Slider_PulseWidthCH1.setValue(val)


def pulsewidth_slider1():
    interface.Label_PulseWidthValCH1.setText(str(interface.Slider_PulseWidthCH1.value()))


# ---------------------------- T On
def ton_plus1():
    data = interface.Label_TOnValCH1.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_TOnValCH1.setText(str(val))
        interface.Slider_TOnCH1.setValue(val)
    else:
        val = 10
        interface.Label_TOnValCH1.setText(str(val))
        interface.Slider_TOnCH1.setValue(val)


def ton_minus1():
    data = interface.Label_TOnValCH1.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_TOnValCH1.setText(str(val))
        interface.Slider_TOnCH1.setValue(val)
    else:
        val = 0
        interface.Label_TOnValCH1.setText(str(val))
        interface.Slider_TOnCH1.setValue(val)


def ton_slider1():
    interface.Label_TOnValCH1.setText(str(interface.Slider_TOnCH1.value()))


# ---------------------------- T Off
def toff_plus1():
    data = interface.Label_TOffValCH1.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_TOffValCH1.setText(str(val))
        interface.Slider_TOffCH1.setValue(val)
    else:
        val = 10
        interface.Label_TOffValCH1.setText(str(val))
        interface.Slider_TOffCH1.setValue(val)


def toff_minus1():
    data = interface.Label_TOffValCH1.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_TOffValCH1.setText(str(val))
        interface.Slider_TOffCH1.setValue(val)
    else:
        val = 0
        interface.Label_TOffValCH1.setText(str(val))
        interface.Slider_TOffCH1.setValue(val)


def toff_slider1():
    interface.Label_TOffValCH1.setText(str(interface.Slider_TOffCH1.value()))


# ---------------------------- Current
def current_plus1():
    data = interface.Label_CurrentValCH1.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_CurrentValCH1.setText(str(val))
        interface.Slider_CurrentCH1.setValue(val)
    else:
        val = 10
        interface.Label_CurrentValCH1.setText(str(val))
        interface.Slider_CurrentCH1.setValue(val)


def current_minus1():
    data = interface.Label_CurrentValCH1.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_CurrentValCH1.setText(str(val))
        interface.Slider_CurrentCH1.setValue(val)
    else:
        val = 0
        interface.Label_CurrentValCH1.setText(str(val))
        interface.Slider_CurrentCH1.setValue(val)


def current_slider1():
    interface.Label_CurrentValCH1.setText(str(interface.Slider_CurrentCH1.value()))


# ###################################################### Function for Controls of CH2
# ---------------------------- Therapy
def the_plus2():
    data = interface.Label_TherapyValCH2.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_TherapyValCH2.setText(str(val))
        interface.Slider_TherapyCH2.setValue(val)
    else:
        val = 10
        interface.Label_TherapyValCH2.setText(str(val))
        interface.Slider_TherapyCH2.setValue(val)


def the_minus2():
    data = interface.Label_TherapyValCH2.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_TherapyValCH2.setText(str(val))
        interface.Slider_TherapyCH2.setValue(val)
    else:
        val = 0
        interface.Label_TherapyValCH2.setText(str(val))
        interface.Slider_TherapyCH2.setValue(val)


def the_slider2():
    interface.Label_TherapyValCH2.setText(str(interface.Slider_TherapyCH2.value()))


# ---------------------------- Frequency
def frequency_plus2():
    data = interface.Label_FrequencyValCH2.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_FrequencyValCH2.setText(str(val))
        interface.Slider_FrequencyCH2.setValue(val)
    else:
        val = 10
        interface.Label_FrequencyValCH2.setText(str(val))
        interface.Slider_FrequencyCH2.setValue(val)


def frequency_minus2():
    data = interface.Label_FrequencyValCH2.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_FrequencyValCH2.setText(str(val))
        interface.Slider_FrequencyCH2.setValue(val)
    else:
        val = 0
        interface.Label_FrequencyValCH2.setText(str(val))
        interface.Slider_FrequencyCH2.setValue(val)


def frequency_slider2():
    interface.Label_FrequencyValCH2.setText(str(interface.Slider_FrequencyCH2.value()))


# ---------------------------- Pulse Witdth
def pulsewidth_plus2():
    data = interface.Label_PulseWidthValCH2.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_PulseWidthValCH2.setText(str(val))
        interface.Slider_PulseWidthCH2.setValue(val)
    else:
        val = 10
        interface.Label_PulseWidthValCH2.setText(str(val))
        interface.Slider_PulseWidthCH2.setValue(val)


def pulsewidth_minus2():
    data = interface.Label_PulseWidthValCH2.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_PulseWidthValCH2.setText(str(val))
        interface.Slider_PulseWidthCH2.setValue(val)
    else:
        val = 0
        interface.Label_PulseWidthValCH2.setText(str(val))
        interface.Slider_PulseWidthCH2.setValue(val)


def pulsewidth_slider2():
    interface.Label_PulseWidthValCH2.setText(str(interface.Slider_PulseWidthCH2.value()))


# ---------------------------- T On
def ton_plus2():
    data = interface.Label_TOnValCH2.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_TOnValCH2.setText(str(val))
        interface.Slider_TOnCH2.setValue(val)
    else:
        val = 10
        interface.Label_TOnValCH2.setText(str(val))
        interface.Slider_TOnCH2.setValue(val)


def ton_minus2():
    data = interface.Label_TOnValCH2.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_TOnValCH2.setText(str(val))
        interface.Slider_TOnCH2.setValue(val)
    else:
        val = 0
        interface.Label_TOnValCH2.setText(str(val))
        interface.Slider_TOnCH2.setValue(val)


def ton_slider2():
    interface.Label_TOnValCH2.setText(str(interface.Slider_TOnCH2.value()))


# ---------------------------- T Off
def toff_plus2():
    data = interface.Label_TOffValCH2.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_TOffValCH2.setText(str(val))
        interface.Slider_TOffCH2.setValue(val)
    else:
        val = 10
        interface.Label_TOffValCH2.setText(str(val))
        interface.Slider_TOffCH2.setValue(val)


def toff_minus2():
    data = interface.Label_TOffValCH2.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_TOffValCH2.setText(str(val))
        interface.Slider_TOffCH2.setValue(val)
    else:
        val = 0
        interface.Label_TOffValCH2.setText(str(val))
        interface.Slider_TOffCH2.setValue(val)


def toff_slider2():
    interface.Label_TOffValCH2.setText(str(interface.Slider_TOffCH2.value()))


# ---------------------------- Current
def current_plus2():
    data = interface.Label_CurrentValCH2.text()
    val = int(data)
    if val < 10:
        val = val + 1
        interface.Label_CurrentValCH2.setText(str(val))
        interface.Slider_CurrentCH2.setValue(val)
    else:
        val = 10
        interface.Label_CurrentValCH2.setText(str(val))
        interface.Slider_CurrentCH2.setValue(val)


def current_minus2():
    data = interface.Label_CurrentValCH2.text()
    val = int(data)
    if val > 0 & val < 10:
        val = val - 1
        interface.Label_CurrentValCH2.setText(str(val))
        interface.Slider_CurrentCH2.setValue(val)
    else:
        val = 0
        interface.Label_CurrentValCH2.setText(str(val))
        interface.Slider_CurrentCH2.setValue(val)


def current_slider2():
    interface.Label_CurrentValCH2.setText(str(interface.Slider_CurrentCH2.value()))


# StartButton
def start_ch1():
    # This function start the stimulation features with the all data
    global valT_CH1
    global FC_StrBtn_CH1
    FC_StrBtn_CH1 = 1
    ini_msg = msg_ini(1)  # The two first data

    data_out = ini_msg + str(valT_CH1) + separate_char + str(valTn_CH1) +\
               separate_char + str(valTf_CH1) + separate_char + str(valF_CH1) +\
               separate_char + str(valPw_CH1) + separate_char + str(valC_CH1)

    print("data from Star Button: " + data_out)
    send_data(data_out)


def send_data(data_out):
    # This function send data to Teensy
    msg = ini_char + data_out + end_char
    print("data from send_data function: " + msg)
    interface.plainTextEdit_terminal.setPlainText(msg)
    msg_bytes = str.encode(msg)
    ser.write(msg_bytes)
    msn = ser.readline()
    print(msn)


def msg_ini(string_type_data):
    # This function implement the two first data
    # -First character is the String type:
    # "1" for long string about all data
    # "0" for short string about single data
    # -Second character is Channel selection
    # "0" for no select channel
    # "1" for channel 1
    # "2" for channel 2
    # "3" for channel 3
    ch1_sel = interface.GroupBox_CH1.isChecked()
    ch2_sel = interface.GroupBox_CH2.isChecked()
    ch_sal_activation = 0
    if ch1_sel is True and ch2_sel is True:
        ch_sal_activation = 3
    elif ch1_sel is True and ch2_sel is False:
        ch_sal_activation = 1
    elif ch1_sel is False and ch2_sel is True:
        ch_sal_activation = 2

    data_out = str(string_type_data) + separate_char + str(ch_sal_activation) + separate_char
    return data_out


# ####################################################################### End actions
app = QtWidgets.QApplication([])

interface = uic.loadUi("GUI_Estimulema.ui")

# interface.Btn_StartCH1.clicked.connect(Convert)

# ######################################################################## Start Accions
# ----------------------------------------------------------------#
# To work with buttons ans sliders for CH1
# Therapy
interface.BtnMinus_TherapyCH1.clicked.connect(the_minus1)
interface.BtnPlus_TherapyCH1.clicked.connect(the_plus1)
interface.Slider_TherapyCH1.valueChanged.connect(the_slider1)
# Frequency
interface.BtnMinus_FrequencyCH1.clicked.connect(frequency_minus1)
interface.BtnPlus_FrequencyCH1.clicked.connect(frequency_plus1)
interface.Slider_FrequencyCH1.valueChanged.connect(frequency_slider1)
# PulseWidth
interface.BtnMinus_PulseWidthCH1.clicked.connect(pulsewidth_minus1)
interface.BtnPlus_PulseWidthCH1.clicked.connect(pulsewidth_plus1)
interface.Slider_PulseWidthCH1.valueChanged.connect(pulsewidth_slider1)
# TOn
interface.BtnMinus_TOnCH1.clicked.connect(ton_minus1)
interface.BtnPlus_TOnCH1.clicked.connect(ton_plus1)
interface.Slider_TOnCH1.valueChanged.connect(ton_slider1)
# TOff
interface.BtnMinus_TOffCH1.clicked.connect(toff_minus1)
interface.BtnPlus_TOffCH1.clicked.connect(toff_plus1)
interface.Slider_TOffCH1.valueChanged.connect(toff_slider1)
# Current
interface.BtnMinus_CurrentCH1.clicked.connect(current_minus1)
interface.BtnPlus_CurrentCH1.clicked.connect(current_plus1)
interface.Slider_CurrentCH1.valueChanged.connect(current_slider1)

# ----------------------------------------------------------------#
# To work with buttons ans sliders for CH2
# Therapy
interface.BtnMinus_TherapyCH2.clicked.connect(the_minus2)
interface.BtnPlus_TherapyCH2.clicked.connect(the_plus2)
interface.Slider_TherapyCH2.valueChanged.connect(the_slider2)
# Frequency
interface.BtnMinus_FrequencyCH2.clicked.connect(frequency_minus2)
interface.BtnPlus_FrequencyCH2.clicked.connect(frequency_plus2)
interface.Slider_FrequencyCH2.valueChanged.connect(frequency_slider2)
# PulseWidth
interface.BtnMinus_PulseWidthCH2.clicked.connect(pulsewidth_minus2)
interface.BtnPlus_PulseWidthCH2.clicked.connect(pulsewidth_plus2)
interface.Slider_PulseWidthCH2.valueChanged.connect(pulsewidth_slider2)
# TOn
interface.BtnMinus_TOnCH2.clicked.connect(ton_minus2)
interface.BtnPlus_TOnCH2.clicked.connect(ton_plus2)
interface.Slider_TOnCH2.valueChanged.connect(ton_slider2)
# TOff
interface.BtnMinus_TOffCH2.clicked.connect(toff_minus2)
interface.BtnPlus_TOffCH2.clicked.connect(toff_plus2)
interface.Slider_TOffCH2.valueChanged.connect(toff_slider2)
# Current
interface.BtnMinus_CurrentCH2.clicked.connect(current_minus2)
interface.BtnPlus_CurrentCH2.clicked.connect(current_plus2)
interface.Slider_CurrentCH2.valueChanged.connect(current_slider2)

# ------------------------#
# StartButton for Channel 1 - send all stimulate parameters to Teensy
interface.Btn_StartCH1.clicked.connect(start_ch1)

# ------------------------#
# StartButton for Channel 1 - send all stimulate parameters to Teensy
interface.Btn_StartCH2.clicked.connect(start_ch1)*-*-*-* adicionar las demas cosas y las funciones en cada conexion

interface.show()
app.exec()
