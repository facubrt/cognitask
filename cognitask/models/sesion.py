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

from cognitask.common import ubicaciones
from datetime import datetime

# NUEVA SESION
class Sesion():

    # INICIALIZACION
    # ///////////////////////////////////////////////////////////
    def __init__(self):
        '''------------
        DOCUMENTACIÓN -
        Inicializa Sesion.
        - Establece los valores predeterminados para cada variable de la sesion.
        ------------'''
        # Estados
        self.__estado_sesion = 'No iniciada' # estado de la sesión. No iniciada, Preparado, Realizando, Completado
        # Ubicaciones
        self.ubicacion_img = ubicaciones.UBICACION_IMG
        self.__ubicacion_datos = ubicaciones.UBICACION_DATOS 
        self.ubicacion_clasificador = ubicaciones.UBICACION_CLASIFICADOR
        #Tarea
        self.modo_calibracion = False
        self.orden_secuencia = list(range(1, 10))
        self.__indice_tarea = 1
        self.__tarea_calibracion = 'TAREA'
        self.cantidad_pasos = 9 # cantidad de pasos que contiene la actividad. Por defecto son 9 pasos
        self.cantidad_distractores = 0
        self.__intentos = 0 # suma 1 cada vez que el sujeto se equivoca en la sesion de terapia
        self.__corrida = 0
        self.tiempo_inicial = 0
        self.tiempo_sesion = 0
        self.actividad_completada = False
        #self.sesion_iniciada = False # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma
        # Selecciones
        self.__siguiente_seleccion = 1 # indica la imagen siguiente que debe elegirse
        self.__imagen_seleccionada = 0 # imagen seleccionada (necesario debido al orden aleatorio de las imagenes)
        self.__selecciones_realizadas = 0
        self.__selecciones_correctas = 0
        self.__selecciones_incorrectas = 0
        self.__porcentaje_aciertos = 0

    # SESION
    # ///////////////////////////////////////////////////////////
    def restablecer(self):
        '''------------
        DOCUMENTACIÓN -
        Restablece los valores de la sesion por defecto.
        - Restablece el estado de la sesion, las selecciones, etc.
        ------------'''
        self.__estado_sesion = 'No iniciada'
        self.__corrida = 0
        self.__indice_tarea = 1
        self.__tarea_calibracion = 'TAREA'
        self.__intentos = 0
        self.tiempo_sesion = 0
        self.actividad_completada = False
        self.__siguiente_seleccion = 1 
        self.__imagen_seleccionada = 0 
        self.__selecciones_realizadas = 0
        self.__selecciones_correctas = 0
        self.__selecciones_incorrectas = 0
        self.__porcentaje_aciertos = 0
      
    def actualizar_estado(self, estado):
        '''------------
        DOCUMENTACIÓN -
        Actualiza el estado de la sesion.
        - Los estados posibles son No iniciada, Preparado, Realizando y Completado.
        ------------'''
        self.__estado_sesion = estado
    
    @property # GETTER
    def estado(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el estado actual de la sesion.
        - Los estados posibles son No iniciada, Preparado, Realizando y Completado.
        ------------'''
        return self.__estado_sesion
    
    @property # GETTER
    def corrida(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el numero de Corrida actual.
        - Devuelve el numero de Corrida actual.
        ------------'''
        return self.__corrida  
    
    def actualizar_corrida(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza el numero de Corrida.
        - Incrementa el numero de Corrida
        ------------'''
        self.__corrida += 1
        
    @property # GETTER
    def ubicacion_datos(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve la ubicacion de los datos del paciente.
        - Retorna la direccion donde se encuentran los datos de la sesion
        ------------'''
        return self.__ubicacion_datos
    
    def actualizar_ubicacion_datos(self, ubicacion_datos):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la ubicacion de los datos del paciente.
        - Modifica la direccion donde se encuentran los datos de la sesion
        ------------'''
        self.__ubicacion_datos = ubicacion_datos
    
    # TAREA
    # ///////////////////////////////////////////////////////////
    @property # GETTER
    def indice_tarea(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el numero de tarea de calibracion actual.
        - Permite saber cual es la tarea preestablecida que debe realizarse a continuacion.
        ------------'''
        return self.__indice_tarea
    
    # SETTER
    def actualizar_indice_tarea(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza el numero de tarea de calibracion actual.
        - Las tareas preestablecidas de calibracion son tres y se encuentran en cognitask/calibracion
        ------------'''
        if (self.__indice_tarea < 3):
            self.__indice_tarea += 1
        else:
            self.__indice_tarea = 1
            
    def actualizar_tarea_calibracion(self, tarea):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la tarea de calibracion actual.
        - Actualiza la tarea de calibracion actual
        ------------'''
        self.__tarea_calibracion = tarea
    
    @property # GETTER
    def tarea_calibracion(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve la tarea de calibracion actual (directorio).
        - Devuelve el directorio de la tarea de calibracion actual
        ------------'''
        return self.__tarea_calibracion
    
    # SELECCIONES
    # ///////////////////////////////////////////////////////////
    def restablecer_selecciones(self):
        '''------------
        DOCUMENTACIÓN -
        Restablece las selecciones realizadas y los intentos.
        - Vuelve a los valores por defecto de las selecciones realizadas y los intentos
        ------------'''
        self.__siguiente_seleccion = 1
        self.__selecciones_realizadas = 0
        self.__selecciones_correctas = 0
        self.__selecciones_incorrectas = 0 
        self.__porcentaje_aciertos = 0
        self.__intentos = 0 
    
    def actualizar_selecciones_realizadas(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza las selecciones realizadas .
        - Incrementa las selecciones realizadas
        ------------'''
        self.__selecciones_realizadas += 1
    
    def actualizar_selecciones_correctas(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza las selecciones realizadas y las correctas.
        - Incrementa las selecciones realizadas y las correctas.
        ------------'''
        self.__selecciones_correctas += 1
        self.__selecciones_realizadas += 1
    
    def actualizar_selecciones_incorrectas(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza las selecciones realizadas y las incorrectas.
        - Incrementa las selecciones realizadas y las incorrectas.
        ------------'''
        self.__selecciones_incorrectas += 1
        self.__selecciones_realizadas += 1
    
    def actualizar_siguiente_seleccion(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la siguiente seleccion.
        - Incrementa el numero de la seleccion siguiente.
        ------------'''
        self.__siguiente_seleccion +=1
    
    @property # GETTER
    def porcentaje_aciertos(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el porcentaje de acierto durante la tarea.
        - Determina el porcentaje de aciertos y retorna su valor.
        ------------'''
        if self.__selecciones_realizadas > 0:
            self.__porcentaje_aciertos = round((self.__selecciones_correctas / self.__selecciones_realizadas) * 100)
        return self.__porcentaje_aciertos
    
    @property # GETTER
    def siguiente_seleccion(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el numero de seleccion siguiente.
        - Determina el numero de la seleccion o paso siguiente.
        ------------'''
        return self.__siguiente_seleccion  
    
    @property # GETTER
    def selecciones_correctas(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve las selecciones correctas realizadas.
        - Devuelve las selecciones correctas realizadas.
        ------------'''
        return self.__selecciones_correctas   
    
    @property # GETTER
    def selecciones_incorrectas(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve las selecciones incorrectas realizadas.
        - Devuelve las selecciones incorrectas realizadas.
        ------------'''
        return self.__selecciones_incorrectas
    
    @property # GETTER
    def selecciones_realizadas(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve las selecciones totales realizadas.
        - Devuelve las selecciones totales realizadas.
        ------------'''
        return self.__selecciones_realizadas
    
    @property # GETTER
    def intentos(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el numero de intentos posibles.
        - Los intentos permiten una cantidad determinada de equivocaciones en una sesion de terapia.
        ------------'''
        return self.__intentos
    
    @property # GETTER
    def imagen_seleccionada(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve la imagen seleccionada.
        - Devuelve la imagen seleccionada.
        ------------'''
        return self.__imagen_seleccionada
    
    def actualizar_imagen_seleccionada(self, imagen_seleccionada):
        '''------------
        DOCUMENTACIÓN -
        Actualiza la imagen seleccionada.
        - Actualiza la imagen seleccionada.
        ------------'''
        self.__imagen_seleccionada = imagen_seleccionada
    
    def restablecer_intentos(self):
        '''------------
        DOCUMENTACIÓN -
        Restablece los intentos.
        - Vuelve a cero el numero de intentos realizados, permitiendo asi nuevamente un maximo numero de equivocaciones.
        ------------'''
        self.__intentos = 0
    
    def actualizar_intentos(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza el numero de intentos realizados.
        - Cuando los intentos alcanzan el maximo, se reestablecen y se pasa a la siguiente imagen.
        ------------'''
        if self.__intentos < 3:
            self.__intentos += 1
        else:
            self.__intentos = 0
        
    # TEMPORIZADOR
    # ///////////////////////////////////////////////////////////
    def iniciar_tiempo(self):
        '''------------
        DOCUMENTACIÓN -
        Inicia el temporizador para saber la duracion de la sesion.
        - Inicia el temporizador.
        ------------'''
        self.tiempo_inicial = datetime.now()

    def actualizar_tiempo(self):
        '''------------
        DOCUMENTACIÓN -
        Actualiza el temporizador para saber la duracion de la sesion.
        - Actualiza el temporizador.
        ------------'''
        diferencia = datetime.now() - self.tiempo_inicial
        tiempo_referencia = datetime(self.tiempo_inicial.year, self.tiempo_inicial.month, self.tiempo_inicial.day, 0, 0, 0)
        self.tiempo_sesion = tiempo_referencia + diferencia
