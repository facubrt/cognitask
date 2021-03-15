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
from PyQt5.QtGui import QImage ###########################################
from PyQt5.QtWidgets import QFileDialog ##################################
from datetime import date, datetime ######################################
import win32process ######################################################
import random ############################################################
import subprocess ########################################################
import win32gui ##########################################################
import inspect ###########################################################
import time ##############################################################
import sys ###############################################################
import os ################################################################
import re ################################################################

from BCI2000.prog.BCI2000Remote import BCI2000Remote #####################
from modulos.aplicacion import BCIAplicacion #############################
from modulos.operador import BCIOperador #################################
from modulos.splash import Splash ########################################

##########################################################################
# IMPORTANTE, ANTES DE PONER A PRUEBA MODIFICAR:
# numero de secuencias en calibración,
# numero de secuencias en niveles de terapia
# modulos_bci.txt

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
        
        # Conexion con BCI2000Remote
        self.bci = BCI2000Remote()
        self.bci.WindowVisible = False # hace invisible el operador de BCI2000
        self.modulos = ("Adquisicion", "Procesamiento", "Aplicacion")
        self.IniciarModulosBCI2000() # permite modificar los modulos posteriormente a traves de modulos_bci.txt
        self.bci.Connect()
        self.bci.StartupModules(self.modulos) # inicializa los modulos de BCI2000
        self.InWindow() # introduce P3Speller dentro del modulo de Aplicacion Cognitask
        self.BCIAplicacion.setWindowFlag(QtCore.Qt.FramelessWindowHint) # Frameless Window
        self.OcultarProcesos() # hace invisible los procesos de BCI2000
        QtCore.QCoreApplication.processEvents() 

        # comportamiento de botones
        self.iniciar_sesion_boton.clicked.connect(self.IniciarSesion)
        self.aplicar_terapia_boton.clicked.connect(self.AplicarConfigTerapia)
        self.preparar_calibracion_boton.clicked.connect(self.AplicarConfigCalibracion)
        self.comenzar_terapia_boton.clicked.connect(self.ComenzarTerapia)
        self.comenzar_calibracion_boton.clicked.connect(self.ComenzarCalibracion)
        self.salir_boton.clicked.connect(self.SalirCognitask)
        self.directorio_boton.clicked.connect(self.SeleccionarDirectorio)
        self.nueva_sesion_boton.clicked.connect(self.NuevaSesionPagina)
        self.calibracion_boton.clicked.connect(self.CalibracionPagina)
        self.terapia_boton.clicked.connect(self.TerapiaPagina)
        self.modo_terapia_boton.clicked.connect(self.SeleccionarSecuencia)
        self.archivo_calibracion_boton.clicked.connect(self.AplicarMatrizClasificacion)
        self.clasificador_boton.clicked.connect(self.AbrirP3Classifier)

        # variables de configuracion
        self.config = self.install_dir + "/config/config.prm"
        self.config_calibracion = self.install_dir + "/config/calibracion.prm"
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
        self.cantidad_pasos = 9 # cantidad de pasos que contiene la actividad. Por defecto son 9 pasos
        self.mostrar_guia = True

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
        
        self.run = 0
        self.actividad_completada = False
        self.sesion_iniciada = False # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma
                       
    ## COMPORTAMIENTO DE APLICACION

    def NuevaSesionPagina(self):
        self.RestablecerConfiguracion()
        self.sesion_iniciada = False # debido a que se cambia de tipo de terapia, se vuelve a escribir la seccion de sesión
        self.run = 0
        self.terapia_boton.setEnabled(False)
        self.calibracion_boton.setEnabled(False)
        self.configuracion_stacked_widget.setCurrentIndex(0)
        self.MostrarInformacion("Nueva sesion")
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(255, 255, 255);")

    def CalibracionPagina(self):
        self.RestablecerConfiguracion()
        self.sesion_iniciada = False # debido a que se cambia de tipo de terapia, se vuelve a escribir la seccion de sesión
        self.run = 0
        self.configuracion_stacked_widget.setCurrentIndex(1)
        self.MostrarInformacion("Calibracion")
        self.seleccion_calibracion_frame.setStyleSheet("background-color:rgb(255,255,255);")
        self.seleccion_terapia_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")

    def TerapiaPagina(self):
        self.RestablecerConfiguracion()
        self.sesion_iniciada = False # debido a que se cambia de tipo de terapia, se vuelve a escribir la seccion de sesión
        self.run = 0
        self.configuracion_stacked_widget.setCurrentIndex(2)
        self.MostrarInformacion("Terapia")
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color:rgb(255,255,255);")


    def IniciarSesion(self):
        # Datos de sujeto y sesión
        if self.nombre_entrada.text() != "":
            self.bci.SubjectID = self.nombre_entrada.text()
            today = date.today()
            hoy = today.strftime("%d%m%y")
            self.bci.SessionID = hoy
            self.bci.DataDirectory = self.ubicacion_datos
            self.configuracion_stacked_widget.setCurrentIndex(1)
            self.informacion_stacked_widget.setCurrentIndex(1)
            self.seleccion_calibracion_frame.setStyleSheet("background-color:rgb(255,255,255);")
            self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
            self.nueva_sesion_boton.setEnabled(True)
            self.calibracion_boton.setEnabled(True)
            self.terapia_boton.setEnabled(True)


    def AplicarConfigTerapia(self):
        QtCore.QCoreApplication.processEvents()
        
        # restablecer variables de sesion
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0

        self.modo_calibracion = False
        if self.guia_inicial_opciones.currentText() == "Habilitada":
            self.MostrarGuia()
        else:
            self.IniciarProgreso()
        self.AplicarSecuencia()
        self.BCIAplicacion.p3_frame.hide()
        self.bci.LoadParametersRemote(self.config)
        self.bci.LoadParametersRemote(self.secuencia)
        self.AplicarNivel()
        
        self.sesion_estado = "Preparado"
        self.ActualizarResumen()
        self.MostrarInformacion("Resumen")

        self.bci.LoadParametersRemote(self.nivel)

        if self.matriz_clasificacion != "":
            self.bci.LoadParametersRemote(self.matriz_clasificacion)
        
        if self.BCIAplicacion.Open == 0:
            self.BCIAplicacion.Open = 1
            self.BCIAplicacion.show()   

        self.bci.SetConfig()
        self.BCIAplicacion.p3_frame.show()
        self.comenzar_terapia_boton.setEnabled(True)
        self.comenzar_calibracion_boton.setEnabled(False)
        self.EscribirResumen(1)
    
    def AplicarConfigCalibracion(self):
        QtCore.QCoreApplication.processEvents() 
        self.siguiente_seleccion = 1
        self.modo_calibracion = True
        self.IniciarProgreso()
        self.AplicarSecuenciaCalibracion()
        self.bci.LoadParametersRemote(self.config_calibracion)
        self.bci.LoadParametersRemote(self.secuencia)
        self.BCIAplicacion.p3_frame.hide()

        if self.BCIAplicacion.Open == 0:
            self.BCIAplicacion.Open = 1
            self.BCIAplicacion.show()  
        
        self.bci.SetConfig()
        self.BCIAplicacion.p3_frame.show()
        self.comenzar_terapia_boton.setEnabled(False)
        self.comenzar_calibracion_boton.setEnabled(True)
        self.EscribirResumen(1)

    def ComenzarTerapia(self):
        if self.bci_estado == 'Suspended': 
            self.bci.Start()
            self.bci_estado = 'Running'
            self.DeshabilitarCambios()
            self.BCIAplicacion.feedback_label.setText("Comencemos!")
            self.BCIAplicacion.feedback_label.show()
            self.BCIAplicacion.feedback_label.setWindowOpacity
            QtCore.QTimer.singleShot(2000, self.msgOcultar)
            self.run += 1
            self.siguiente_seleccion = 1
            self.IniciarProgreso()
            self.IniciarTiempo()
            self.sesion_estado = "Realizando"
            self.ActualizarResumen()
            self.EscribirResumen(2)  
        else:
            self.bci.Stop()
            self.bci_estado = 'Suspended'
            self.HabilitarCambios()
            self.BCIAplicacion.feedback_label.setText("Espera un momento...")
            self.BCIAplicacion.feedback_label.show()
            self.sesion_estado = "Interrumpido"
            self.ActualizarResumen()
            self.EscribirResumen(3) # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen   

        self.Observar()
    
    def ComenzarCalibracion(self):
        if self.running == 0: 
            self.bci.Start()
            self.DeshabilitarCambios()
            self.running = 1
            self.BCIAplicacion.feedback_label.setText("Comencemos!")
            if self.calibracion_tarea == 1:
                self.calibracion_estado_1.setText("Realizando ...")
            elif self.calibracion_tarea == 2:
                self.calibracion_estado_2.setText("Realizando ...")
            else:
                self.calibracion_estado_3.setText("Realizando ...")
            self.BCIAplicacion.feedback_label.show()
            QtCore.QTimer.singleShot(2000, self.msgOcultar)
            self.run += 1
            self.siguiente_seleccion = 1
            self.IniciarProgreso()
            self.EscribirResumen(2)
        else:
            self.bci.Stop()
            self.HabilitarCambios()
            self.running = 0
            self.BCIAplicacion.feedback_label.setText("Espera un momento...")
            if self.calibracion_tarea == 1:
                self.calibracion_estado_1.setText("Esperando ...")
            elif self.calibracion_tarea == 2:
                self.calibracion_estado_2.setText("Esperando ...")
            else:
                self.calibracion_estado_3.setText("Esperando ...")
            self.BCIAplicacion.feedback_label.show()
            self.EscribirResumen(3) # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
         
        self.bci_estado = 'Running'
        self.Observar()


    def Feedback(self):
        # modo terapia
        if self.imagen_seleccionada == self.siguiente_seleccion and self.siguiente_seleccion != self.cantidad_pasos and self.modo_calibracion == False:
            self.BCIAplicacion.feedback_label.setText("Elegiste bien!")
            self.BCIAplicacion.feedback_label.show()
            QtCore.QTimer.singleShot(2000, self.msgOcultar)
            self.ActualizarProgreso()
            self.selecciones_correctas += 1
            self.selecciones_realizadas += 1
            self.siguiente_seleccion = self.siguiente_seleccion + 1

        elif self.imagen_seleccionada == self.siguiente_seleccion and self.siguiente_seleccion == self.cantidad_pasos and self.modo_calibracion == False:
            self.ActualizarProgreso()
            self.selecciones_correctas += 1
            self.selecciones_realizadas += 1
            self.ActualizarResumen()
            self.TerapiaFinalizada()
        
        elif self.imagen_seleccionada != self.siguiente_seleccion and self.modo_calibracion == False:
            self.BCIAplicacion.feedback_label.setText("Casi! Vuelve a intentar")
            self.BCIAplicacion.feedback_label.setStyleSheet("color: rgb(242, 242, 242);border-color: rgb(0, 0, 0);border-radius: 6px;"
            "background-color: rgb(234, 86, 61)")
            self.BCIAplicacion.feedback_label.show()
            QtCore.QTimer.singleShot(2000, self.msgOcultar)
            self.selecciones_incorrectas += 1
            self.selecciones_realizadas += 1
        
        # modo calibracion
        if self.modo_calibracion == True and self.siguiente_seleccion != 9:
            if self.imagen_seleccionada != self.siguiente_seleccion:
                self.selecciones_incorrectas += 1
            else:
                self.selecciones_correctas += 1
            self.ActualizarProgreso()
            self.siguiente_seleccion = self.siguiente_seleccion + 1
            self.selecciones_realizadas += 1

        elif self.modo_calibracion == True and self.siguiente_seleccion == 9:
            if self.imagen_seleccionada != self.siguiente_seleccion:
                self.selecciones_incorrectas += 1
            else:
                self.selecciones_correctas += 1
            self.selecciones_realizadas += 1
            self.ActualizarProgreso()
            self.CalibracionFinalizada()

        self.ActualizarResumen() # informa al operador de la seleccion

    def MostrarGuia(self):
        # queda ver si se puede poner opacidad en las imagenes de guia. También debería hacerse para calibracion
        for i in range(0, 9):
            if i < self.cantidad_pasos:
                img = self.ubicacion_img + "/img" + str(i+1) + ".png"
                p = QtGui.QPixmap(img)
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(p))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(p))
            else:
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  

    def MostrarInformacion(self, informacion):
        if (informacion == "Nueva sesion"):
            self.informacion_titulo.setText("¿Cómo empezar?")
            self.informacion_stacked_widget.setCurrentIndex(0)
        elif (informacion == "Calibracion"):
            self.informacion_titulo.setText("¿Cómo empezar?")
            self.informacion_stacked_widget.setCurrentIndex(1)
        elif (informacion == "Terapia"):
            self.informacion_titulo.setText("¿Cómo empezar?")
            self.informacion_stacked_widget.setCurrentIndex(2)
        elif (informacion == "Resumen"):
            self.informacion_titulo.setText(self.bci.SubjectID)
            self.informacion_stacked_widget.setCurrentIndex(3)

    def ActualizarResumen(self):
        if (self.sesion_estado == "Preparado"):
            self.modo_resumen_texto.setText(self.modo_terapia_opciones.currentText())
            if (self.modo_terapia_opciones.currentText() == "Rompecabezas"):
                self.actividad_resumen_titulo.setText("Imagen")
            elif (self.modo_terapia_opciones.currentText() == "Actividades"):
                self.actividad_resumen_titulo.setText("Actividad")
            elif (self.modo_terapia_opciones.currentText() == "Palabras"):
                self.actividad_resumen_titulo.setText("Palabra")
            self.actividad_resumen_texto.setText(os.path.basename(self.ubicacion_img))
            self.nivel_resumen_texto.setText(self.nivel_opciones.currentText())
            self.selecciones_resumen_texto.setText(str(self.selecciones_realizadas))
            self.correctas_resumen_texto.setText(str(self.selecciones_correctas))
            self.incorrectas_resumen_texto.setText(str(self.selecciones_incorrectas))
            self.estado_resumen_texto.setText("Preparado")
        elif (self.sesion_estado == "Realizando"):
            self.selecciones_resumen_texto.setText(str(self.selecciones_realizadas))
            self.correctas_resumen_texto.setText(str(self.selecciones_correctas))
            self.incorrectas_resumen_texto.setText(str(self.selecciones_incorrectas))
            self.estado_resumen_texto.setText("Realizando")
        elif (self.sesion_estado == "Completado"):
            self.estado_resumen_texto.setText("Completado")
        elif (self.sesion_estado == "Interrumpido"):
            self.estado_resumen_texto.setText("Interrumpido")

    def IniciarProgreso(self):
        
        if self.modo_calibracion == False:
            for i in range(0, 9):
                if i < self.cantidad_pasos:
                    self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/target_v.png"))
                    self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/target_h.png"))
                else:
                    self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                    self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))
        
        if self.modo_calibracion == True and self.calibracion_tarea == 1:
            for i in range(0, 9):
                img = "calibracion/tarea 1/dimg" + str(i+1) + ".png"
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))
        
        if self.modo_calibracion == True and self.calibracion_tarea == 2:
            for i in range(0, 9):
                img = "calibracion/tarea 2/dimg" + str(i+1) + ".png"
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))

        if self.modo_calibracion == True and self.calibracion_tarea == 3:
            for i in range(0, 9):
                img = "calibracion/tarea 3/dimg" + str(i+1) + ".png"
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))

    def ActualizarProgreso(self):

        if self.modo_calibracion == False:
            if self.siguiente_seleccion < self.cantidad_pasos:
                self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_v.png"))
                self.BCIAplicacion.progreso_grid[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_h.png"))
            img = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"
            p = QtGui.QPixmap(img)
            self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
            self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        
        if self.modo_calibracion == True:
            img = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"
            p = QtGui.QPixmap(img)
            self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
            self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

    def TerapiaFinalizada(self):
        self.bci.Stop()
        self.HabilitarCambios()
        self.running = 0
        self.BCIAplicacion.feedback_label.setText("Has terminado!")
        self.BCIAplicacion.feedback_label.show()
        self.actividad_completada = True
        self.sesion_estado = "Completado"
        self.ActualizarResumen()
        # actualizamos tambien el porcentaje de aciertos
        self.porcentaje_aciertos = round((self.selecciones_correctas / self.selecciones_realizadas) * 100)

        self.EscribirResumen(3)

    def CalibracionFinalizada(self):
        self.bci.Stop()
        self.HabilitarCambios()
        self.comenzar_calibracion_boton.setEnabled(False)
        self.running = 0
        self.BCIAplicacion.feedback_label.setText("Has terminado!")
        self.BCIAplicacion.feedback_label.show()
        p = QtGui.QPixmap("img/completado.png")
        if self.calibracion_tarea == 1:
            print('tarea 1')
            self.calibracion_estado_1.setText("Completado")
            self.calibracion_completada_1.setPixmap(QtGui.QPixmap(p))
            self.calibracion_tarea += 1
        elif self.calibracion_tarea == 2:
            print('tarea 2')
            self.calibracion_estado_2.setText("Completado")
            self.calibracion_completada_2.setPixmap(QtGui.QPixmap(p))
            self.calibracion_tarea += 1
        elif self.calibracion_tarea == 3:
            print('tarea 3')
            self.calibracion_estado_3.setText("Completado")
            self.calibracion_completada_3.setPixmap(QtGui.QPixmap(p))
            self.calibracion_tarea = 1
            self.preparar_calibracion_boton.setEnabled(False)
            self.clasificador_boton.setEnabled(True)
        self.actividad_completada = True
        self.EscribirResumen(3)


    def EscribirResumen(self, indice):
        QtCore.QCoreApplication.processEvents()
        path = self.ubicacion_datos + "/" + self.bci.SubjectID + "/resumen_sesiones.txt" 
        file_exists = os.path.isfile(path)
        fout = open(path, "a") 
        if not file_exists:  
            header = "Resumen de todas las sesiones [" + self.bci.SubjectID + "]\n"
            fout.write(header)
            #montaje = "Electrodos utilizados ---[Fz Cz Pz PO7 PO8 Oz]\n"
            #fout.write(montaje)
        if indice == 1:
            today = date.today()
            d = today.strftime("%d-%m-%y")
            if self.modo_calibracion == True and self.sesion_iniciada == False:
                sesion = "\n--- Sesión del día " + d + " [CALIBRACIÓN] ---\n"
                fout.write(sesion)
                self.sesion_iniciada = True
            elif self.modo_calibracion == False and self.sesion_iniciada == False:
                sesion = "\n--- Sesión del día " + d + " [TERAPIA] ---\n"
                fout.write(sesion)
                matriz_text = "\nMatriz de clasificación ---\n"
                fout.write(matriz_text)
                matriz = self.bci.GetMatrixParameter("Classifier") # me dice la matriz usada en la corrida
                for c in range(len(matriz)):
                    m = str(matriz[c][0]) + " " + str(matriz[c][1]) + " " + str(matriz[c][2]) + " " + str(matriz[c][3]) + "\n"
                    fout.write(m)
                self.sesion_iniciada = True 
        elif indice == 2:
            r = "\n--------------- Corrida R" + str(self.run).zfill(2) + "\n"
            fout.write(r)
            if self.modo_calibracion == True:
                sec = "\n[Tarea Nro. " + str(self.calibracion_tarea) + "]\n"
                fout.write(sec)
            else:
                modo = "\nModo ------- [" + self.modo_terapia_opciones.currentText() + "]\n"
                fout.write(modo)
                if (self.modo_terapia_opciones.currentText() == "Rompecabezas"):
                    sec = "Imagen ----- [" + os.path.basename(self.ubicacion_img) + "]\n"
                elif (self.modo_terapia_opciones.currentText() == "Actividades"):
                    sec = "Actividad -- [" + os.path.basename(self.ubicacion_img) + "]\n"
                elif (self.modo_terapia_opciones.currentText() == "Palabras"):
                    sec = "Palabra ---- [" + os.path.basename(self.ubicacion_img) + "]\n"
                fout.write(sec)
                n = "Nivel ------ [" + self.nivel_opciones.currentText() + "]\n"
                fout.write(n)
        elif indice == 3:
            act = "\nACTIVIDAD INTERRUMPIDA -"
            if self.actividad_completada == True:
                act = "\nACTIVIDAD COMPLETADA ---" 
            fout.write(act)
            tiempo = "\nDuración ------[" + str(self.tiempo_sesion.minute).zfill(2) + ' min ' + str(self.tiempo_sesion.second).zfill(2) + ' s' + "]"
            fout.write(tiempo)
            selecciones = "\nSelecciones realizadas  [" + str(self.selecciones_realizadas).zfill(2) + "]"
            fout.write(selecciones)
            correctas = "\nSelecciones correctas   [" + str(self.selecciones_correctas).zfill(2) + "]"
            fout.write(correctas)
            incorrectas = "\nSelecciones incorrectas [" + str(self.selecciones_incorrectas).zfill(2) + "]\n"
            fout.write(incorrectas)
            aciertos = "\nPorcentaje de aciertos [" + str(self.porcentaje_aciertos) + "%]\n"
            fout.write(aciertos)
        fout.close()


    def SalirCognitask(self):
        self.bci.Quit()
        self.BCIAplicacion.close()
        Cognitask.close(self)

    ## OBSERVACION DE ESTADOS DE BCI2000

    def Observar(self):
        while self.bci_estado == 'Running':
            self.ActualizarTiempo()  # la actualización se realiza en este lugar para aprovechar el while de Observacion
            QtCore.QCoreApplication.processEvents()
            starget = self.bci.GetStateVariable('SelectedTarget') # me da el numero de target seleccionado (1 a 9)
            starget = int(starget)

            if starget != 0 and self.consultar_seleccion == True:
                self.imagen_seleccionada = self.orden_secuencia[starget-1] # con esto puedo conocer que imagen se encuentra en este target (necesario debido al orden aleatorio de las imagenes)
                self.target_seleccionado = starget
                self.Feedback()
                self.consultar_seleccion = False

            elif starget == 0 and self.consultar_seleccion == False:
                self.consultar_seleccion = True
            self.bci_estado = self.bci.GetSystemState()
    
    ## CONFIGURACION DE LA SESION

    def AbrirP3Classifier(self):
        subprocess.Popen("BCI2000/P300Classifier.exe")

    def SeleccionarDirectorio(self):
        directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una carpeta:', 'C:/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.ubicacion_datos = directorio
            self.directorio_entrada.setText(self.ubicacion_datos)
            
    def SeleccionarSecuencia(self):
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

    def AplicarMatrizClasificacion(self):
        clas = QFileDialog.getOpenFileName(self, "Seleccione el archivo de calibración: ", "C:/", "PRM (*.prm)")
        self.archivo_calibracion_entrada.setText(clas[0])
        self.matriz_clasificacion = clas[0]

    def AplicarNivel(self): 
        # ver si faltan mas configuraciones para definir un nivel. Tal vez duracion de estimulo, etc
        QtCore.QCoreApplication.processEvents() 
        fout = open("config/nivel.prm", "wt")
        if self.nivel_opciones.currentText() == "Avanzado":
            fout.write("Application:Sequencing int NumberOfSequences= 2 15 1 % // number of sequences in a set of intensifications\n")
            fout.write("Filtering:P3TemporalFilter int EpochsToAverage= 2 1 0 % // Number of epochs to average")
        elif self.nivel_opciones.currentText() == "Intermedio":
            fout.write("Application:Sequencing int NumberOfSequences= 10 15 1 % // number of sequences in a set of intensifications\n")
            fout.write("Filtering:P3TemporalFilter int EpochsToAverage= 10 1 0 % // Number of epochs to average")
        else:
            fout.write("Application:Sequencing int NumberOfSequences= 15 15 1 % // number of sequences in a set of intensifications\n")
            fout.write("Filtering:P3TemporalFilter int EpochsToAverage= 15 1 0 % // Number of epochs to average")
        fout.close()
    
    def AplicarSecuencia(self):
        QtCore.QCoreApplication.processEvents()
        orden_secuencia = list(range(1, 10))

        if self.cantidad_pasos < 9:
            for i in range (self.cantidad_pasos, 9):
                orden_secuencia[i] = 0
        
        # escribimos el archivo de configuracion BCI2000
        img_path = self.ubicacion_img.replace(' ', '%20') # el archivo de configuracion de BCI2000 necesita que los espacios sean indicados con '%20'
        install_path = self.install_dir.replace(' ', '%20')
        fout = open("config/secuencia.prm", "wt")
        fout.write("Application:Speller%20Targets matrix TargetDefinitions= 9 { Display Enter Display%20Size Icon%20File Sound Intensified%20Icon } ")
        lista = ("A A 1 ", "B B 1 ", "C C 1 ", "D D 1 ", "E E 1 ", "F F 1 ", "G G 1 ", "H H 1 ", "I I 1 ") # necesario para construir el archivo prm
        random.shuffle(orden_secuencia)
        for i in range(0, 9):
            if orden_secuencia[i] != 0:
                orden_img = lista[i] + img_path + "/img" + str(orden_secuencia[i]) +".png % % "
                fout.write(orden_img)
            else:
                orden_img = lista[i] + install_path + "/img" + "/img" + str(orden_secuencia[i]) +".png % % "
                fout.write(orden_img)
            self.orden_secuencia[i] = orden_secuencia[i]
        
        fout.write("// speller target properties")
        fout.close()
    
    def AplicarSecuenciaCalibracion(self):
        QtCore.QCoreApplication.processEvents()
        fout = open("config/secuencia.prm", "wt")
        fout.write("Application:Speller%20Targets matrix TargetDefinitions= 9 { Display Enter Display%20Size Icon%20File Sound Intensified%20Icon } ")
        lista = ("A A 1 ", "B B 1 ", "C C 1 ", "D D 1 ", "E E 1 ", "F F 1 ", "G G 1 ", "H H 1 ", "I I 1 ") # necesario para construir el archivo prm
        if self.calibracion_tarea == 1:
            self.ubicacion_img = self.install_dir + "/calibracion/tarea 1"
            orden_sec = [5, 2, 7, 1, 9, 4, 3, 6, 8] # el orden debe ser siempre el mismo debido a el comportamiento de BCI2000 en modo calibración
            text_to_spell = "Application:Speller string TextToSpell= DBGFAHCIE // character or string to spell in offline copy mode"
        elif self.calibracion_tarea == 2:
            self.ubicacion_img = self.install_dir + "/calibracion/tarea 2"
            orden_sec = [8, 1, 4, 7, 6, 3, 9, 2, 5]
            text_to_spell = "Application:Speller string TextToSpell= BHFCIEDAG // character or string to spell in offline copy mode"
        else:
            self.ubicacion_img = self.install_dir + "/calibracion/tarea 3"
            orden_sec = [4, 9, 2, 5, 8, 3, 6, 1, 7]
            text_to_spell = "Application:Speller string TextToSpell= HCFADGIEB // character or string to spell in offline copy mode"
        ubicacion_img = self.ubicacion_img.replace(' ', '%20')
        for i in range(0, 9):
            orden_img = lista[i] + ubicacion_img + "/img" + str(orden_sec[i]) +".png % % "
            fout.write(orden_img)
        fout.write("// speller target properties\n")
        fout.write(text_to_spell)
        fout.close()
        self.orden_secuencia = orden_sec
     
    def IniciarModulosBCI2000(self):
        with open('config/modulos_bci.txt', 'r') as f:
            self.modulos = [line.strip() for line in f]

    def RestablecerConfiguracion(self):
        self.nombre_entrada.setText("")
        self.calibracion_tarea = 1
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
        self.comenzar_terapia_boton.setEnabled(False)
   
    ## OTRAS FUNCIONES

    def IniciarTiempo (self):
        self.tiempo_inicial = datetime.now()

    def ActualizarTiempo(self):
            diferencia = datetime.now() - self.tiempo_inicial
            tiempo_referencia = datetime(self.tiempo_inicial.year, self.tiempo_inicial.month, self.tiempo_inicial.day, 0, 0, 0)
            self.tiempo_sesion = tiempo_referencia + diferencia
            self.tiempo_resumen_texto.setText(str(self.tiempo_sesion.minute).zfill(2) + ' min ' + str(self.tiempo_sesion.second).zfill(2) + ' s')

    def DeshabilitarCambios(self):
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
        self.modo_terapia_opciones.setEnabled(False)
        self.modo_terapia_boton.setEnabled(False)
        self.nivel_opciones.setEnabled(False)
        self.archivo_calibracion_entrada.setEnabled(False)
        self.archivo_calibracion_boton.setEnabled(False)

    def HabilitarCambios(self):
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
        #self.clasificador_boton.setEnabled(True)
        self.modo_terapia_opciones.setEnabled(True)
        self.modo_terapia_boton.setEnabled(True)
        self.nivel_opciones.setEnabled(True)
        self.archivo_calibracion_entrada.setEnabled(True)
        self.archivo_calibracion_boton.setEnabled(True)

    def msgOcultar(self):
        self.BCIAplicacion.feedback_label.hide()
        self.BCIAplicacion.feedback_label.setStyleSheet("color: rgb(242, 242, 242);border-color: rgb(0, 0, 0);border-radius: 6px;"
            "background-color: rgb(35, 181, 156);") # restaura valores por defecto
       
    def OcultarProcesos(self):
        for i in range (0, 3):
            title = re.sub(r"(\w)([A-Z])", r"\1 \2", self.modulos[i])
            hwnd = win32gui.FindWindow(None, title)
            pid = win32process.GetWindowThreadProcessId(hwnd)
            pid = str(pid[1])
            command = "HIDE PROCESS " + pid 
            self.bci.Execute (command)
    
    def InWindow(self):
        parent = self.BCIAplicacion.p3_frame.winId()
        child = win32gui.FindWindow(None, "P3 Speller")
        win32gui.SetParent(child, parent)
        win32gui.SetWindowPos(child, 0, 0, 0, 600, 600, 0)

# SPLASH
class SplashScreen(QtWidgets.QMainWindow, Splash):
    
    def __init__(self):
        super(SplashScreen, self).__init__()
       
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.IniciarCognitask)
        self.timer.start(1250)
        QtCore.QCoreApplication.processEvents() 
        QtCore.QTimer.singleShot(1000, lambda: self.label_2.setText("Configurando módulos..."))
        QtCore.QTimer.singleShot(1200, lambda: self.label_2.setText("Iniciando..."))
        
    
    def IniciarCognitask(self):
        self.timer.stop()
        self.Operador = Cognitask()
        self.Operador.show()
        self.close()

# MAIN
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # agrego las fuentes de texto Gilroy utilizadas
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Light.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Bold.ttf')
    sp = SplashScreen()
    sp.show()
    sys.exit(app.exec_())