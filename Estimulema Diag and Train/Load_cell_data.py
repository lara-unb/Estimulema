import serial
import matplotlib.pyplot as plt
from drawnow import *
import atexit

values = []

plt.ion()
cnt = 0

serialArduino = serial.Serial('COM19', 115200)


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


atexit.register(doAtExit)

print("serialArduino.isOpen() = " + str(serialArduino.isOpen()))
ini = 's'
ini_b = str.encode(ini)
serialArduino.write(ini_b)

# pre-load dummy data
for i in range(0, 100):
    values.append(0)

while True:
    while (serialArduino.inWaiting() == 0):
        pass
    print("readline()")
    valueRead = serialArduino.readline()

    # check if valid value can be casted
    try:
        str_msn = valueRead.decode("utf-8")
        str_msn = str_msn.rstrip()
        valueInInt = float(str_msn)
        print(valueInInt)
        if valueInInt <= 1024:
            if valueInInt >= 0:
                values.append(valueInInt)
                values.pop(0)
                drawnow(plotValues)
            else:
                print("Invalid! negative number")
        else:
            print("Invalid! too large")
    except ValueError:
        print("Invalid! cannot cast")