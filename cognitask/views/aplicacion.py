### Cognitask ############################################################
##########################################################################
## Autor: Facundo Barreto ### facubrt@outlook.com ########################
##                                                                      ##
## Sistema para rehabilitación cognitiva basado en BCI por P300 ##########
##                                                                      ##
## Pagina del proyecto ### https://facubrt.github.io/cognitask ###########
##                                                                      ##
## Proyecto Final de Bioingeniería ### 2021 ##############################
##########################################################################
##########################################################################

import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow

from .ui_aplicacion import Ui_BCIAplicacion
import cognitask.common.constantes as constantes
import cognitask.common.ubicaciones as ubicaciones

# GLOBAL_STATE = 0

class BCIAplicacion(QMainWindow, Ui_BCIAplicacion):
    
    def __init__(self):
        '''------------
        DOCUMENTACIÓN -
        Inicializa el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        ------------'''
        super(BCIAplicacion, self).__init__()
    
    def cerrarAplicacion(self):
        '''------------
        DOCUMENTACIÓN -
        Cierra el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        ------------'''
        self.Open = 0
        self.close()
         
    def ocultarMatriz(self):
        '''------------
        DOCUMENTACIÓN -
        Oculta la matriz de estimulacion en el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        ------------'''
        self.p3_frame.hide() 
    
    def mostrarMatriz(self):
        '''------------
        DOCUMENTACIÓN -
        Muestra la matriz de estimulacion en el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        ------------'''
        if self.Open == 0:
            self.Open = 1
            self.show()
        self.p3_frame.show()
        
    # MENSAJES
    # ///////////////////////////////////////////////////////////
    def mostrarMensajes(self, mensaje, estilo, temporal):
        '''------------
        DOCUMENTACIÓN -
        Muestra el area de mensaje en el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        - Permite que este area sea solo visible por un tiempo
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.feedback_label.setText(mensaje)
        self.feedback_label.setStyleSheet(estilo)
        self.feedback_label.show()
        if temporal == True:
            QtCore.QTimer.singleShot(2000, self.restablecerMensajes)
            
    def restablecerMensajes(self):
        '''------------
        DOCUMENTACIÓN -
        Restablece el area de mensaje en el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        ------------'''
        self.feedback_label.hide()
        self.feedback_label.setStyleSheet(constantes.CSS_MSG_CORRECTO) # restaura valores por defecto   
      
    # PROGRESO
    # ///////////////////////////////////////////////////////////    
    def ui_iniciar_progreso(self, guia, cantidad_pasos, calibracion):
        '''------------
        DOCUMENTACIÓN -
        Inicia el progreso en el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        ------------'''
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
        '''------------
        DOCUMENTACIÓN -
        Indica la seleccion siguiente en el area de progreso en el modulo de Aplicacion (Interfaz de usuario Paciente) de Cognitask.
        - Marca con un borde la seleccion siguiente
        ------------'''
        QtCore.QCoreApplication.processEvents()
        if siguiente_seleccion != 0:
            self.progreso_lineal[siguiente_seleccion - 1].setStyleSheet("")
            self.progreso_grid[siguiente_seleccion - 1].setStyleSheet("")
                
        self.progreso_lineal[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
        self.progreso_grid[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
    
    def ui_mostrar_guia_calibracion(self, sesion):
        '''------------
        DOCUMENTACIÓN -
        Muestra la guia en el area de progreso para una sesion de calibracion.
        - Muestra el orden correcto de las imagenes antes de comenzar con la estimulacion visual
        ------------'''
        if sesion.indice_tarea == 1:
            ubicacion_img = ubicaciones.UBICACION_TAREA1
        elif sesion.indice_tarea == 2:
            ubicacion_img = ubicaciones.UBICACION_TAREA2
        elif sesion.indice_tarea == 3:
            ubicacion_img = ubicaciones.UBICACION_TAREA3
    
        for i in range(0, 9):  
            if i < constantes.PASOS_CALIBRACION:
                extension = ".png"
                img = ubicacion_img + "/img" + str(i+1) + extension
                
                new_pix = QtGui.QPixmap(img)
                new_pix.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(new_pix)
                painter.setOpacity(0.2)
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.end()
                
                self.progreso_lineal[i].setPixmap(new_pix)
                self.progreso_grid[i].setPixmap(new_pix)
                self.progreso_lineal[i].setStyleSheet("")
                self.progreso_grid[i].setStyleSheet("")
                    
            else:
                self.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                self.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png")) 
        
        self.ui_siguiente_seleccion(0) 
    
    def ui_mostrar_guia_terapia(self, sesion):
        '''------------
        DOCUMENTACIÓN -
        Muestra la guia en el area de progreso para una sesion de terapia.
        - Muestra el orden correcto de las imagenes antes de comenzar con la estimulacion visual.
        - Permite mantener la guia durante la realizacion de la tarea
        ------------'''
         
        for i in range(0, 9):
            self.progreso_lineal[i].setStyleSheet("")
            self.progreso_grid[i].setStyleSheet("")
            if i < sesion.cantidad_pasos:
                # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
                if os.path.isfile(sesion.ubicacion_img + "/img" + str(i+1) + ".png"):
                    extension = ".png"
                else:
                    extension = " - punto.png"
                
                img = sesion.ubicacion_img + "/img" + str(i+1) + extension
                
                new_pix = QtGui.QPixmap(img)
                new_pix.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(new_pix)
                painter.setOpacity(0.2)
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.end()
                
                self.progreso_lineal[i].setPixmap(new_pix)
                self.progreso_grid[i].setPixmap(new_pix)
                self.progreso_lineal[i].setStyleSheet("")
                self.progreso_grid[i].setStyleSheet("")
                    
            else:
                self.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                self.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  
        
        self.ui_siguiente_seleccion(0) 
    
    def ui_actualizar_progreso(self, tipo_tarea, sesion, calibracion):
        '''------------
        DOCUMENTACIÓN -
        Actualiza el progreso de la tarea.
        - Carga la imagen seleccionada en el area de progreso
        ------------'''
        QtCore.QCoreApplication.processEvents()
        if calibracion is True:
            if sesion.siguiente_seleccion < constantes.PASOS_CALIBRACION:
                self.ui_siguiente_seleccion(sesion.siguiente_seleccion)
            img = "img/paso_completado.png"
            
        else:
            if sesion.siguiente_seleccion < sesion.cantidad_pasos:
                self.ui_siguiente_seleccion(sesion.siguiente_seleccion)
                
            if tipo_tarea == 'Bloque C2':
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
        '''------------
        DOCUMENTACIÓN -
        Actualiza el area de progreso luego de equivocarse un numero de intentos determinados.
        - Pasa a la siguiente seleccion.
        ------------'''
        QtCore.QCoreApplication.processEvents()
        if tipo_tarea == 'Bloque B2':
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