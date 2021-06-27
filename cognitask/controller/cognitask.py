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

import cognitask.models.progreso as progreso
import cognitask.models.parametros as parametros
import cognitask.models.resumen as resumen

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
        self.configBotones()
        # BCI2000
        self.bci = bci
        # SESION
        self.sesion = sesion
        
        # ubicaciones por defecto
        self.ubicacion_img = ubicaciones.UBICACION_IMG
        self.ubicacion_datos = ubicaciones.UBICACION_DATOS 
        self.ubicacion_clasificador = ubicaciones.UBICACION_CLASIFICADOR

        # variables
        self.paciente = 'Paciente'
        self.tarea = 'Tarea'
        
        # variables de sesion
        # estado de la sesión. No iniciada, Preparado, Realizando, Completado
        #self.sesion_estado = "No iniciada"
        self.orden_secuencia = list(range(1, 10))
        self.siguiente_seleccion = 1  # indica la imagen siguiente que debe elegirse
        # imagen seleccionada (necesario debido al orden aleatorio de las imagenes)
        self.imagen_seleccionada = 0
        # permite cambiar entre las distintas tareas de calibración automaticamente
        self.calibracion_tarea = [1, 'TAREA'] # [numero_tarea, tarea]
        # cantidad de pasos que contiene la tarea. Por defecto son 9 pasos
        self.cantidad_pasos = 9
        self.mostrar_guia = True
        self.intentos = 0  # suma 1 cada vez que el sujeto se equivoca en la sesion de terapia
        self.run = 0
        self.actividad_completada = False
        # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma
        self.sesion_iniciada = False

        # estados
        self.running = 0  # permite alternar entre comenzar y suspender una actividad
        self.consultar_seleccion = True

        # resumen
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        self.porcentaje_aciertos = 0

    # PAGINAS
    # ///////////////////////////////////////////////////////////
    def nuevaSesionPagina(self):
        self.BCIOperador.ui_nuevaSesionPagina()
        self.sesion.restablecer()

    def calibracionPagina(self):
        self.BCIOperador.ui_calibracionPagina()
        self.sesion.restablecer()

    def terapiaPagina(self):
        self.BCIOperador.ui_terapiaPagina()
        self.sesion.restablecer()

    # NUEVA SESION
    # ///////////////////////////////////////////////////////////
    def iniciarSesion(self):
        # Datos de sujeto y sesión
        if self.BCIOperador.paciente != "":
            # Datos de sujeto y sesión
            hoy = date.today().strftime("%d%m%y")
            self.paciente = self.BCIOperador.paciente
            self.bci.cargarDatos(self.BCIOperador.paciente, hoy, self.ubicacion_datos)
            # navega a la pagina de calibracion
            self.calibracionPagina()

    def seleccionarDirectorio(self):
        directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una carpeta:', 'C:/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.ubicacion_datos = directorio
            self.BCIOperador.ui_seleccionarDirectorio(self.ubicacion_datos)

    # CALIBRACION
    # ///////////////////////////////////////////////////////////
    def prepararCalibracion(self):
        QtCore.QCoreApplication.processEvents()

        # restablecer variables de sesion
        self.BCIAplicacion.restablecerMensajes()
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0

        # preparamos la tarea
        if self.calibracion_tarea[0] == 1:
            self.calibracion_tarea[1] = constantes.TAREA_UNO
        if self.calibracion_tarea[0] == 2:
            self.calibracion_tarea[1] = constantes.TAREA_DOS
        if self.calibracion_tarea[0] == 3:
            self.calibracion_tarea[1] = constantes.TAREA_TRES
            
        self.tarea = self.calibracion_tarea[1]
        
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
        self.BCIAplicacion.ocultarMatriz()
        parametros.aplicarNivel(self.BCIOperador, True)

        self.bci.cargarParametros(ubicaciones.CONFIG_NIVEL)

        self.bci.aplicarConfiguracion()
        # hace visible la interfaz de usuario paciente
        self.BCIAplicacion.mostrarMatriz()
        self.sesion.sesion_estado = "Preparado"
        self.BCIOperador.ui_prepararCalibracion(self.paciente)
        self.BCIOperador.ui_iniciarResumen(CALIBRACION, self.tarea)
        
        resumen.escribirResumen(self, "sesion", True)

    def comenzarCalibracion(self):
        if self.running == 0:
            self.bci.iniciar()
            self.BCIOperador.ui_comenzarCalibracion(self.calibracion_tarea[0])
            self.running = 1
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)

            self.run += 1
            self.siguiente_seleccion = 1
            self.sesion.sesion_estado = "Realizando"
            progreso.iniciar(self, True)
            # self.BCIOperador.ui_actualizarSelecciones(self.selecciones_realizadas, self.selecciones_correctas, self.selecciones_incorrectas)
            self.BCIOperador.ui_actualizarEstado(self.sesion.sesion_estado)
            resumen.escribirResumen(self, "corrida", True)
        else:
            self.bci.suspender()
            self.BCIOperador.ui_suspenderCalibracion(self.calibracion_tarea[0])
            self.running = 0
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
            # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
            self.sesion.sesion_estado = "Interrumpido"
            self.BCIOperador.ui_actualizarEstado(self.sesion.sesion_estado)
            resumen.escribirResumen(self, "resumen", True)

        self.bci.bci_estado = 'Running'
        self.observarEstados(True)

    def finalizarCalibracion(self):
        self.BCIOperador.ui_finalizarCalibracion(self.calibracion_tarea[0])
        
        if self.calibracion_tarea[0] < 3:
            self.calibracion_tarea[0] += 1
        else:
            self.calibracion_tarea[0] = 1
        
        self.running = 0
        self.BCIAplicacion.mostrarMensajes(constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
        self.actividad_completada = True
        self.sesion.sesion_estado = "Completado"
        self.BCIOperador.ui_actualizarEstado(self.sesion.sesion_estado)
        resumen.escribirResumen(self, "resumen", True)
        
        self.bci.ejecutar("Wait for Suspended 5")
        self.bci.suspender()

    # TERAPIA
    # ///////////////////////////////////////////////////////////
    def aplicarTerapia(self):
        QtCore.QCoreApplication.processEvents()

        # restablecer variables de sesion
        self.BCIAplicacion.restablecerMensajes()
        self.siguiente_seleccion = 1
        self.selecciones_realizadas = 0
        self.selecciones_correctas = 0
        self.selecciones_incorrectas = 0
        self.intentos = 0

        if self.BCIOperador.guiaVisual != "Deshabilitada":
            progreso.mostrarGuia(self, False)
        else:
            progreso.iniciar(self, False)
            
        parametros.aplicarSecuenciaTerapia(self)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultarMatriz()
        self.bci.cargarParametros(ubicaciones.CONFIG_BASE)
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.cargarParametros(ubicaciones.CONFIG_AMPLIFICADOR)
        QtCore.QCoreApplication.processEvents()
        self.bci.cargarParametros(ubicaciones.CONFIG_SECUENCIA)
        parametros.aplicarNivel(self.BCIOperador, False)

        self.bci.cargarParametros(ubicaciones.CONFIG_NIVEL)

        if self.ubicacion_clasificador != ubicaciones.UBICACION_CLASIFICADOR:
            self.bci.cargarParametros(self.ubicacion_clasificador)

        
        # evita que la gui se cuelgue cuando se cargan los parametros
        QtCore.QCoreApplication.processEvents()
        self.bci.aplicarConfiguracion()
        self.BCIAplicacion.mostrarMatriz()
        self.BCIOperador.ui_aplicarTerapia(self.paciente)
        self.sesion.sesion_estado = "Preparado"
        self.BCIOperador.ui_iniciarResumen(TERAPIA, self.tarea)
        resumen.escribirResumen(self, "sesion", False)

    def comenzarTerapia(self):
        if self.bci.bci_estado == 'Suspended':
            self.bci.iniciar()
            self.bci.bci_estado = 'Running'
            self.BCIOperador.ui_comenzarTerapia()
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)
            self.run += 1
            self.sesion.sesion_estado = "Realizando"
            progreso.iniciar(self, False)
            self.BCIOperador.ui_actualizarSelecciones(self.selecciones_realizadas, self.selecciones_correctas, self.selecciones_incorrectas)
            self.BCIOperador.ui_actualizarEstado(self.sesion.sesion_estado)
            resumen.escribirResumen(self, "corrida", False)
        else:
            self.bci.suspender()
            self.bci.bci_estado = 'Suspended'
            self.BCIOperador.ui_suspenderTerapia()
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
            self.sesion.sesion_estado = "Interrumpido"
            # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
            self.BCIOperador.ui_actualizarEstado(self.sesion.sesion_estado)
            resumen.escribirResumen(self, "resumen", False)

        self.observarEstados(False)

    def seleccionarSecuencia(self):
        # abrir explorador en carpeta segun el tipo de tarea
        if self.BCIOperador.tipoTarea.startswith("Rompecabezas"):
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Rompecabezas/', QFileDialog.ShowDirsOnly)
        elif self.BCIOperador.tipoTarea.startswith("Sucesiones"):
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Sucesiones/', QFileDialog.ShowDirsOnly)
        elif self.BCIOperador.tipoTarea.startswith("Palabras"):
            directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una secuencia:', 'terapia/Palabras/', QFileDialog.ShowDirsOnly)
        
        # asignar la ubicacion de la tarea elegida
        if directorio != "":
            self.ubicacion_img = directorio
            self.tarea = os.path.basename(directorio)

        # contamos la cantidad de pasos que contiene la secuencia elegida
        self.cantidad_pasos = sum(1 for item in os.listdir(self.ubicacion_img) if os.path.isfile(os.path.join(self.ubicacion_img, item)))

    def cargarMatrizClasificacion(self):
        ubicacion = QFileDialog.getOpenFileName(None, "Seleccione el archivo de calibración: ", "C:/", "PRM (*.prm)")
        self.ubicacion_clasificador = ubicacion[0]
        self.BCIOperador.ui_cargarMatriz(ubicacion)

    def finalizarTerapia(self):
        self.bci.suspender()
        self.BCIOperador.ui_finalizarTerapia()
        self.running = 0
        self.BCIAplicacion.mostrarMensajes(constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
        self.actividad_completada = True
        self.sesion.sesion_estado = "Completado"
        self.BCIOperador.ui_actualizarSelecciones(self.selecciones_realizadas, self.selecciones_correctas, self.selecciones_incorrectas)
        self.BCIOperador.ui_actualizarEstado(self.sesion.sesion_estado)
        # actualizamos tambien el porcentaje de aciertos
        self.porcentaje_aciertos = round((self.selecciones_correctas / self.selecciones_realizadas) * 100)
        resumen.escribirResumen(self, "resumen", False)

    # OBSERVAR ESTADOS BCI2000
    # ///////////////////////////////////////////////////////////
    def observarEstados(self, calibracion):

        self.sesion.iniciarTiempo()
        
        while self.bci.bci_estado == 'Running':
            QtCore.QCoreApplication.processEvents()
            
            self.sesion.actualizarTiempo()
            self.BCIOperador.ui_actualizarTiempo(self.sesion.tiempo_sesion)
            # me da el numero de celda seleccionado (1 a 9)
            celda_seleccionada = int(self.bci.obtenerSeleccion)

            if celda_seleccionada != 0 and self.consultar_seleccion == True:
                # con esto puedo conocer que imagen se encuentra en este target (necesario debido al orden aleatorio de las imagenes)
                self.imagen_seleccionada = self.orden_secuencia[celda_seleccionada - 1]
                
                # PROGRESO - REALIMENTACION
                #############                
                # CALIBRACION
                if calibracion:
                    msg_calibracion = "Elige la letra " + self.calibracion_tarea[1][self.siguiente_seleccion]
                    self.BCIAplicacion.mostrarMensajes(msg_calibracion, constantes.CSS_MSG_CALIBRACION, True)
                    self.selecciones_realizadas += 1
                    progreso.actualizar(self, calibracion)
                    if self.siguiente_seleccion < constantes.PASOS_CALIBRACION:
                        self.siguiente_seleccion += 1
                    else:
                        self.finalizarCalibracion()
                # TERAPIA
                else:
                    if self.BCIOperador.tipoTarea == 'Rompecabezas - mem. espacial':
                        seleccion_correcta = EvaluacionSelecciones.evaluar_memoria_espacial(self)
                    elif self.BCIOperador.tipoTarea == 'Palabras - al revés':
                        seleccion_correcta = EvaluacionSelecciones.evaluar_atencion_inversa(self)
                    else:
                        seleccion_correcta = EvaluacionSelecciones.evaluar_atencion(self)
                    
                    if seleccion_correcta:
                        self.seleccionCorrecta(calibracion)
                    else:
                        self.seleccionIncorrecta(calibracion)
                        
                    self.BCIOperador.ui_actualizarSelecciones(self.selecciones_realizadas, self.selecciones_correctas, self.selecciones_incorrectas)
                ###########
                self.consultar_seleccion = False

            elif celda_seleccionada == 0 and self.consultar_seleccion == False:
                self.consultar_seleccion = True
            self.bci.bci_estado = self.bci.obtenerEstadoSistema

    # SELECCIONES
    # ///////////////////////////////////////////////////////////
    def seleccionCorrecta(self, calibracion):
        
        if self.siguiente_seleccion < self.cantidad_pasos:
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_CORRECTO, constantes.CSS_MSG_CORRECTO, True)
            self.intentos = 0
            progreso.actualizar(self, calibracion)
            self.selecciones_correctas += 1
            self.selecciones_realizadas += 1
            self.siguiente_seleccion = self.siguiente_seleccion + 1
            
        else:
            progreso.actualizar(self, calibracion)
            self.intentos = 0
            self.selecciones_correctas += 1
            self.selecciones_realizadas += 1
            self.finalizarTerapia()
            
    def seleccionIncorrecta(self, calibracion):
    
        if self.intentos < constantes.INTENTOS_MAXIMOS:
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_INCORRECTO, constantes.CSS_MSG_INCORRECTO, True)
            self.intentos += 1
            self.selecciones_incorrectas += 1
            self.selecciones_realizadas += 1

        elif self.intentos == constantes.INTENTOS_MAXIMOS and self.siguiente_seleccion == self.cantidad_pasos:
            progreso.siguientePaso(self, calibracion)
            self.intentos = 0 # restablecemos los valores de intentos
            self.selecciones_incorrectas += 1
            self.selecciones_realizadas += 1
            self.finalizarTerapia()
            
        elif self.intentos == constantes.INTENTOS_MAXIMOS and self.siguiente_seleccion != self.cantidad_pasos:
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_PASAR, constantes.CSS_MSG_PASAR, True)
            progreso.siguientePaso(self, calibracion)
            self.intentos = 0
            self.selecciones_incorrectas += 1
            self.selecciones_realizadas += 1
            self.siguiente_seleccion = self.siguiente_seleccion + 1  
      
    # OTRAS FUNCIONES
    # ///////////////////////////////////////////////////////////
    def abrirP3Classifier(self):
        subprocess.Popen("BCI2000/P300Classifier/P300Classifier.exe")

    def configBotones(self):
        self.BCIOperador.iniciar_sesion_boton.clicked.connect(self.iniciarSesion)
        self.BCIOperador.aplicar_terapia_boton.clicked.connect(self.aplicarTerapia)
        self.BCIOperador.preparar_calibracion_boton.clicked.connect(self.prepararCalibracion)
        self.BCIOperador.comenzar_terapia_boton.clicked.connect(self.comenzarTerapia)
        self.BCIOperador.comenzar_calibracion_boton.clicked.connect(self.comenzarCalibracion)
        self.BCIOperador.salir_boton.clicked.connect(self.salirCognitask)
        self.BCIOperador.directorio_boton.clicked.connect(self.seleccionarDirectorio)
        self.BCIOperador.nueva_sesion_boton.clicked.connect(self.nuevaSesionPagina)
        self.BCIOperador.calibracion_boton.clicked.connect(self.calibracionPagina)
        self.BCIOperador.terapia_boton.clicked.connect(self.terapiaPagina)
        self.BCIOperador.tipo_tarea_boton.clicked.connect(self.seleccionarSecuencia)
        self.BCIOperador.archivo_calibracion_boton.clicked.connect(self.cargarMatrizClasificacion)
        self.BCIOperador.clasificador_boton.clicked.connect(self.abrirP3Classifier)

    # SALIR

    def salirCognitask(self):
        self.bci.terminar()
        del self.bci
        self.BCIAplicacion.close()
        self.BCIOperador.close()
