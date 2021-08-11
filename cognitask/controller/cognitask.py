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

from cognitask.models.resumen import Resumen
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from datetime import date
import subprocess
import os

import cognitask.models.progreso as progreso
import cognitask.models.parametros as parametros

from cognitask.models.evaluacion_selecciones import EvaluacionSelecciones
import cognitask.common.ubicaciones as ubicaciones
import cognitask.common.constantes as constantes

####################################################################
# PARA EJECUTAR COGNITASK ESCRIBIR EN CONSOLA: python -m cognitask #
####################################################################

TERAPIA = "Terapia"
CALIBRACION = "Calibracion"

class Cognitask():

    def __init__(self, bci, sesion, operador, aplicacion):
        super(Cognitask, self).__init__()
        
        # INTERFAZ PACIENTE
        self.BCIAplicacion = aplicacion
        # INTERFAZ PROFESIONAL
        self.BCIOperador = operador
        self.config_botones()
        # BCI2000
        self.bci = bci
        # SESION
        self.sesion = sesion

        # variables
        self.paciente = 'Paciente'
        self.tarea = 'Tarea'
        
        self.orden_secuencia = list(range(1, 10))

        # estados
        self.suspender = False  # permite alternar entre comenzar y suspender una actividad
        self.consultar_seleccion = True

    # PAGINAS
    # ///////////////////////////////////////////////////////////
    def nueva_sesion_pagina(self):
        self.BCIOperador.ui_nueva_sesion_pagina()
        self.sesion.restablecer()

    def calibracion_pagina(self):
        self.BCIOperador.ui_calibracion_pagina()
        self.sesion.restablecer()

    def terapia_pagina(self):
        self.BCIOperador.ui_terapia_pagina()
        self.sesion.restablecer()

    # NUEVA SESION
    # ///////////////////////////////////////////////////////////
    def iniciar_sesion(self):
        if self.BCIOperador.paciente != "":
            # Datos de sujeto y sesión
            hoy = date.today().strftime("%d%m%y")
            self.paciente = self.BCIOperador.paciente
            self.bci.cargar_datos(self.BCIOperador.paciente, hoy, self.sesion.ubicacion_datos)
            self.calibracion_pagina()

    def seleccionar_directorio(self):
        directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una carpeta:', 'C:/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.sesion.actualizar_ubicacion_datos(directorio)
            self.BCIOperador.ui_seleccionar_directorio(directorio)

    # CALIBRACION
    # ///////////////////////////////////////////////////////////
    def preparar_calibracion(self):
        QtCore.QCoreApplication.processEvents()
        # restablecer
        self.BCIAplicacion.restablecerMensajes()
        self.sesion.restablecer_selecciones()
        # tarea
        if self.sesion.indice_tarea == 1:
            self.sesion.actualizar_tarea_calibracion(constantes.TAREA_UNO)
        if self.sesion.indice_tarea == 2:
            self.sesion.actualizar_tarea_calibracion(constantes.TAREA_DOS)
        if self.sesion.indice_tarea == 3:
            self.sesion.actualizar_tarea_calibracion(constantes.TAREA_TRES)
        self.tarea = self.sesion.tarea_calibracion
        
        progreso.mostrarGuia(self, True)
        parametros.aplicarSecuenciaCalibracion(self)
        self.bci.cargar_parametros(ubicaciones.CONFIG_CALIBRACION)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_AMPLIFICADOR)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_SECUENCIA)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultarMatriz()
        parametros.aplicarNivel(self.BCIOperador, True)

        self.bci.cargar_parametros(ubicaciones.CONFIG_NIVEL)

        self.bci.aplicar_configuracion()
        # hace visible la interfaz de usuario paciente
        self.BCIAplicacion.mostrarMatriz()
        self.BCIOperador.ui_preparar_calibracion(self.paciente)
        self.BCIOperador.ui_iniciar_resumen(CALIBRACION, self.tarea)
        
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "sesion", True)
        self.sesion.actualizar_estado_sesion('Preparado')

    def comenzar_calibracion(self):
        
        if self.suspender:
            self.bci.suspender()
            self.BCIOperador.ui_suspender_calibracion(self.sesion.indice_tarea)
            self.suspender = False
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
            # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
            self.sesion.actualizar_estado("Interrumpido")
            self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
            Resumen.escribir_resumen(self, self.sesion, self.bci, self.BCIOperador, "resumen", True)
            
        else:
            self.bci.iniciar()
            self.BCIOperador.ui_comenzar_calibracion(self.sesion.indice_tarea)
            self.suspender = True
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)

            self.sesion.actualizar_corrida()
            self.sesion.actualizar_estado("Realizando")
            self.BCIAplicacion.ui_iniciar_progreso(self.BCIOperador.guia_visual, constantes.PASOS_CALIBRACION, True)
            self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
            Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "corrida", True)

        self.bci.bci_estado = 'Running'
        self.observar_estados(True)

    def finalizar_calibracion(self):
        self.suspender = False
        self.sesion.actividad_completada = True
        self.sesion.actualizar_estado("Completado")
        self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
        self.BCIOperador.ui_finalizar_calibracion(self.sesion.indice_tarea)
        self.sesion.actualizar_indice_tarea()
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "resumen", True)
        self.bci.ejecutar("Wait for Suspended 1")
        self.bci.suspender()
        
    # TERAPIA
    # ///////////////////////////////////////////////////////////
    def aplicar_terapia(self):
        QtCore.QCoreApplication.processEvents()

        # restablecer variables de sesion
        self.BCIAplicacion.restablecerMensajes()
        self.sesion.restablecer_selecciones()

        if self.BCIOperador.guia_visual != "Deshabilitada":
            progreso.mostrarGuia(self, False)
        else:
            self.BCIAplicacion.ui_iniciar_progreso(self.BCIOperador.guia_visual, self.sesion.cantidad_pasos, False)
            
        parametros.aplicarSecuenciaTerapia(self)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultarMatriz()
        self.bci.cargar_parametros(ubicaciones.CONFIG_BASE)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_AMPLIFICADOR)
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_SECUENCIA)
        parametros.aplicarNivel(self.BCIOperador, False)

        self.bci.cargar_parametros(ubicaciones.CONFIG_NIVEL)

        if self.sesion.ubicacion_clasificador != ubicaciones.UBICACION_CLASIFICADOR:
            self.bci.cargar_parametros(self.sesion.ubicacion_clasificador)
        
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.aplicar_configuracion()
        self.BCIAplicacion.mostrarMatriz()
        self.BCIOperador.ui_aplicar_terapia(self.paciente)
        self.sesion.actualizar_estado("Preparado")
        self.BCIOperador.ui_iniciar_resumen(TERAPIA, self.tarea)
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "sesion", False)
        self.sesion.actualizar_estado_sesion('Preparado')

    def comenzar_terapia(self):
        if self.bci.bci_estado == 'Suspended':
            self.bci.iniciar()
            self.bci.bci_estado = 'Running'
            self.BCIOperador.ui_comenzar_terapia()
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)
            self.sesion.actualizar_corrida()
            self.sesion.actualizar_estado("Realizando")
            self.BCIAplicacion.ui_iniciar_progreso(self.BCIOperador.guia_visual, self.sesion.cantidad_pasos, False)
            self.BCIOperador.ui_actualizar_selecciones(self.sesion.selecciones_realizadas, self.sesion.selecciones_correctas, self.sesion.selecciones_incorrectas)
            self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
            Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "corrida", False)
        else:
            self.bci.suspender()
            self.bci.bci_estado = 'Suspended'
            self.BCIOperador.ui_suspender_terapia()
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
            self.sesion.actualizar_estado("Interrumpido")
            self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
            # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
            Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "resumen", False)

        self.observar_estados(False)

    def seleccionar_secuencia(self):
        # abrir explorador en carpeta segun el tipo de tarea
        if self.BCIOperador.tipo_tarea.startswith("Rompecabezas"):
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Rompecabezas/', QFileDialog.ShowDirsOnly)
        elif self.BCIOperador.tipo_tarea.startswith("Sucesiones"):
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Sucesiones/', QFileDialog.ShowDirsOnly)
        elif self.BCIOperador.tipo_tarea.startswith("Palabras"):
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Palabras/', QFileDialog.ShowDirsOnly)
        
        # asignar la ubicacion de la tarea elegida
        if directorio != "":
            self.sesion.ubicacion_img = directorio
            self.tarea = os.path.basename(directorio)

        # contamos la cantidad de pasos que contiene la secuencia elegida. En el caso de que se incluyan distractores estos no se cuentan
        self.sesion.cantidad_pasos = sum(1 for item in os.listdir(self.sesion.ubicacion_img) if os.path.isfile(os.path.join(self.sesion.ubicacion_img, item)) and item.startswith('img'))
        # contamos la cantidad de distractores que contiene la secuencia elegida. Puede no tener
        self.sesion.cantidad_distractores = sum(1 for item in os.listdir(self.sesion.ubicacion_img) if os.path.isfile(os.path.join(self.sesion.ubicacion_img, item)) and item.startswith('distractor'))

    def cargar_matriz_clasificacion(self):
        ubicacion = QFileDialog.getOpenFileName(None, "Seleccione el archivo de calibración: ", "C:/", "PRM (*.prm)")
        self.sesion.ubicacion_clasificador = ubicacion[0]
        self.BCIOperador.ui_cargar_matriz(ubicacion)

    def finalizar_terapia(self):
        self.suspender = False
        self.BCIAplicacion.mostrarMensajes(constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
        self.sesion.actividad_completada = True
        self.sesion.actualizar_estado("Completado")
        self.BCIOperador.ui_actualizar_selecciones(self.sesion.selecciones_realizadas, self.sesion.selecciones_correctas, self.sesion.selecciones_incorrectas)
        self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
        self.BCIOperador.ui_finalizar_terapia()
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "resumen", False)
        self.bci.ejecutar("Wait for Suspended 1")
        self.bci.suspender()

    # OBSERVAR ESTADOS BCI2000
    # ///////////////////////////////////////////////////////////
    def observar_estados(self, calibracion):

        self.sesion.iniciar_tiempo()
        
        while self.bci.bci_estado == 'Running':
            QtCore.QCoreApplication.processEvents()
            
            self.sesion.actualizar_tiempo()
            self.BCIOperador.ui_actualizar_tiempo(self.sesion.tiempo_sesion)
            # me da el numero de celda seleccionado (1 a 9)
            celda_seleccionada = int(self.bci.obtener_seleccion)

            if celda_seleccionada != 0 and self.consultar_seleccion == True:
                # con esto puedo conocer que imagen se encuentra en este target (necesario debido al orden aleatorio de las imagenes)
                imagen_seleccionada = self.orden_secuencia[celda_seleccionada - 1]
                self.sesion.actualizar_imagen_seleccionada(imagen_seleccionada)
                
                # PROGRESO - REALIMENTACION
                #############                
                # CALIBRACION
                if calibracion:
                    self.sesion.actualizar_selecciones_realizadas()
                    self.BCIAplicacion.ui_actualizar_progreso(self.BCIOperador.tipo_tarea, self.sesion, calibracion)
                    if self.sesion.siguiente_seleccion < constantes.PASOS_CALIBRACION:
                        msg_calibracion = "Elige la letra " + self.sesion.tarea_calibracion[self.sesion.siguiente_seleccion]
                        self.BCIAplicacion.mostrarMensajes(msg_calibracion, constantes.CSS_MSG_CALIBRACION, True)
                        self.sesion.actualizar_siguiente_seleccion()
                    else:
                        self.BCIAplicacion.mostrarMensajes(constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
                        self.finalizar_calibracion()
                
                # TERAPIA
                else:
                    # ROMPECABEZAS - MEM. ESPACIAL y PALABRAS - REVES tienen algoritmos de evaluacion diferentes
                    if self.BCIOperador.tipo_tarea == 'Rompecabezas - mem. espacial':
                        seleccion_correcta = EvaluacionSelecciones.evaluar_rompecabezas_me(self)
                    elif self.BCIOperador.tipo_tarea == 'Palabras - al revés':
                        seleccion_correcta = EvaluacionSelecciones.evaluar_palabras_reves(self)
                    else:
                        seleccion_correcta = EvaluacionSelecciones.evaluar_seleccion(self)
                    
                    if seleccion_correcta:
                        self.seleccion_correcta(calibracion)
                    else:
                        self.seleccion_incorrecta(calibracion)
                        
                    self.BCIOperador.ui_actualizar_selecciones(self.sesion.selecciones_realizadas, self.sesion.selecciones_correctas, self.sesion.selecciones_incorrectas)
                ###########
                
                self.consultar_seleccion = False

            elif celda_seleccionada == 0 and self.consultar_seleccion == False:
                self.consultar_seleccion = True
            self.bci.bci_estado = self.bci.obtener_estado_sistema

    # SELECCIONES
    # ///////////////////////////////////////////////////////////
    def seleccion_correcta(self, calibracion):
        self.sesion.actualizar_selecciones_correctas()
        self.sesion.restablecer_intentos()
        self.BCIAplicacion.ui_actualizar_progreso(self.BCIOperador.tipo_tarea, self.sesion, calibracion)
        
        if self.sesion.siguiente_seleccion < self.sesion.cantidad_pasos:
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_CORRECTO, constantes.CSS_MSG_CORRECTO, True)
            self.sesion.actualizar_siguiente_seleccion()
            
        else:
            self.finalizar_terapia()
            
    def seleccion_incorrecta(self, calibracion):
        self.sesion.actualizar_selecciones_incorrectas() 
        if self.sesion.intentos < constantes.INTENTOS_MAXIMOS:
            self.sesion.actualizar_intentos()
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_INCORRECTO, constantes.CSS_MSG_INCORRECTO, True)
        else:
            self.sesion.restablecer_intentos()
            if self.sesion.siguiente_seleccion == self.sesion.cantidad_pasos:
                self.finalizar_terapia()
            else:
                self.BCIAplicacion.mostrarMensajes(constantes.MSG_PASAR, constantes.CSS_MSG_PASAR, True)
            self.BCIAplicacion.ui_pasar(self.sesion, self.BCIOperador.tipo_tarea)
            self.sesion.actualizar_siguiente_seleccion()
            
    # OTRAS FUNCIONES
    # ///////////////////////////////////////////////////////////
    def abrir_P3Classifier(self):
        subprocess.Popen("BCI2000/P300Classifier/P300Classifier.exe")

    def config_botones(self):
        self.BCIOperador.iniciar_sesion_boton.clicked.connect(self.iniciar_sesion)
        self.BCIOperador.aplicar_terapia_boton.clicked.connect(self.aplicar_terapia)
        self.BCIOperador.preparar_calibracion_boton.clicked.connect(self.preparar_calibracion)
        self.BCIOperador.comenzar_terapia_boton.clicked.connect(self.comenzar_terapia)
        self.BCIOperador.comenzar_calibracion_boton.clicked.connect(self.comenzar_calibracion)
        self.BCIOperador.salir_boton.clicked.connect(self.salir_cognitask)
        self.BCIOperador.directorio_boton.clicked.connect(self.seleccionar_directorio)
        self.BCIOperador.nueva_sesion_boton.clicked.connect(self.nueva_sesion_pagina)
        self.BCIOperador.calibracion_boton.clicked.connect(self.calibracion_pagina)
        self.BCIOperador.terapia_boton.clicked.connect(self.terapia_pagina)
        self.BCIOperador.tipo_tarea_boton.clicked.connect(self.seleccionar_secuencia)
        self.BCIOperador.archivo_calibracion_boton.clicked.connect(self.cargar_matriz_clasificacion)
        self.BCIOperador.clasificador_boton.clicked.connect(self.abrir_P3Classifier)

    # SALIR
    # ///////////////////////////////////////////////////////////
    def salir_cognitask(self):
        self.bci.terminar()
        del self.bci
        self.BCIAplicacion.close()
        self.BCIOperador.close()
