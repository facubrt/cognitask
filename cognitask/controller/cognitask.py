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
import subprocess
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from datetime import date
from cognitask.models.parametros import Parametros
from cognitask.models.evaluacion import Evaluacion
from cognitask.models.resumen import Resumen
import cognitask.common.ubicaciones as ubicaciones
import cognitask.common.constantes as constantes

TERAPIA = "Terapia"
CALIBRACION = "Calibracion"

####################################################################
# PARA EJECUTAR COGNITASK ESCRIBIR EN CONSOLA: python -m cognitask #
####################################################################
class Cognitask():

    def __init__(self, bci, sesion, operador, aplicacion):
        '''------------
        DOCUMENTACIÓN -
        Inicializa Cognitask.
        - Instancia los objetos Aplicacion, Operador, BCI y Sesion que recibe.
        - Configura el comportamiento de los botones de la vista Operador.
        - Establece valores por defecto.
        
        Parametros que recibe
        - Instancia de BCI.
        - Instancia de Sesion.
        - Instancia de Operador.
        - Instancia de Aplicacion.
        ------------'''
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
        
        #self.orden_secuencia = list(range(1, 10))

        # estados
        self.consultar_seleccion = True

    # PAGINAS
    # ///////////////////////////////////////////////////////////
    def nueva_sesion_pagina(self):
        '''------------
        DOCUMENTACIÓN -
        Abre la pagina Nueva Sesion.
        - Restablece los valores y variables de la sesion.
        ------------'''
        self.BCIOperador.ui_nueva_sesion_pagina()
        self.sesion.restablecer()

    def calibracion_pagina(self):
        '''------------
        DOCUMENTACIÓN -
        Abre la pagina Calibracion.
        - Restablece los valores y variables de la sesion.
        ------------'''
        self.BCIOperador.ui_calibracion_pagina()
        self.sesion.restablecer()

    def terapia_pagina(self):
        '''------------
        DOCUMENTACIÓN -
        Abre la pagina Terapia.
        - Restablece los valores y variables de la sesion.
        ------------'''
        self.BCIOperador.ui_terapia_pagina()
        self.sesion.restablecer()

    # NUEVA SESION
    # ///////////////////////////////////////////////////////////
    def iniciar_sesion(self):
        '''------------
        DOCUMENTACIÓN -
        Inicia una nueva sesion. 
        - Carga los datos del paciente en BCI.
        - Pasa a la pagina Calibracion.
        ------------'''
        if self.BCIOperador.paciente != "":
            # Datos de sujeto y sesión
            hoy = date.today().strftime("%d%m%y")
            self.paciente = self.BCIOperador.paciente
            self.bci.cargar_datos(self.BCIOperador.paciente, hoy, self.sesion.ubicacion_datos)
            self.calibracion_pagina()

    def seleccionar_directorio(self):
        '''------------
        DOCUMENTACIÓN -
        Selecciona el directorio donde se guardaran los datos de la sesion.
        - Abre el explorador de Windows para seleccionar el directorio.
        - Actualiza la ubicacion de los datos en Sesion.
        - Actualiza la ubicacion de los datos en Operador.
        ------------'''
        directorio = QFileDialog.getExistingDirectory(None, 'Selecciona una carpeta:', 'C:/', QFileDialog.ShowDirsOnly)
        if directorio != "":
            self.sesion.actualizar_ubicacion_datos(directorio)
            self.BCIOperador.ui_seleccionar_directorio(directorio)

    # CALIBRACION
    # ///////////////////////////////////////////////////////////
    def preparar_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Prepara la tarea preestablecida de calibracion.
        - Restablece valores de la sesion.
        - Carga en Sesion la nueva tarea de calibracion.
        - Muestra la guia visual en Aplicacion.
        - Carga los parametros de calibracion y la tarea seleccionada en BCI.
        - Presenta la matriz de estimulacion en Aplicacion
        - Actualiza la informacion de la tarea en Operador
        - Escribe la seccion 'sesion' en el archivo externo resumen_sesiones
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
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
        
        self.BCIAplicacion.ui_mostrar_guia_calibracion(self.sesion)
        Parametros.aplicar_tarea_calibracion(self.sesion)
        self.bci.cargar_parametros(ubicaciones.CONFIG_CALIBRACION)
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_AMPLIFICADOR)
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_SECUENCIA)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultarMatriz()
        Parametros.aplicar_nivel_calibracion()

        self.bci.cargar_parametros(ubicaciones.CONFIG_NIVEL)

        self.bci.aplicar_configuracion()
        # hace visible la interfaz de usuario paciente
        self.BCIAplicacion.mostrarMatriz()
        self.BCIOperador.ui_preparar_calibracion(self.paciente)
        self.BCIOperador.ui_iniciar_resumen(CALIBRACION, self.tarea)
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "sesion", True)
        self.sesion.actualizar_estado('Preparado')

    def comenzar_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Comienza la tarea de calibracion.
        - Inicia la estimuacion visual de BCI2000
        - Actualiza informacion de la tarea en Operador.
        - Actualiza informacion de la tarea en Sesion.
        - Inicia el progreso de la tarea
        - Escribe la seccion 'corrida' en el archivo externo resumen_sesiones
        - Si la tarea ya se esta ejecutando, permite suspender la misma
        - Observa los estados de BCI2000 para determinar las selecciones realizadas
        ------------'''
        if self.bci.estado == 'Suspended':
            self.bci.iniciar()
            self.bci.estado = 'Running'
            self.BCIOperador.ui_comenzar_calibracion(self.sesion.indice_tarea)
            self.suspender = True
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)

            self.sesion.actualizar_corrida()
            self.sesion.actualizar_estado("Realizando")
            self.BCIAplicacion.ui_iniciar_progreso(self.BCIOperador.guia_visual, constantes.PASOS_CALIBRACION, True)
            self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
            Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "corrida", True)  
        else:
            self.suspender_calibracion()
            
        self.bci.estado = 'Running'
        self.observar_estados(True)

    def suspender_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Suspende la tarea de calibracion.
        - Suspende la estimuacion visual de BCI2000
        - Actualiza informacion de la tarea en Operador.
        - Actualiza informacion de la tarea en Sesion.
        - Escribe la seccion 'resumen' en el archivo externo resumen_sesiones
        ------------'''
        self.bci.suspender()
        self.BCIOperador.ui_suspender_calibracion(self.sesion.indice_tarea)
        self.bci.estado = 'Suspended'
        self.BCIAplicacion.mostrarMensajes(constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
        # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
        self.sesion.actualizar_estado("Interrumpido")
        self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "resumen", True)
        
    def finalizar_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Finaliza la tarea de calibracion.
        - Actualiza informacion de la tarea en Operador.
        - Actualiza informacion de la tarea en Sesion.
        - Escribe la seccion 'resumen' en el archivo externo resumen_sesiones
        - Suspende la estimuacion visual de BCI2000
        ------------'''
        self.bci.estado = 'Suspended'
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
        '''------------
        DOCUMENTACIÓN -
        Prepara la tarea de terapia.
        - Restablece valores de la sesion.
        - Muestra la guia visual en Aplicacion si esta habilitada.
        - Carga en Sesion la nueva tarea de calibracion.
        - Carga los parametros de configuracion y la tarea seleccionada en BCI.
        - Presenta la matriz de estimulacion en Aplicacion
        - Actualiza la informacion de la tarea en Operador
        - Escribe la seccion 'sesion' en el archivo externo resumen_sesiones
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        # restablecer variables de sesion
        self.BCIAplicacion.restablecerMensajes()
        self.sesion.restablecer_selecciones()

        if self.BCIOperador.guia_visual != "Deshabilitada":
            self.BCIAplicacion.ui_mostrar_guia_terapia(self.sesion)
        else:
            self.BCIAplicacion.ui_iniciar_progreso(self.BCIOperador.guia_visual, self.sesion.cantidad_pasos, False)
            
        Parametros.aplicar_tarea_terapia(self.sesion, self.BCIOperador.tipo_tarea)
        # se oculta la matriz antes de configurar para evitar los glitches visuales de BCI2000
        self.BCIAplicacion.ocultarMatriz()
        self.bci.cargar_parametros(ubicaciones.CONFIG_BASE)
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_AMPLIFICADOR)
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        self.bci.cargar_parametros(ubicaciones.CONFIG_SECUENCIA)
        Parametros.aplicar_nivel_terapia(self.BCIOperador.nivel)

        self.bci.cargar_parametros(ubicaciones.CONFIG_NIVEL)

        if self.sesion.ubicacion_clasificador != ubicaciones.UBICACION_CLASIFICADOR:
            self.bci.cargar_parametros(self.sesion.ubicacion_clasificador)
        
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        self.bci.aplicar_configuracion()
        self.BCIAplicacion.mostrarMatriz()
        self.BCIOperador.ui_aplicar_terapia(self.paciente)
        self.BCIOperador.ui_iniciar_resumen(TERAPIA, self.tarea)
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "sesion", False)
        self.sesion.actualizar_estado('Preparado')

    def comenzar_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Comienza la tarea de terapia.
        - Inicia la estimuacion visual de BCI2000
        - Actualiza informacion de la tarea en Operador.
        - Actualiza informacion de la tarea en Sesion.
        - Inicia el progreso de la tarea
        - Escribe la seccion 'corrida' en el archivo externo resumen_sesiones
        - Si la tarea ya se esta ejecutando, permite suspender la misma
        - Observa los estados de BCI2000 para determinar las selecciones realizadas
        ------------'''
        if self.bci.estado == 'Suspended':
            self.bci.iniciar()
            self.bci.estado = 'Running'
            self.BCIOperador.ui_comenzar_terapia()
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_COMENZAR, constantes.CSS_MSG_COMENZAR, True)
            self.sesion.actualizar_corrida()
            self.sesion.actualizar_estado("Realizando")
            self.BCIAplicacion.ui_iniciar_progreso(self.BCIOperador.guia_visual, self.sesion.cantidad_pasos, False)
            self.BCIOperador.ui_actualizar_selecciones(self.sesion.selecciones_realizadas, self.sesion.selecciones_correctas, self.sesion.selecciones_incorrectas)
            self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
            Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "corrida", False)
        else:
            self.suspender_terapia()

        self.observar_estados(False)

    def seleccionar_secuencia(self):
        '''------------
        DOCUMENTACIÓN -
        Selecciona el directorio donde se encuentran las imagenes que se utilizaran segun el tipo de tarea.
        - Abre el explorador de Windows para buscar y seleccionar el directorio
        - Actualiza la informacion sobre la tarea seleccionada en Sesion
        - Determina cuantos pasos requiere la tarea seleccionada
        - Determina la presencia de distractores en la tarea
        ------------'''
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
        '''------------
        DOCUMENTACIÓN -
        Carga la matriz de clasificacion obtenida en P300Classifier.
        - Abre el explorador de Windows para buscar y seleccionar el archivo .prm
        - Actualiza la informacion sobre la matriz utilizada en Sesion
        - Actualiza la informacion sobre la matriz utilizada en Operador
        ------------'''
        ubicacion = QFileDialog.getOpenFileName(None, "Seleccione el archivo de calibración: ", "C:/", "PRM (*.prm)")
        self.sesion.ubicacion_clasificador = ubicacion[0]
        self.BCIOperador.ui_cargar_matriz(ubicacion)

    def suspender_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Suspende la tarea de terapia.
        - Suspende la estimuacion visual de BCI2000
        - Actualiza informacion de la tarea en Operador.
        - Actualiza informacion de la tarea en Sesion.
        - Escribe la seccion 'resumen' en el archivo externo resumen_sesiones
        ------------'''
        self.bci.suspender()
        self.bci.estado = 'Suspended'
        self.BCIOperador.ui_suspender_terapia()
        self.BCIAplicacion.mostrarMensajes(constantes.MSG_SUSPENDIDO, constantes.CSS_MSG_SUSPENDIDO, False)
        self.sesion.actualizar_estado("Interrumpido")
        self.BCIOperador.ui_actualizar_estado(self.sesion.estado)
        # si se interrumpe la corrida y se empieza una nueva, se anuncia que no se completo y se da un resumen
        Resumen.escribir_resumen(self.sesion, self.bci, self.BCIOperador, "resumen", False)

    def finalizar_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Finaliza la tarea de terapia.
        - Actualiza informacion de la tarea en Operador.
        - Actualiza informacion de la tarea en Sesion.
        - Escribe la seccion 'resumen' en el archivo externo resumen_sesiones
        - Suspende la estimuacion visual de BCI2000
        ------------'''
        self.bci.estado = 'Suspended'
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
        '''------------
        DOCUMENTACIÓN -
        Observa los estados de BCI2000.
        - Inicia tiempo de la sesion
        - Determina la imagen seleccionada
        - CALIBRACION. Actualiza el progreso de la tarea y avanza a la siguiente
        - TERAPIA. Evalua la seleccion realizada para determinar si es correcta o incorrecta (depende del tipo de tarea).
        - Actualiza las selecciones realizadas
        ------------'''
        self.sesion.iniciar_tiempo()
        
        while self.bci.estado == 'Running':
            # Refrezca la interfaz grafica evitando que se congele
            QtCore.QCoreApplication.processEvents()
            self.sesion.actualizar_tiempo()
            self.BCIOperador.ui_actualizar_tiempo(self.sesion.tiempo_sesion)
            # me da el numero de celda seleccionado (1 a 9)
            celda_seleccionada = int(self.bci.obtener_seleccion)
            
            if celda_seleccionada != 0 and self.consultar_seleccion == True:
                # con esto puedo conocer que imagen se encuentra en este target (necesario debido al orden aleatorio)
                imagen_seleccionada = self.sesion.orden_secuencia[celda_seleccionada - 1]
                self.sesion.actualizar_imagen_seleccionada(imagen_seleccionada)
                                
                # CALIBRACION
                if calibracion:
                    self.actualizar_selecciones_calibracion()
                # TERAPIA
                else:
                    self.actualizar_selecciones_terapia()
                
                self.consultar_seleccion = False

            elif celda_seleccionada == 0 and self.consultar_seleccion == False:
                self.consultar_seleccion = True
            self.bci.estado = self.bci.obtener_estado_sistema

    # SELECCIONES
    # ///////////////////////////////////////////////////////////
    def actualizar_selecciones_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza las selecciones realizadas durante la tarea de calibracion.
        - Actualiza las selecciones realizadas sin evaluar las mismas
        ------------'''
        self.sesion.actualizar_selecciones_realizadas()
        self.BCIAplicacion.ui_actualizar_progreso(self.BCIOperador.tipo_tarea, self.sesion, True)
        if self.sesion.siguiente_seleccion < constantes.PASOS_CALIBRACION:
            msg_calibracion = "Elige la letra " + self.sesion.tarea_calibracion[self.sesion.siguiente_seleccion]
            self.BCIAplicacion.mostrarMensajes(msg_calibracion, constantes.CSS_MSG_CALIBRACION, True)
            self.sesion.actualizar_siguiente_seleccion()
        else:
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_TERMINADO, constantes.CSS_MSG_TERMINADO, False)
            self.finalizar_calibracion()
                
    def actualizar_selecciones_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza las selecciones realizadas durante la tarea de terapia y evalua si son correctas o incorrectas.
        - Evalua la seleccion segun el tipo de tarea
        - Actualiza las selecciones realizadas en Operador
        ------------'''
        # ROMPECABEZAS - MEM. ESPACIAL y PALABRAS - REVES tienen algoritmos de evaluacion diferentes
        seleccion_correcta = Evaluacion.evaluar_seleccion(self.BCIOperador.tipo_tarea, self.sesion)
        
        if seleccion_correcta:
            self.seleccion_correcta()
        else:
            self.seleccion_incorrecta()
            
        self.BCIOperador.ui_actualizar_selecciones(self.sesion.selecciones_realizadas, self.sesion.selecciones_correctas, self.sesion.selecciones_incorrectas)
    
    def seleccion_correcta(self):
        '''------------
        DOCUMENTACIÓN -
        Determina el comportamiento del sistema cuando se realiza una seleccion correcta.
        - Actualiza las selecciones correctas en Sesion
        - Restablece los intentos permitidos
        - Actualiza el progreso de la tarea
        - Muestra una realimentacion al usuario paciente en Aplicacion
        - Determina el comportamiento del sistema (siguiente seleccion, terminar tarea)
        ------------'''
        self.sesion.actualizar_selecciones_correctas()
        self.sesion.restablecer_intentos()
        self.BCIAplicacion.ui_actualizar_progreso(self.BCIOperador.tipo_tarea, self.sesion, False)
        
        if self.sesion.siguiente_seleccion < self.sesion.cantidad_pasos:
            self.BCIAplicacion.mostrarMensajes(constantes.MSG_CORRECTO, constantes.CSS_MSG_CORRECTO, True)
            self.sesion.actualizar_siguiente_seleccion()
            
        else:
            self.finalizar_terapia()
            
    def seleccion_incorrecta(self):
        '''------------
        DOCUMENTACIÓN -
        Determina el comportamiento del sistema cuando se realiza una seleccion incorrecta.
        - Actualiza las selecciones incorrectas en Sesion
        - Actualiza los intentos en Sesion
        - Muestra una realimentacion al usuario paciente en Aplicacion
        - Determina el comportamiento del sistema (repetir seleccion, pasar a la siguiente, terminar tarea)
        ------------'''
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
    def abrir_P300Classifier(self):
        '''------------
        DOCUMENTACIÓN -
        Inicia la herramienta P300Classifier de BCI2000.
        - Inicia la herramienta P300Classifier en un subproceso.
        ------------'''
        subprocess.Popen("BCI2000/P300Classifier/P300Classifier.exe")

    def config_botones(self):
        '''------------
        DOCUMENTACIÓN -
        Configura el comportamiento de los botones en Operador.
        - Asigna los diferentes botones a una funcion determinada.
        ------------'''
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
        self.BCIOperador.clasificador_boton.clicked.connect(self.abrir_P300Classifier)

    # SALIR
    # ///////////////////////////////////////////////////////////
    def salir_cognitask(self):
        '''------------
        DOCUMENTACIÓN -
        Termina Cognitask.
        - Cierra los procesos de BCI2000.
        - Cierra los procesos de Aplicacion.
        - Cierra los procesos de Operador.
        ------------'''
        self.bci.terminar()
        del self.bci
        self.BCIAplicacion.close()
        self.BCIOperador.close()
