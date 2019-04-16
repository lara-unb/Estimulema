import serial
import threading

serPort1 = "COM13"
baudRate = 2000000

# lock to serialize console output
lock = threading.Lock()

try:
    t1 = threading.Thread(target=read_serial, args=(serPort1, baudRate))
    t1.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t1.start()

except:
    print("Error: unable to start thread")


def read_serial(port, baud):
    start_thread_s = True
    ser = serial.Serial()
    ser.port = port
    ser.timeout = 1
    ser.baudrate = baud
    ser.xonxoff = 1

    msg = "2>50>500>5>0>1>10>5>1>1>0>5>500>1>0>0>0>1>0>"
    msg_bytes = str.encode(msg)

    try:
        ser.open()
    except Exception as e:
        print("Error open serial port: " + str(e))
        exit()

    if ser.isOpen():
        try:
            while start_thread_s is False:
                pass

            ser.write(msg_bytes)
            print("Star capture for Stim")

        except Exception as e1:
            print("error communicating...: " + str(e1))

    else:
        print("Cannot open serial port " + str(port))
        exit()

    print("End Thread Stim")
