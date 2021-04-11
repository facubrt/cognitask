from PyQt5 import QtCore, QtWidgets, QtGui
from cognitask import Cognitask
from modulos.splash import Splash
import sys

# MAIN
def iniciarCognitask():
    timer.stop()
    Operador = Cognitask()
    Operador.show()
    splashScreen.close()

def agregarFuentes():
    # agrego las fuentes de texto Gilroy utilizadas
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Light.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Bold.ttf')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    agregarFuentes()
    splashScreen = Splash()
    splashScreen.show()

    # creo un temporizador para el splash
    timer = QtCore.QTimer()
    timer.timeout.connect(iniciarCognitask)
    timer.start(1250)
    QtCore.QCoreApplication.processEvents() 
    QtCore.QTimer.singleShot(1000, lambda: splashScreen.label_2.setText("Configurando módulos..."))
    QtCore.QTimer.singleShot(1200, lambda: splashScreen.label_2.setText("Iniciando..."))

    sys.exit(app.exec_())