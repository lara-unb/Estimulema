from PyQt5 import QtWidgets, uic


def Convert():
    interface.radioButton.setText("Hola")


def TheT_Plus():
    dataText = interface.Tht_Lb.text()
    val = int(dataText)
    if val < 10:
        val = val + 1
        interface.Tht_Lb.setText(str(val))
        interface.TherapyTimeSlider.setValue(val)
    else:
        val = 10
        interface.Tht_Lb.setText(str(val))
        interface.TherapyTimeSlider.setValue(val)



def TheT_Minus():
    dataText = interface.Tht_Lb.text()
    val = int(dataText)
    if val > 0 & val < 10:
        val = val - 1
        interface.Tht_Lb.setText(str(val))
        interface.TherapyTimeSlider.setValue(val)
    else:
        val = 0
        interface.Tht_Lb.setText(str(val))
        interface.TherapyTimeSlider.setValue(val)


def TheT_Slider():
    interface.Tht_Lb.setText(str(interface.TherapyTimeSlider.value()))


app = QtWidgets.QApplication([])
interface = uic.loadUi("GUI_Estimulema.ui")

interface.StartCh1.clicked.connect(Convert)

#To work with therapy buttons ans slider
interface.TheT_PlusBtn.clicked.connect(TheT_Plus)
interface.TheT_MinusBtn.clicked.connect(TheT_Minus)
interface.TherapyTimeSlider.valueChanged.connect(TheT_Slider)


interface.show()
app.exec()
