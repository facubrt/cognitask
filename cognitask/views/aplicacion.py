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
# from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from .ui_aplicacion import Ui_BCIAplicacion
import cognitask.common.constantes as constantes

# GLOBAL_STATE = 0

class BCIAplicacion(QMainWindow, Ui_BCIAplicacion):
    
    def __init__(self):
        super(BCIAplicacion, self).__init__()
    
    def cerrarAplicacion(self):
        self.Open = 0
        self.close()
         
    def ocultarMatriz(self):
        self.p3_frame.hide() 
    
    def mostrarMatriz(self):
        if self.Open == 0:
            self.Open = 1
            self.show()
        self.p3_frame.show()
        
    # MENSAJES
    # ///////////////////////////////////////////////////////////
    def mostrarMensajes(self, mensaje, estilo, temporal):
        
        self.feedback_label.setText(mensaje)
        self.feedback_label.setStyleSheet(estilo)
        self.feedback_label.show()
        if temporal == True:
            QtCore.QTimer.singleShot(2000, self.restablecerMensajes)
            
    def restablecerMensajes(self):
        self.feedback_label.hide()
        self.feedback_label.setStyleSheet(constantes.CSS_MSG_CORRECTO) # restaura valores por defecto   