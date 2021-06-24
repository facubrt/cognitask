### Módulo de Aplicación #################################################
##########################################################################
## Autor: Facundo Barreto ### facubrt@gmail.com ##########################
## 
## BCI basada en P300 para rehabilitación cognitiva ######################
## 
## Proyecto Final de Bioingeniería ### 2020 ##############################

### LICENCIA GPL #########################################################
## This file is part of Cognitask. #######################################
##
##  Cognitask is free software: you can redistribute it and/or modify ####
##  it under the terms of the GNU General Public License as published by #
##  the Free Software Foundation, either version 3 of the License, or ####
##  (at your option) any later version. ##################################
##
##  Cognitask is distributed in the hope that it will be useful, #########
##  but WITHOUT ANY WARRANTY; without even the implied warranty of #######
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the ########
##  GNU General Public License for more details. #########################
##
##  You should have received a copy of the GNU General Public License ####
##  along with Cognitask.  If not, see <https://www.gnu.org/licenses/>. ##

from .ui_aplicacion import Ui_BCIAplicacion
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets

GLOBAL_STATE = 0

class BCIAplicacion(QtWidgets.QMainWindow, Ui_BCIAplicacion):
   
# INICIALIZACION
# ///////////////////////////////////////////////////////////
    def __init__(self):
        super(BCIAplicacion, self).__init__()
        self.setupUi(self)

        self.maximizar_boton.clicked.connect(lambda: BCIAplicacion.maximize_restore(self))
        self.minimizar_boton.clicked.connect(lambda: self.showMinimized())
        self.cerrar_boton.clicked.connect(lambda: BCIAplicacion.cerrarAplicacion(self))
        self.expandir_boton.clicked.connect(lambda: self.toggleMenu(310, True))

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # Frameless Window

        def moveWindow(event):
                if event.buttons() == QtCore.Qt.LeftButton and GLOBAL_STATE == 0:
                        self.move(self.pos() + event.globalPos() - self.dragPos)
                        self.dragPos = event.globalPos()
                        event.accept()
        
        self.titlebar_frame.mouseMoveEvent = moveWindow

# FUNCIONES DE INTERFAZ GENERAL
# ///////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE

        # si no está maximizada
        if status == 0:
                self.showFullScreen()
                GLOBAL_STATE = 1

        else:
                GLOBAL_STATE = 0
                self.showNormal()
    
    def cerrarAplicacion(self):
            self.Open = 0
            self.close()
  
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def toggleMenu(self, maxWidth, enable):
            if enable:
                width = self.right_frame.width()
                heigth = self.bottom_frame.height()
                maxHeigth = 150 # bottom frame
                minHeight = 0 # bottom frame
                standard = 0

                if width == 0:
                        widthExtended = maxWidth
                        nueva_heigth = minHeight
                        self.expandir_boton.setIcon(self.icon4)

                else:
                        widthExtended = standard
                        nueva_heigth = maxHeigth
                        self.expandir_boton.setIcon(self.icon3)
                
                self.animation = QPropertyAnimation(self.right_frame, b"minimumWidth")
                self.animation_2 = QPropertyAnimation(self.bottom_frame,b"maximumHeight")
                self.animation.setDuration(400)
                self.animation_2.setDuration(400)
                self.animation.setStartValue(width)
                self.animation_2.setStartValue(heigth)
                self.animation.setEndValue(widthExtended)
                self.animation_2.setEndValue(nueva_heigth)
                self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation_2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation.start()
                self.animation_2.start()
        
    def ocultar(self):
        self.p3_frame.hide() 
    
    def mostrar(self):
        if self.Open == 0:
            self.Open = 1
            self.show()
        self.p3_frame.show()
                
# FUNCIONES DE INTERFAZ GENERAL
# ///////////////////////////////////////////////////////////
    def mostrarMatriz(self, mostrar):
        
        if mostrar is True:
                self.p3_frame.show()
                print('mostrar true')
        else:
                self.p3_frame.hide()
                print('mostrar false')