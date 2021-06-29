from cognitask.common import ubicaciones
from datetime import datetime

# NUEVA SESION
class Sesion():

    # INICIALIZACION
    # ///////////////////////////////////////////////////////////
    def __init__(self):
        
        # Estados
        self.estado_sesion = "No iniciada" # estado de la sesión. No iniciada, Preparado, Realizando, Completado
        
        # Ubicaciones
        self.ubicacion_img = ubicaciones.UBICACION_IMG
        self.ubicacion_datos = ubicaciones.UBICACION_DATOS 
        self.ubicacion_clasificador = ubicaciones.UBICACION_CLASIFICADOR
        
        #Tarea
        self.modo_calibracion = False
        self.orden_secuencia = list(range(1, 10))
        self.__indice_tarea = 1
        self.__tarea_calibracion = 'TAREA'
        self.cantidad_pasos = 9 # cantidad de pasos que contiene la actividad. Por defecto son 9 pasos
        self.__intentos = 0 # suma 1 cada vez que el sujeto se equivoca en la sesion de terapia
        self.run = 0
        
        self.tiempo_inicial = 0
        self.tiempo_sesion = 0
        self.actividad_completada = False
        self.sesion_iniciada = False # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma
        
        # Selecciones
        self.__siguiente_seleccion = 1 # indica la imagen siguiente que debe elegirse
        self.imagen_seleccionada = 0 # imagen seleccionada (necesario debido al orden aleatorio de las imagenes)
        
        self.__selecciones_realizadas = 0
        self.__selecciones_correctas = 0
        self.__selecciones_incorrectas = 0
        self.__porcentaje_aciertos = 0

    # SESION
    # ///////////////////////////////////////////////////////////
    def restablecer(self):
        self.sesion_iniciada = False # debido a que se cambia de tipo de terapia, se vuelve a escribir la seccion de sesión
        self.run = 0
        self.calibracion_tarea = 1
      
    def actualizar_estado(self, estado):
        self.estado_sesion = estado
    
    @property # GETTER
    def estado(self):
        return self.estado_sesion
      
    # TAREA
    # ///////////////////////////////////////////////////////////
    @property # GETTER
    def indice_tarea(self):
        return self.__indice_tarea
    
    # SETTER
    def actualizar_indice_tarea(self):
        if (self.__indice_tarea < 3):
            self.__indice_tarea += 1
        else:
            self.__indice_tarea = 1
            
    def actualizar_tarea_calibracion(self, tarea):
        self.__tarea_calibracion = tarea
    
    @property # GETTER
    def tarea_calibracion(self):
        return self.__tarea_calibracion
    
    # SELECCIONES
    # ///////////////////////////////////////////////////////////
    def restablecer_selecciones(self):
        self.__siguiente_seleccion = 1
        self.__selecciones_realizadas = 0
        self.__selecciones_correctas = 0
        self.__selecciones_incorrectas = 0 
        self.__porcentaje_aciertos = 0  
    
    def actualizar_selecciones_realizadas(self):
        self.__selecciones_realizadas += 1
    
    def actualizar_selecciones_correctas(self):
        self.__selecciones_correctas += 1
        self.__selecciones_realizadas += 1
    
    def actualizar_selecciones_incorrectas(self):
        self.__selecciones_incorrectas += 1
        self.__selecciones_realizadas += 1
    
    def actualizar_siguiente_seleccion(self):
        self.__siguiente_seleccion +=1
    
    @property # GETTER
    def porcentaje_aciertos(self):
        self.__porcentaje_aciertos = round((self.__selecciones_correctas / self.__selecciones_realizadas) * 100)
        return self.__porcentaje_aciertos
    
    @property # GETTER
    def siguiente_seleccion(self):
        return self.__siguiente_seleccion  
    
    @property # GETTER
    def selecciones_correctas(self):
        return self.__selecciones_correctas   
    
    @property # GETTER
    def selecciones_incorrectas(self):
        return self.__selecciones_incorrectas
    
    @property # GETTER
    def selecciones_realizadas(self):
        return self.__selecciones_realizadas
    
    @property # GETTER
    def intentos(self):
        return self.__intentos
    
    def restablecer_intentos(self):
        self.__intentos = 0
    
    def actualizar_intentos(self):
        if self.__intentos < 3:
            self.__intentos += 1
        else:
            self.__intentos = 0
        
    # TEMPORIZADOR
    # ///////////////////////////////////////////////////////////

    # Temporizador para conocer la duracion de cada sesion
    def iniciar_tiempo(self):
        self.tiempo_inicial = datetime.now()

    def actualizar_tiempo(self):
        diferencia = datetime.now() - self.tiempo_inicial
        tiempo_referencia = datetime(self.tiempo_inicial.year, self.tiempo_inicial.month, self.tiempo_inicial.day, 0, 0, 0)
        self.tiempo_sesion = tiempo_referencia + diferencia
