### Cognitask ############################################################
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

from PyQt5 import QtCore, QtGui, QtWidgets ###############################
from PyQt5.QtWidgets import QFileDialog ##################################
from datetime import date ######################################
import subprocess ########################################################
import inspect ###########################################################
import os ################################################################

from modulos.BCI2000 import BCI2000
from modulos.aplicacion import BCIAplicacion #############################
from modulos.operador import BCIOperador #################################
import modulos.constantes as c
import modulos.procesos as procesos
import modulos.informacion as informacion
import modulos.progreso as progreso
import modulos.mensajes as mensajes
import modulos.temporizador as temporizador
import modulos.estados as estados
import modulos.parametros as parametros
from modulos.sesion import Sesion 

class Cognitask(QtWidgets.QMainWindow, BCIOperador):
   
    def __init__(self):
        super(Cognitask, self).__init__()
        
        # obtener la ubicacion de instalacion de Cognitask
        pyfile = inspect.getfile(inspect.currentframe())
        self.install_dir = os.path.dirname(os.path.realpath(pyfile))

        # Conexion con el modulo de Aplicacion
        self.Aplicacion = QtWidgets.QMainWindow()
        self.BCIAplicacion = BCIAplicacion()
        self.BCIAplicacion.__init__()
        
        # BCI2000
        self.bci = BCI2000()

        # Sesion
        self.sesion = Sesion()

        # Procesos
        procesos.incorporarMatriz(self) # introduce P3Speller dentro del modulo de Aplicacion Cognitask
        procesos.ocultarProcesos(self) # hace invisible los procesos de BCI2000

        QtCore.QCoreApplication.processEvents() 

        # comportamiento de botones
        self.configBotones()

        # variables de configuracion
        self.config = self.install_dir + "/config/config.prm"
        self.config_calibracion = self.install_dir + "/config/calibracion.prm"
        self.config_source = self.install_dir + "/config/" + c.ADQUISICION + ".prm"
        self.secuencia = self.install_dir + "/config/secuencia.prm"
        self.nivel = self.install_dir + "/config/nivel.prm"
        self.ubicacion_datos = self.install_dir + "\datos" # ubicacion de datos por defecto
        self.directorio_entrada.setPlaceholderText(self.ubicacion_datos)
        self.ubicacion_img = self.install_dir + "/sec/Rompecabezas/Musica" # por defecto
        self.matriz_clasificacion = ""
        self.modo_calibracion = False

        # variables de sesion
        self.sesion_estado = "No iniciada" # estado de la sesión. No iniciada, Preparado, Realizando, Completado
        self.orden_secuencia = list(range(1, 10))
        self.siguiente_seleccion = 1 # indica la imagen siguiente que debe elegirse
        self.imagen_seleccionada = 0 # imagen seleccionada (necesario debido al orden aleatorio de las imagenes)
        self.target_seleccionado = 0 # target seleccionado
        self.calibracion_tarea = 1 # permite cambiar entre las distintas tareas de calibración automaticamente
        self.cantidad_pasos = 9 # cantidad de pasos que contiene la tarea. Por defecto son 9 pasos
        self.mostrar_guia = True
        self.intentos = 0 # suma 1 cada vez que el sujeto se equivoca en la sesion de terapia
        self.run = 0
        self.actividad_completada = False
        self.sesion_iniciada = False # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma

        # temporizador
        self.tiempo_inicial = 0
        self.tiempo_sesion = 0
 
        # estados
        self.running = 0 # permite alternar entre comenzar y suspender una actividad
        self.bci_estado = 'Suspended'
        self.consultar_seleccion = True

        # resumen
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        self.porcentaje_aciertos = 0
                       
    # PAGINAS
    def nuevaSesionPagina(self):
        self.restablecerConfiguracion()
        self.sesion.restablecer()
        
        # interfaz
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.terapia_boton.setEnabled(False)
        self.calibracion_boton.setEnabled(False)
        self.configuracion_stacked_widget.setCurrentIndex(0)
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(255, 255, 255);")

        # informacion
        informacion.mostrar(self, "Nueva sesion")
    
    def calibracionPagina(self):
        self.restablecerConfiguracion()
        self.sesion.restablecer()
        
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.configuracion_stacked_widget.setCurrentIndex(1)
        self.seleccion_calibracion_frame.setStyleSheet("background-color:rgb(255,255,255);")

        informacion.mostrar(self, "Calibracion")
        
    def terapiaPagina(self):
        self.restablecerConfiguracion()
        self.sesion.restablecer()
        
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.configuracion_stacked_widget.setCurrentIndex(2)
        self.seleccion_terapia_frame.setStyleSheet("background-color:rgb(255,255,255);")

        informacion.mostrar(self, "Terapia")
    
    # NUEVA SESION

    def iniciarSesion(self):
        # Datos de sujeto y sesión
        if self.nombre_entrada.text() != "":
            # Datos de sujeto y sesión
            hoy = date.today().strftime("%d%m%y")
            self.bci.cargarDatos(self.nombre_entrada.text(), hoy, self.ubicacion_datos)
            self.configuracion_stacked_widget.setCurrentIndex(1)
            self.informacion_stacked_widget.setCurrentIndex(1)
            self.seleccion_calibracion_frame.setStyleSheet("background-color:rgb(255,255,255);")
            self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
            self.nueva_sesion_boton.setEnabled(True)
            self.calibracion_boton.setEnabled(True)
            self.terapia_boton.setEnabled(True)

    def seleccionarDirectorio(self):
        directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una carpeta:', 'C:/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.ubicacion_datos = directorio
            self.directorio_entrada.setText(self.ubicacion_datos)
    
    # CALIBRACION

    def aplicarConfigCalibracion(self):
        QtCore.QCoreApplication.processEvents() 
        
        # restablecer variables de sesion
        mensajes.restablecer(self)
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        
        self.modo_calibracion = True
        progreso.iniciar(self)
        parametros.aplicarSecuenciaCalibracion(self)
        self.bci.cargarParametros(self.config_calibracion)
        QtCore.QCoreApplication.processEvents() # evita que la gui se cuelgue cuando se cargan los parametros
        self.bci.cargarParametros(self.config_source)
        QtCore.QCoreApplication.processEvents() # evita que la gui se cuelgue cuando se cargan los parametros
        self.bci.cargarParametros(self.secuencia)
        self.BCIAplicacion.p3_frame.hide()
        parametros.aplicarNivel(self)

        self.bci.cargarParametros(self.nivel)

        if self.BCIAplicacion.Open == 0:
            self.BCIAplicacion.Open = 1
            self.BCIAplicacion.show()  
        
        self.bci.aplicarConfiguracion()
        self.BCIAplicacion.p3_frame.show()
        self.comenzar_terapia_boton.setEnabled(False)
        self.comenzar_calibracion_boton.setEnabled(True)
        self.sesion_estado = "Preparado"
        informacion.actualizar(self)
        informacion.mostrar(self, "Resumen")
        informacion.escribir(self, "sesion")
    
    def comenzarCalibracion(self):
        if self.running == 0: 
            self.bci.iniciar()
            self.deshabilitarCambios()
            self.running = 1
            mensajes.mostrar(self, c.MSG_COMENZAR, c.CSS_MSG_COMENZAR, True)
            
            if self.calibracion_tarea == 1:
                self.calibracion_estado_1.setText("Realizando ...")
            elif self.calibracion_tarea == 2:
                self.calibracion_estado_2.setText("Realizando ...")
            else:
                self.calibracion_estado_3.setText("Realizando ...")
            
            self.run += 1
            self.siguiente_seleccion = 1
            self.sesion_estado = "Realizando"
            progreso.iniciar(self)
            informacion.actualizar(self)
            temporizador.iniciar(self)
            informacion.escribir(self, "corrida")
        else:
            self.bci.suspender()
            self.habilitarCambios()
            self.running = 0
            self.sesion_estado = "Interrumpido"
            mensajes.mostrar(self, c.MSG_SUSPENDIDO, c.CSS_MSG_SUSPENDIDO, False)
            if self.calibracion_tarea == 1:
                self.calibracion_estado_1.setText("Esperando ...")
            elif self.calibracion_tarea == 2:
                self.calibracion_estado_2.setText("Esperando ...")
            else:
                self.calibracion_estado_3.setText("Esperando ...")
            informacion.escribir(self, "resumen") # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
         
        self.bci_estado = 'Running'
        estados.observar(self)

    def calibracionFinalizada(self):
        self.habilitarCambios()
        self.comenzar_calibracion_boton.setEnabled(False)
        self.running = 0
        mensajes.mostrar(self, c.MSG_TERMINADO, c.CSS_MSG_TERMINADO, False)
        
        p = QtGui.QPixmap("img/completado.png")
        if self.calibracion_tarea == 1:
            self.calibracion_estado_1.setText("Completado")
            self.calibracion_completada_1.setPixmap(QtGui.QPixmap(p))
            self.calibracion_tarea += 1
        elif self.calibracion_tarea == 2:
            self.calibracion_estado_2.setText("Completado")
            self.calibracion_completada_2.setPixmap(QtGui.QPixmap(p))
            self.calibracion_tarea += 1
        elif self.calibracion_tarea == 3:
            self.calibracion_estado_3.setText("Completado")
            self.calibracion_completada_3.setPixmap(QtGui.QPixmap(p))
            self.calibracion_tarea = 1
            self.preparar_calibracion_boton.setEnabled(False)
            self.clasificador_boton.setEnabled(True)
        self.actividad_completada = True
        self.sesion_estado = "Completado"
        informacion.escribir(self, "resumen")
        self.bci.ejecutar("Wait for Suspended 5")
        self.bci.suspender()
    
    # TERAPIA

    def aplicarConfigTerapia(self):
        QtCore.QCoreApplication.processEvents()
        
        # restablecer variables de sesion
        mensajes.restablecer(self)
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        self.intentos = 0

        self.modo_calibracion = False
        if self.guia_inicial_opciones.currentText() == "Habilitada":
            progreso.mostrarGuia(self)
        else:
            progreso.iniciar(self)
        parametros.aplicarSecuenciaTerapia(self)
        self.BCIAplicacion.p3_frame.hide()
        self.bci.cargarParametros(self.config)
        QtCore.QCoreApplication.processEvents() # evita que la gui se cuelgue cuando se cargan los parametros
        self.bci.cargarParametros(self.config_source)
        QtCore.QCoreApplication.processEvents() # evita que la gui se cuelgue cuando se cargan los parametros
        self.bci.cargarParametros(self.secuencia)
        parametros.aplicarNivel(self)
        
        self.sesion_estado = "Preparado"
        informacion.actualizar(self)
        informacion.mostrar(self, "Resumen")

        self.bci.cargarParametros(self.nivel)

        if self.matriz_clasificacion != "":
            self.bci.cargarParametros(self.matriz_clasificacion)
        
        if self.BCIAplicacion.Open == 0:
            self.BCIAplicacion.Open = 1
            self.BCIAplicacion.show()   

        QtCore.QCoreApplication.processEvents() # evita que la gui se cuelgue cuando se cargan los parametros
        self.bci.aplicarConfiguracion()
        self.BCIAplicacion.p3_frame.show()
        self.comenzar_terapia_boton.setEnabled(True)
        self.comenzar_calibracion_boton.setEnabled(False)
        informacion.escribir(self, "sesion")

    def comenzarTerapia(self):
        if self.bci_estado == 'Suspended': 
            self.bci.iniciar()
            self.bci_estado = 'Running'
            self.deshabilitarCambios()
            mensajes.mostrar(self, c.MSG_COMENZAR, c.CSS_MSG_COMENZAR, True)
            self.run += 1
            self.siguiente_seleccion = 1
            self.sesion_estado = "Realizando"
            progreso.iniciar(self)
            temporizador.iniciar(self)
            informacion.actualizar(self)
            informacion.escribir(self, "corrida")  
        else:
            self.bci.suspender()
            self.bci_estado = 'Suspended'
            self.habilitarCambios()
            mensajes.mostrar(self, c.MSG_SUSPENDIDO, c.CSS_MSG_SUSPENDIDO, False)
            self.sesion_estado = "Interrumpido"
            informacion.actualizar(self)
            informacion.escribir(self, "resumen") # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen   

        estados.observar(self)

    def seleccionarSecuencia(self):
        if self.modo_terapia_opciones.currentText() == "Rompecabezas":
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Rompecabezas/', QFileDialog.ShowDirsOnly)
        elif self.modo_terapia_opciones.currentText() == "Actividades":
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Actividades/', QFileDialog.ShowDirsOnly)
        else:
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Palabras/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.ubicacion_img = directorio
        
        # contamos la cantidad de pasos que contiene la secuencia elegida
        self.cantidad_pasos = sum(1 for item in os.listdir(self.ubicacion_img) if os.path.isfile(os.path.join(self.ubicacion_img, item)))

    def cargarMatrizClasificacion(self):
        clas = QFileDialog.getOpenFileName(self, "Seleccione el archivo de calibración: ", "C:/", "PRM (*.prm)")
        self.archivo_calibracion_entrada.setText(clas[0])
        self.matriz_clasificacion = clas[0]

    def terapiaFinalizada(self):
        self.bci.suspender()
        self.habilitarCambios()
        self.running = 0
        mensajes.mostrar(self, c.MSG_TERMINADO, c.CSS_MSG_TERMINADO, False)
        self.actividad_completada = True
        self.sesion_estado = "Completado"
        informacion.actualizar(self)
        # actualizamos tambien el porcentaje de aciertos
        self.porcentaje_aciertos = round((self.selecciones_correctas / self.selecciones_realizadas) * 100)

        informacion.escribir(self, "resumen")

        ## BCI2000
   
    ## OTRAS FUNCIONES

    def abrirP3Classifier(self):
        subprocess.Popen("BCI2000/P300Classifier/P300Classifier.exe")

    def configBotones(self):
        self.iniciar_sesion_boton.clicked.connect(self.iniciarSesion)
        self.aplicar_terapia_boton.clicked.connect(self.aplicarConfigTerapia)
        self.preparar_calibracion_boton.clicked.connect(self.aplicarConfigCalibracion)
        self.comenzar_terapia_boton.clicked.connect(self.comenzarTerapia)
        self.comenzar_calibracion_boton.clicked.connect(self.comenzarCalibracion)
        self.salir_boton.clicked.connect(self.salirCognitask)
        self.directorio_boton.clicked.connect(self.seleccionarDirectorio)
        self.nueva_sesion_boton.clicked.connect(self.nuevaSesionPagina)
        self.calibracion_boton.clicked.connect(self.calibracionPagina)
        self.terapia_boton.clicked.connect(self.terapiaPagina)
        self.modo_terapia_boton.clicked.connect(self.seleccionarSecuencia)
        self.archivo_calibracion_boton.clicked.connect(self.cargarMatrizClasificacion)
        self.clasificador_boton.clicked.connect(self.abrirP3Classifier)

    ## SALIR

    def salirCognitask(self):
        self.bci.terminar()
        del self.bci
        self.BCIAplicacion.close()
        Cognitask.close(self)