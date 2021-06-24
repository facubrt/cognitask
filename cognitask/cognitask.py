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

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from datetime import date
import subprocess
import os

from cognitask.models.BCI2000 import BCI2000
from cognitask.views.aplicacion import BCIAplicacion
from cognitask.views.operador import BCIOperador
from cognitask.models.sesion import Sesion
import cognitask.common.constantes as constantes
import cognitask.common.procesos as procesos
import cognitask.models.informacion as informacion
import cognitask.models.progreso as progreso
import cognitask.models.mensajes as mensajes
import cognitask.models.temporizador as temporizador
import cognitask.models.estados as estados
import cognitask.models.parametros as parametros
import cognitask.common.ubicaciones as ubicaciones

# PARA EJECUTAR COGNITASK ESCRIBIR EN CONSOLA: python -m cognitask

class Cognitask(BCIOperador):

    def __init__(self):
        super(Cognitask, self).__init__()
        
        # INTERFAZ PACIENTE
        self.BCIAplicacion = BCIAplicacion()
        # BCI2000
        self.bci = BCI2000()
        # SESION
        self.sesion = Sesion()

        # PROCESOS
        # introduce P3Speller dentro del modulo de Aplicacion Cognitask
        procesos.incorporarMatriz(self.BCIAplicacion.p3_frame.winId())
        # hace invisible los procesos de BCI2000
        procesos.ocultarProcesos(self.bci)

        QtCore.QCoreApplication.processEvents()

        # comportamiento de botones
        self.configBotones()
        # ubicaciones por defecto
        self.ubicacion_img = ubicaciones.UBICACION_IMG
        self.ubicacion_datos = ubicaciones.UBICACION_DATOS 
        self.ubicacion_clasificador = ubicaciones.UBICACION_CLASIFICADOR

        # variables de sesion
        # estado de la sesión. No iniciada, Preparado, Realizando, Completado
        #self.sesion_estado = "No iniciada"
        self.orden_secuencia = list(range(1, 10))
        self.siguiente_seleccion = 1  # indica la imagen siguiente que debe elegirse
        # imagen seleccionada (necesario debido al orden aleatorio de las imagenes)
        self.imagen_seleccionada = 0
        self.target_seleccionado = 0  # target seleccionado
        # permite cambiar entre las distintas tareas de calibración automaticamente
        self.calibracion_tarea = 1
        # cantidad de pasos que contiene la tarea. Por defecto son 9 pasos
        self.cantidad_pasos = 9
        self.mostrar_guia = True
        self.intentos = 0  # suma 1 cada vez que el sujeto se equivoca en la sesion de terapia
        self.run = 0
        self.actividad_completada = False
        # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma
        self.sesion_iniciada = False

        # temporizador
        self.tiempo_inicial = 0
        self.tiempo_sesion = 0

        # estados
        self.running = 0  # permite alternar entre comenzar y suspender una actividad
        #self.bci_estado = 'Suspended'
        self.consultar_seleccion = True

        # resumen
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        self.porcentaje_aciertos = 0

    # PAGINAS
    # ///////////////////////////////////////////////////////////
    def nuevaSesionPagina(self):
        self.ui_nuevaSesionPagina()
        self.sesion.restablecer()
        # informacion
        informacion.mostrar(self, "Nueva sesion")

    def calibracionPagina(self):
        self.ui_calibracionPagina()
        self.sesion.restablecer()
        # informacion
        informacion.mostrar(self, "Calibracion")

    def terapiaPagina(self):
        self.ui_terapiaPagina()
        self.sesion.restablecer()
        # informacion
        informacion.mostrar(self, "Terapia")

    # NUEVA SESION
    # ///////////////////////////////////////////////////////////
    def iniciarSesion(self):
        # Datos de sujeto y sesión
        if self.nombre_entrada.text() != "":
            # Datos de sujeto y sesión
            hoy = date.today().strftime("%d%m%y")
            self.bci.cargarDatos(self.nombre_entrada.text(), hoy, self.ubicacion_datos)
            # navega a la pagina de calibracion
            self.calibracionPagina()

    def seleccionarDirectorio(self):
        directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una carpeta:', 'C:/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.ubicacion_datos = directorio
            self.ui_seleccionarDirectorio(self.ubicacion_datos)

    # CALIBRACION
    # ///////////////////////////////////////////////////////////
    def prepararCalibracion(self):
        QtCore.QCoreApplication.processEvents()

        # restablecer variables de sesion
        mensajes.restablecer(self)
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0

        progreso.mostrarGuia(self, True)
        parametros.aplicarSecuenciaCalibracion(self)
        self.bci.cargarParametros(ubicaciones.CONFIG_CALIBRACION)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargarParametros(ubicaciones.CONFIG_AMPLIFICADOR)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargarParametros(ubicaciones.CONFIG_SECUENCIA)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultar()
        parametros.aplicarNivel(self, True)

        self.bci.cargarParametros(ubicaciones.CONFIG_NIVEL)

        self.bci.aplicarConfiguracion()
        # hace visible la interfaz de usuario paciente
        self.BCIAplicacion.mostrar()
        self.ui_prepararCalibracion()
        self.sesion.sesion_estado = "Preparado"
        informacion.actualizar(self, True)
        informacion.mostrar(self, "Resumen")
        informacion.escribir(self, "sesion", True)

    def comenzarCalibracion(self):
        if self.running == 0:
            self.bci.iniciar()
            self.ui_comenzarCalibracion(self.calibracion_tarea)
            self.running = 1
            mensajes.mostrar(self, constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)

            self.run += 1
            self.siguiente_seleccion = 1
            self.sesion.sesion_estado = "Realizando"
            progreso.iniciar(self, True)
            informacion.actualizar(self, True)
            temporizador.iniciar(self)
            informacion.escribir(self, "corrida", True)
        else:
            self.bci.suspender()
            self.ui_suspenderCalibracion(self.calibracion_tarea)
            self.running = 0
            self.sesion.sesion_estado = "Interrumpido"
            mensajes.mostrar(self, constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
            # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
            informacion.actualizar(self, True)
            informacion.escribir(self, "resumen", True)

        self.bci.bci_estado = 'Running'
        estados.observar(self, True)

    def finalizarCalibracion(self):
        self.ui_finalizarCalibracion(self.calibracion_tarea)
        
        if self.calibracion_tarea < 3:
            self.calibracion_tarea += 1
        else:
            self.calibracion_tarea = 1
        
        self.running = 0
        mensajes.mostrar(self, constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
        self.actividad_completada = True
        self.sesion.sesion_estado = "Completado"
        informacion.actualizar(self, True)
        informacion.escribir(self, "resumen", True)
        
        self.bci.ejecutar("Wait for Suspended 5")
        self.bci.suspender()

    # TERAPIA
    # ///////////////////////////////////////////////////////////
    def aplicarTerapia(self):
        QtCore.QCoreApplication.processEvents()

        # restablecer variables de sesion
        mensajes.restablecer(self)
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        self.intentos = 0

        if self.guiaVisual != "Deshabilitada":
            progreso.mostrarGuia(self, False)
        else:
            progreso.iniciar(self, False)
            
        parametros.aplicarSecuenciaTerapia(self)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultar()
        self.bci.cargarParametros(ubicaciones.CONFIG_BASE)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargarParametros(ubicaciones.CONFIG_AMPLIFICADOR)
        QtCore.QCoreApplication.processEvents()
        self.bci.cargarParametros(ubicaciones.CONFIG_SECUENCIA)
        parametros.aplicarNivel(self, False)

        self.sesion.sesion_estado = "Preparado"
        informacion.actualizar(self, False)
        informacion.mostrar(self, "Resumen")

        self.bci.cargarParametros(ubicaciones.CONFIG_NIVEL)

        if self.ubicacion_clasificador != ubicaciones.UBICACION_CLASIFICADOR:
            self.bci.cargarParametros(self.ubicacion_clasificador)

        
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.aplicarConfiguracion()
        self.BCIAplicacion.mostrar()
        self.ui_aplicarTerapia()
        informacion.escribir(self, "sesion", False)

    def comenzarTerapia(self):
        if self.bci.bci_estado == 'Suspended':
            self.bci.iniciar()
            self.bci.bci_estado = 'Running'
            self.ui_comenzarTerapia()
            mensajes.mostrar(self, constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)
            self.run += 1
            #self.siguiente_seleccion = 1
            self.sesion.sesion_estado = "Realizando"
            progreso.iniciar(self, False)
            temporizador.iniciar(self)
            informacion.actualizar(self, False)
            informacion.escribir(self, "corrida", False)
        else:
            self.bci.suspender()
            self.bci.bci_estado = 'Suspended'
            self.ui_suspenderTerapia()
            mensajes.mostrar(self, constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
            self.sesion.sesion_estado = "Interrumpido"
            informacion.actualizar(self, False)
            # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
            informacion.escribir(self, "resumen", False)

        estados.observar(self, False)

    def seleccionarSecuencia(self):
        # abrir explorador en carpeta segun el tipo de tarea
        if self.tipo_tarea_opciones.currentText() == "Rompecabezas" or self.tipo_tarea_opciones.currentText() == "Rompecabezas - mem. espacial":
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Rompecabezas/', QFileDialog.ShowDirsOnly)
        elif self.tipo_tarea_opciones.currentText() == "Sucesiones":
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Sucesiones/', QFileDialog.ShowDirsOnly)
        else:
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Palabras/', QFileDialog.ShowDirsOnly)
        
        # asignar la ubicacion de la tarea elegida
        if directorio != "":
            self.ubicacion_img = directorio

        # contamos la cantidad de pasos que contiene la secuencia elegida
        self.cantidad_pasos = sum(1 for item in os.listdir(self.ubicacion_img) if os.path.isfile(os.path.join(self.ubicacion_img, item)))

    def cargarMatrizClasificacion(self):
        ubicacion = QFileDialog.getOpenFileName(self, "Seleccione el archivo de calibración: ", "C:/", "PRM (*.prm)")
        self.ubicacion_clasificador = ubicacion[0]
        self.ui_cargarMatriz(ubicacion)

    def finalizarTerapia(self):
        self.bci.suspender()
        self.ui_finalizarTerapia()
        self.running = 0
        mensajes.mostrar(self, constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
        self.actividad_completada = True
        self.sesion.sesion_estado = "Completado"
        informacion.actualizar(self, False)
        # actualizamos tambien el porcentaje de aciertos
        self.porcentaje_aciertos = round((self.selecciones_correctas / self.selecciones_realizadas) * 100)
        informacion.escribir(self, "resumen", False)

    # OTRAS FUNCIONES
    # ///////////////////////////////////////////////////////////
    def abrirP3Classifier(self):
        subprocess.Popen("BCI2000/P300Classifier/P300Classifier.exe")

    def configBotones(self):
        self.iniciar_sesion_boton.clicked.connect(self.iniciarSesion)
        self.aplicar_terapia_boton.clicked.connect(self.aplicarTerapia)
        self.preparar_calibracion_boton.clicked.connect(self.prepararCalibracion)
        self.comenzar_terapia_boton.clicked.connect(self.comenzarTerapia)
        self.comenzar_calibracion_boton.clicked.connect(self.comenzarCalibracion)
        self.salir_boton.clicked.connect(self.salirCognitask)
        self.directorio_boton.clicked.connect(self.seleccionarDirectorio)
        self.nueva_sesion_boton.clicked.connect(self.nuevaSesionPagina)
        self.calibracion_boton.clicked.connect(self.calibracionPagina)
        self.terapia_boton.clicked.connect(self.terapiaPagina)
        self.tipo_tarea_boton.clicked.connect(self.seleccionarSecuencia)
        self.archivo_calibracion_boton.clicked.connect(self.cargarMatrizClasificacion)
        self.clasificador_boton.clicked.connect(self.abrirP3Classifier)

    # SALIR

    def salirCognitask(self):
        self.bci.terminar()
        del self.bci
        self.BCIAplicacion.close()
        Cognitask.close(self)
