from cognitask.cognitask import Cognitask
from cognitask.views.ui_splash import Ui_Splash
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore 

# SPLASH
# ///////////////////////////////////////////////////////////
class Splash(QMainWindow, Ui_Splash):
    
    def __init__(self):
        super(Splash, self).__init__()
        self.setupSplash(self)

        # Eliminacion de la barra de titulo por defecto
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # creo un temporizador para el splash
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.iniciarCognitask)
        self.timer.start(1250)
        QtCore.QTimer.singleShot(1000, lambda: self.label_2.setText("Configurando módulos..."))
        QtCore.QTimer.singleShot(1200, lambda: self.label_2.setText("Iniciando..."))
        
    def iniciarCognitask(self):
        self.timer.stop()
        ctask = Cognitask()
        ctask.show()
        self.close()