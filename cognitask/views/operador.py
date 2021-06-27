### Módulo de BCIOperador ###################################################
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

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui

from .ui_operador import Ui_BCIOperador
import cognitask.common.ubicaciones as ubicaciones
from cognitask.common import constantes

INDICE_NUEVA_SESION = 0
INDICE_CALIBRACION = 1
INDICE_TERAPIA = 2
INDICE_RESUMEN = 3

class BCIOperador(QMainWindow, Ui_BCIOperador):

    def __init__(self):
        super(BCIOperador, self).__init__()

    # FUNCIONES DE INTERFAZ GENERAL
    # ///////////////////////////////////////////////////////////
    def configuracionInicial(self):
            self.configuracion_stacked_widget.setCurrentIndex(0)
            self.informacion_stacked_widget.setCurrentIndex(0)
            self.nueva_sesion_boton.setEnabled(False)
            self.calibracion_boton.setEnabled(False)
            self.terapia_boton.setEnabled(False)
            self.comenzar_calibracion_boton.setEnabled(False)
            self.comenzar_terapia_boton.setEnabled(False)
            self.clasificador_boton.setEnabled(False)
            self.directorio_entrada.setPlaceholderText(ubicaciones.UBICACION_DATOS)
            
    def _deshabilitarCambios(self):
        self.comenzar_calibracion_boton.setText("Suspender")
        self.comenzar_terapia_boton.setText("Suspender")
        self.aplicar_terapia_boton.setEnabled(False)
        self.preparar_calibracion_boton.setEnabled(False)
        self.terapia_boton.setEnabled(False)
        self.calibracion_boton.setEnabled(False)
        self.salir_boton.setEnabled(False)
        self.nueva_sesion_boton.setEnabled(False)
        self.iniciar_sesion_boton.setEnabled(False)
        self.nombre_entrada.setEnabled(False)
        self.directorio_entrada.setEnabled(False)
        self.directorio_boton.setEnabled(False)
        self.clasificador_boton.setEnabled(False)
        self.tipo_tarea_opciones.setEnabled(False)
        self.tipo_tarea_boton.setEnabled(False)
        self.nivel_opciones.setEnabled(False)
        self.archivo_calibracion_entrada.setEnabled(False)
        self.archivo_calibracion_boton.setEnabled(False)
        self.guia_visual_opciones.setEnabled(False)

    def _habilitarCambios(self):
        self.comenzar_calibracion_boton.setText("Comenzar")
        self.comenzar_terapia_boton.setText("Comenzar")
        self.aplicar_terapia_boton.setEnabled(True)
        self.preparar_calibracion_boton.setEnabled(True)
        self.terapia_boton.setEnabled(True)
        self.calibracion_boton.setEnabled(True)
        self.salir_boton.setEnabled(True)
        self.nueva_sesion_boton.setEnabled(True)
        self.iniciar_sesion_boton.setEnabled(True)
        self.nombre_entrada.setEnabled(True)
        self.directorio_entrada.setEnabled(True)
        self.directorio_boton.setEnabled(True)
        self.tipo_tarea_opciones.setEnabled(True)
        self.tipo_tarea_boton.setEnabled(True)
        self.nivel_opciones.setEnabled(True)
        self.archivo_calibracion_entrada.setEnabled(True)
        self.archivo_calibracion_boton.setEnabled(True)
        self.guia_visual_opciones.setEnabled(True)

    # PAGINAS 
    # ///////////////////////////////////////////////////////////
    def ui_nuevaSesionPagina (self):
        # interfaz
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        
        self.nueva_sesion_boton.setEnabled(True)        
        self.terapia_boton.setEnabled(False)
        self.calibracion_boton.setEnabled(False)
        self.configuracion_stacked_widget.setCurrentIndex(0)
        
        self.nombre_entrada.setText("")
        
        # como empezar
        self._comoEmpezar(INDICE_NUEVA_SESION)
    
    def ui_calibracionPagina(self):
        # interfaz
        self.seleccion_calibracion_frame.setStyleSheet("background-color:rgb(255,255,255);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        
        self.nueva_sesion_boton.setEnabled(True)        
        self.terapia_boton.setEnabled(True)
        self.calibracion_boton.setEnabled(True)
        self.configuracion_stacked_widget.setCurrentIndex(1)
        
        self.calibracion_estado_1.setText("Realizar tarea de calibración Nro. 1")
        self.calibracion_estado_2.setText("Realizar tarea de calibración Nro. 2")
        self.calibracion_estado_3.setText("Realizar tarea de calibración Nro. 3")
        p = QtGui.QPixmap("img/completado_d.png")
        pr = p.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.calibracion_completada_1.setPixmap(QtGui.QPixmap(pr))
        self.calibracion_completada_2.setPixmap(QtGui.QPixmap(pr))
        self.calibracion_completada_3.setPixmap(QtGui.QPixmap(pr))
        self.comenzar_calibracion_boton.setEnabled(False)
        self.clasificador_boton.setEnabled(False)
        
        self._comoEmpezar(INDICE_CALIBRACION)
        
    def ui_terapiaPagina(self):
        # interfaz
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color:rgb(255,255,255);")
        
        self.nueva_sesion_boton.setEnabled(True)
        self.calibracion_boton.setEnabled(True)
        self.terapia_boton.setEnabled(True)
        
        self.configuracion_stacked_widget.setCurrentIndex(2)
        self.comenzar_terapia_boton.setEnabled(False)
        
        self._comoEmpezar(INDICE_TERAPIA)     
    
    def _comoEmpezar(self, pagina):
        self.informacion_titulo.setText("¿Cómo empezar?")
        self.informacion_stacked_widget.setCurrentIndex(pagina)
        
    # NUEVA SESION
    # ///////////////////////////////////////////////////////////
    def ui_seleccionarDirectorio(self, ubicacion_datos):
        self.directorio_entrada.setText(ubicacion_datos)

    @property # GETTER
    def paciente(self):
        return self.nombre_entrada.text()
    # CALIBRACION
    # ///////////////////////////////////////////////////////////
    def ui_prepararCalibracion(self, paciente):
        self.comenzar_terapia_boton.setEnabled(False)
        self.comenzar_calibracion_boton.setEnabled(True)
        self._mostrarResumen(paciente, INDICE_RESUMEN)
        
    def ui_comenzarCalibracion(self, calibracion_tarea):
        self._deshabilitarCambios()
        if calibracion_tarea == 1:
                self.calibracion_estado_1.setText(constantes.MSG_REALIZANDO_TAREA)
        elif calibracion_tarea == 2:
                self.calibracion_estado_2.setText(constantes.MSG_REALIZANDO_TAREA)
        else:
                self.calibracion_estado_3.setText(constantes.MSG_REALIZANDO_TAREA)
    
    def ui_suspenderCalibracion(self, calibracion_tarea):
        self._habilitarCambios()
        if calibracion_tarea == 1:
                self.calibracion_estado_1.setText(constantes.MSG_TAREA_SUSPENDIDA)
        elif calibracion_tarea == 2:
                self.calibracion_estado_2.setText(constantes.MSG_TAREA_SUSPENDIDA)
        else:
                self.calibracion_estado_3.setText(constantes.MSG_TAREA_SUSPENDIDA)
    
    def ui_finalizarCalibracion(self, calibracion_tarea):
        self._habilitarCambios()
        self.comenzar_calibracion_boton.setEnabled(False)
        p = QtGui.QPixmap("img/completado.png")
        if calibracion_tarea == 1:
            self.calibracion_estado_1.setText(constantes.MSG_TAREA_FINALIZADA)
            self.calibracion_completada_1.setPixmap(QtGui.QPixmap(p))
        elif calibracion_tarea == 2:
            self.calibracion_estado_2.setText(constantes.MSG_TAREA_FINALIZADA)
            self.calibracion_completada_2.setPixmap(QtGui.QPixmap(p))
        elif calibracion_tarea == 3:
            self.calibracion_estado_3.setText(constantes.MSG_TAREA_FINALIZADA)
            self.calibracion_completada_3.setPixmap(QtGui.QPixmap(p))
            self.preparar_calibracion_boton.setEnabled(False)
            self.clasificador_boton.setEnabled(True)

    # TERAPIA
    # ///////////////////////////////////////////////////////////
    @property # GETTER
    def tipoTarea(self):
        return self.tipo_tarea_opciones.currentText()
    
    @property # GETTER
    def nivel(self):
        return self.nivel_opciones.currentText()
    
    @property # GETTER
    def guiaVisual(self):
        return self.guia_visual_opciones.currentText()
    
    def ui_aplicarTerapia(self, paciente):
        self.comenzar_terapia_boton.setEnabled(True)
        self.comenzar_calibracion_boton.setEnabled(False)
        self._mostrarResumen(paciente, INDICE_RESUMEN)
    
    def ui_cargarMatriz(self, matriz):
        self.archivo_calibracion_entrada.setText(matriz[0])
    
    def ui_comenzarTerapia(self):
        self._deshabilitarCambios()
    
    def ui_suspenderTerapia(self):
        self._habilitarCambios()
        
    def ui_finalizarTerapia(self):
        self._habilitarCambios()
    
    # RESUMEN SESION
    # ///////////////////////////////////////////////////////////
    def _mostrarResumen(self, titulo, pagina):
        self.informacion_titulo.setText(titulo)
        self.informacion_stacked_widget.setCurrentIndex(pagina)
    
    def ui_iniciarResumen(self, modo, tarea):
        self.modo_resumen_texto.setText(modo)
        self.actividad_resumen_titulo.setText('Tarea')
        if modo == 'Terapia':
            self.actividad_resumen_titulo.setText(self.tipoTarea)
        self.actividad_resumen_texto.setText(tarea)
        self.nivel_resumen_texto.setText(self.nivel)
        
        self.selecciones_resumen_texto.setText('-')
        self.correctas_resumen_texto.setText('-')
        self.incorrectas_resumen_texto.setText('-')
        
        self.estado_resumen_texto.setText('No iniciado')
        
    def ui_actualizarSelecciones(self, selecciones, correctas, incorrectas):
        self.selecciones_resumen_texto.setText(str(selecciones))
        self.correctas_resumen_texto.setText(str(correctas))
        self.incorrectas_resumen_texto.setText(str(incorrectas))
        
    def ui_actualizarEstado(self, estado):
        self.estado_resumen_texto.setText(estado)
        
    def ui_actualizarTiempo(self, tiempo_sesion):
        self.tiempo_resumen_texto.setText(str(tiempo_sesion.minute).zfill(2) + ' min ' + str(tiempo_sesion.second).zfill(2) + ' s')