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
import os
from PyQt5 import QtCore, QtGui
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
        QtCore.QCoreApplication.processEvents()
        self.feedback_label.setText(mensaje)
        self.feedback_label.setStyleSheet(estilo)
        self.feedback_label.show()
        if temporal == True:
            QtCore.QTimer.singleShot(2000, self.restablecerMensajes)
            
    def restablecerMensajes(self):
        self.feedback_label.hide()
        self.feedback_label.setStyleSheet(constantes.CSS_MSG_CORRECTO) # restaura valores por defecto   
      
    # PROGRESO
    # ///////////////////////////////////////////////////////////    
    def ui_iniciar_progreso(self, guia, cantidad_pasos, calibracion):
        QtCore.QCoreApplication.processEvents()
        if calibracion:
            for i in range(0, cantidad_pasos):
                self.progreso_lineal[i].setStyleSheet("")
                self.progreso_grid[i].setStyleSheet("")   
        else:
            for i in range(0, 9):
                if i < cantidad_pasos:
                    if guia != 'Mantener':
                        self.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/target_v.png"))
                        self.progreso_grid[i].setPixmap(QtGui.QPixmap("img/target_h.png"))
                else:
                    self.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                    self.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))   
                self.progreso_lineal[i].setStyleSheet("")
                self.progreso_grid[i].setStyleSheet("")
        self.ui_siguiente_seleccion(0)

    def ui_siguiente_seleccion(self, siguiente_seleccion):
        QtCore.QCoreApplication.processEvents()
        if siguiente_seleccion != 0:
            self.progreso_lineal[siguiente_seleccion - 1].setStyleSheet("")
            self.progreso_grid[siguiente_seleccion - 1].setStyleSheet("")
                
        self.progreso_lineal[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
        self.progreso_grid[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
    
    def ui_mostrar_guia(self):
        pass
    
    def ui_actualizar_progreso(self, tipo_tarea, sesion, calibracion):
        QtCore.QCoreApplication.processEvents()
        if calibracion is True:
            if sesion.siguiente_seleccion < constantes.PASOS_CALIBRACION:
                self.ui_siguiente_seleccion(sesion.siguiente_seleccion)
            img = "img/paso_completado.png"
            
        else:
            if sesion.siguiente_seleccion < sesion.cantidad_pasos:
                self.ui_siguiente_seleccion(sesion.siguiente_seleccion)
                
            if tipo_tarea == 'Rompecabezas - mem. espacial':
                # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
                if os.path.isfile(sesion.ubicacion_img + "/img" + str(sesion.siguiente_seleccion) + ".png"):
                    extension = ".png"
                else:
                    extension = " - punto.png"
                img = sesion.ubicacion_img + "/img" + str(sesion.siguiente_seleccion) + extension
            else:
                img = sesion.ubicacion_img + "/img" + str(sesion.imagen_seleccionada) + ".png"
        
        p = QtGui.QPixmap(img)
        self.progreso_lineal[sesion.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.progreso_grid[sesion.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

    def ui_pasar(self, sesion, tipo_tarea):
        QtCore.QCoreApplication.processEvents()
        if tipo_tarea == 'Palabras - al revés':
            siguiente_seleccion = (sesion.cantidad_pasos + 1) - sesion.siguiente_seleccion
        else:
            siguiente_seleccion = sesion.siguiente_seleccion
        
        if sesion.siguiente_seleccion < sesion.cantidad_pasos:
                self.ui_siguiente_seleccion(sesion.siguiente_seleccion)
    
        # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
        if os.path.isfile(sesion.ubicacion_img + "/img" + str(siguiente_seleccion) + ".png"):
            extension = ".png"
        else:
            extension = " - punto.png"
                    
        img = sesion.ubicacion_img + "/img" + str(siguiente_seleccion) + extension
        p = QtGui.QPixmap(img)
        self.progreso_lineal[sesion.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.progreso_grid[sesion.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))        