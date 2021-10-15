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
        '''------------
        DOCUMENTACIÓN -
        Inicializa el Operador (Interfaz de usuario Profesional) de Cognitask.
        ------------'''
        super(BCIOperador, self).__init__()
        self.configuracion_inicial()

    # FUNCIONES DE INTERFAZ GENERAL
    # ///////////////////////////////////////////////////////////
    def configuracion_inicial(self):
        '''------------
        DOCUMENTACIÓN -
        Establece valores y estados por defecto en el Operador.
        - Pagina inicial, estado de botones, etc
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.configuracion_stacked_widget.setCurrentIndex(0)
        self.informacion_stacked_widget.setCurrentIndex(0)
        self.nueva_sesion_boton.setEnabled(False)
        self.calibracion_boton.setEnabled(False)
        self.terapia_boton.setEnabled(False)
        self.comenzar_calibracion_boton.setEnabled(False)
        self.comenzar_terapia_boton.setEnabled(False)
        self.clasificador_boton.setEnabled(False)
        self.directorio_entrada.setPlaceholderText(ubicaciones.UBICACION_DATOS)
            
    def _deshabilitar_cambios(self):
        '''------------
        DOCUMENTACIÓN -
        Deshabilita la posibilidad de realizar cambios en los parámetros cuando la tarea ha comenzado.
        - Bloquea o modifica el comportamiento de botones, paginas, etc
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.comenzar_calibracion_boton.setText("Suspender")
        self.comenzar_calibracion_boton.setStyleSheet(constantes.SUSPENDER_BOTON_CSS)
        self.comenzar_terapia_boton.setText("Suspender")
        self.comenzar_terapia_boton.setStyleSheet(constantes.SUSPENDER_BOTON_CSS)
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

    def _habilitar_cambios(self):
        '''------------
        DOCUMENTACIÓN -
        Habilita la posibilidad de realizar cambios en los parámetros cuando la tarea ha finalizado.
        - Desbloquea o modifica el comportamiento de botones, paginas, etc
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.comenzar_calibracion_boton.setText("Comenzar")
        self.comenzar_calibracion_boton.setStyleSheet(constantes.COMENZAR_BOTON_CSS)
        self.comenzar_terapia_boton.setText("Comenzar")
        self.comenzar_terapia_boton.setStyleSheet(constantes.COMENZAR_BOTON_CSS)
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
    
    def _aplicando_configuracion(self):
        '''------------
        DOCUMENTACIÓN -
        Inhabilita las modificaciones cuando se prepara o se aplica la configuración de una sesión
        - Bloquea el comportamiento de botones, paginas, etc
        ------------'''
        self.preparar_calibracion_boton.setEnabled(False)
        self.preparar_calibracion_boton.setText("Preparando...")
        self.aplicar_terapia_boton.setEnabled(False)
        self.aplicar_terapia_boton.setText("Aplicando...")
    
    def _configuracion_lista(self):  
        '''------------
        DOCUMENTACIÓN -
        Habilita las modificaciones cuando se prepara o se aplica la configuración de una sesión
        - Desbloquea el comportamiento de botones, paginas, etc
        ------------'''
        self.preparar_calibracion_boton.setEnabled(True)
        self.preparar_calibracion_boton.setText("Preparar")
        self.aplicar_terapia_boton.setEnabled(True)
        self.aplicar_terapia_boton.setText("Aplicar")
          
    # PAGINAS 
    # ///////////////////////////////////////////////////////////
    def ui_nueva_sesion_pagina (self):
        '''------------
        DOCUMENTACIÓN -
        Configura la pagina de Nueva sesion.
        - Muestra la informacion correspondiente a la pagina Nueva sesion y deshabilita las otras paginas
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
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
        self._como_empezar(INDICE_NUEVA_SESION)
    
    def ui_calibracion_pagina(self):
        '''------------
        DOCUMENTACIÓN -
        Configura la pagina de Calibracion.
        - Muestra la informacion correspondiente a la pagina Calibracion
        ------------'''
        QtCore.QCoreApplication.processEvents()
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
        
        self._como_empezar(INDICE_CALIBRACION)
        
    def ui_terapia_pagina(self):
        '''------------
        DOCUMENTACIÓN -
        Configura la pagina de Calibracion.
        - Muestra la informacion correspondiente a la pagina Terapia
        ------------'''
        QtCore.QCoreApplication.processEvents()
        # interfaz
        self.seleccion_calibracion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_nueva_sesion_frame.setStyleSheet("background-color: rgb(38, 43, 50);")
        self.seleccion_terapia_frame.setStyleSheet("background-color:rgb(255,255,255);")
        
        self.nueva_sesion_boton.setEnabled(True)
        self.calibracion_boton.setEnabled(True)
        self.terapia_boton.setEnabled(True)
        
        self.configuracion_stacked_widget.setCurrentIndex(2)
        self.comenzar_terapia_boton.setEnabled(False)
        
        self._como_empezar(INDICE_TERAPIA)     
    
    def _como_empezar(self, pagina):
        '''------------
        DOCUMENTACIÓN -
        Guia rapida ¿Como empezar?.
        - Muestra la informacion necesaria para configurar y comenzar una sesion
        ------------'''
        self.informacion_titulo.setText("¿Cómo empezar?")
        self.informacion_stacked_widget.setCurrentIndex(pagina)
        
    # NUEVA SESION
    # ///////////////////////////////////////////////////////////
    def ui_seleccionar_directorio(self, ubicacion_datos):
        '''------------
        DOCUMENTACIÓN -
        Muestra en el Operador la direccion seleccionada para la ubicacion de los datos.
        ------------'''
        self.directorio_entrada.setText(ubicacion_datos)

    @property # GETTER
    def paciente(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el nombre del paciente ingresado en el campo de texto
        ------------'''
        return self.nombre_entrada.text()
    # CALIBRACION
    # ///////////////////////////////////////////////////////////
    def ui_preparar_calibracion(self, paciente):
        '''------------
        DOCUMENTACIÓN -
        Prepara la sesion de calibracion.
        - Bloquea o modifica el comportamiento de los botones, paginas, etc cuando se selecciona "Preparar"
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.comenzar_terapia_boton.setEnabled(False)
        self.comenzar_calibracion_boton.setEnabled(True)
        self._mostrar_resumen(paciente, INDICE_RESUMEN)
    
    def ui_inhabilitar_preparacion_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Inhabilita las modificaciones cuando se prepara o se aplica la configuración de una sesión de Calibración
        - Bloquea el comportamiento de botones, paginas, etc
        ------------'''
        self.preparar_calibracion_boton.setEnabled(False)
        self.preparar_calibracion_boton.setText("Preparando...")
    
    def ui_habilitar_preparacion_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Habilita las modificaciones cuando se prepara o se aplica la configuración de una sesión de Calibración
        - Desbloquea el comportamiento de botones, paginas, etc
        ------------'''
        self.preparar_calibracion_boton.setEnabled(True)
        self.preparar_calibracion_boton.setText("Preparar")
            
    def ui_comenzar_calibracion(self, calibracion_tarea):
        '''------------
        DOCUMENTACIÓN -
        Comienza la sesion de calibracion.
        - Bloquea o modifica el comportamiento de los botones, paginas, etc cuando se selecciona "Comenzar"
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self._deshabilitar_cambios()
        if calibracion_tarea == 1:
                self.calibracion_estado_1.setText(constantes.MSG_REALIZANDO_TAREA)
        elif calibracion_tarea == 2:
                self.calibracion_estado_2.setText(constantes.MSG_REALIZANDO_TAREA)
        else:
                self.calibracion_estado_3.setText(constantes.MSG_REALIZANDO_TAREA)
    
    def ui_suspender_calibracion(self, calibracion_tarea):
        '''------------
        DOCUMENTACIÓN -
        Suspende la sesion de calibracion.
        - Desbloquea o modifica el comportamiento de los botones, paginas, etc cuando se selecciona "Suspender"
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self._habilitar_cambios()
        if calibracion_tarea == 1:
                self.calibracion_estado_1.setText(constantes.MSG_TAREA_SUSPENDIDA)
        elif calibracion_tarea == 2:
                self.calibracion_estado_2.setText(constantes.MSG_TAREA_SUSPENDIDA)
        else:
                self.calibracion_estado_3.setText(constantes.MSG_TAREA_SUSPENDIDA)
    
    def ui_finalizar_calibracion(self, calibracion_tarea):
        '''------------
        DOCUMENTACIÓN -
        Finaliza la sesion de calibracion.
        - Desbloquea o modifica el comportamiento de los botones, paginas, etc cuando se finaliza la tarea
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self._habilitar_cambios()
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
    def tipo_tarea(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el tipo de tarea seleccionada.
        ------------'''
        return self.tipo_tarea_opciones.currentText()
    
    @property # GETTER
    def nivel(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el nivel seleccionado.
        ------------'''
        return self.nivel_opciones.currentText()
    
    @property # GETTER
    def guia_visual(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve la opcion seleccionada de guia visual.
        ------------'''
        return self.guia_visual_opciones.currentText()
    
    def ui_aplicar_terapia(self, paciente):
        '''------------
        DOCUMENTACIÓN -
        Aplica las opciones seleccionadas para la sesion de terapia.
        - Bloquea o modifica el comportamiento de los botones, paginas, etc cuando se selecciona "Aplicar"
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.comenzar_terapia_boton.setEnabled(True)
        self.comenzar_calibracion_boton.setEnabled(False)
        self._mostrar_resumen(paciente, INDICE_RESUMEN)

    def ui_inhabilitar_aplicacion_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Inhabilita las modificaciones cuando se prepara o se aplica la configuración de una sesión de Terapia
        - Bloquea el comportamiento de botones, paginas, etc
        ------------'''
        self.aplicar_terapia_boton.setEnabled(False)
        self.aplicar_terapia_boton.setText("Aplicando...")
        
    def ui_habilitar_aplicacion_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Habilita las modificaciones cuando se prepara o se aplica la configuración de una sesión de Terapia
        - Desbloquea el comportamiento de botones, paginas, etc
        ------------'''
        self.aplicar_terapia_boton.setEnabled(True)
        self.aplicar_terapia_boton.setText("Aplicar")
    
    def ui_cargar_matriz(self, matriz):
        '''------------
        DOCUMENTACIÓN -
        Carga en el cuadro de texto la direccion de la matriz de clasificacion seleccionada.
        ------------'''
        self.archivo_calibracion_entrada.setText(matriz[0])
    
    def ui_comenzar_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Comienza la sesion de terapia.
        - Bloquea o modifica el comportamiento de los botones, paginas, etc cuando se selecciona "Comenzar"
        ------------'''
        self._deshabilitar_cambios()
    
    def ui_suspender_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Suspende la sesion de terapia.
        - Desbloquea o modifica el comportamiento de los botones, paginas, etc cuando se selecciona "Suspender"
        ------------'''
        self._habilitar_cambios()
        
    def ui_finalizar_terapia(self):
        '''------------
        DOCUMENTACIÓN -
        Finaliza la sesion de terapia.
        - Desbloquea o modifica el comportamiento de los botones, paginas, etc cuando se finaliza la tarea
        ------------'''
        self._habilitar_cambios()
    
    # RESUMEN SESION
    # ///////////////////////////////////////////////////////////
    def _mostrar_resumen(self, titulo, pagina):
        '''------------
        DOCUMENTACIÓN -
        Reemplaza la informacion de ¿Como empezar? por el resumen cuando se prepara una sesion de calibracion o terapia.
        ------------'''
        self.informacion_titulo.setText(titulo)
        self.informacion_stacked_widget.setCurrentIndex(pagina)
    
    def ui_iniciar_resumen(self, modo, tarea):
        '''------------
        DOCUMENTACIÓN -
        Inicia el resumen de la sesion.
        - Establece los valores iniciales antes de comenzar con la tarea
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.modo_resumen_texto.setText(modo)
        self.actividad_resumen_titulo.setText('Tarea')
        if modo == 'Terapia':
            self.actividad_resumen_titulo.setText(self.tipo_tarea)
        self.actividad_resumen_texto.setText(tarea)
        self.nivel_resumen_texto.setText(self.nivel)
        
        self.selecciones_resumen_texto.setText('-')
        self.correctas_resumen_texto.setText('-')
        self.incorrectas_resumen_texto.setText('-')
        
        self.estado_resumen_texto.setText('No iniciado')
        
    def ui_actualizar_selecciones(self, selecciones, correctas, incorrectas):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la informacion en el resumen.
        - Actualiza las selecciones realizadas
        ------------'''
        QtCore.QCoreApplication.processEvents()
        self.selecciones_resumen_texto.setText(str(selecciones))
        self.correctas_resumen_texto.setText(str(correctas))
        self.incorrectas_resumen_texto.setText(str(incorrectas))
        
    def ui_actualizar_estado(self, estado):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la informacion en el resumen.
        - Actualiza el estado de la sesion
        ------------'''
        self.estado_resumen_texto.setText(estado)
        
    def ui_actualizar_tiempo(self, tiempo_sesion):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la informacion en el resumen.
        - Actualiza el tiempo transcurrido de la sesion
        ------------'''
        self.tiempo_resumen_texto.setText(str(tiempo_sesion.minute).zfill(2) + ' min ' + str(tiempo_sesion.second).zfill(2) + ' s')