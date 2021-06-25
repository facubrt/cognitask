from datetime import datetime

# NUEVA SESION
class Sesion():

    # INICIALIZACION
    # ///////////////////////////////////////////////////////////
    def __init__(self):
        self.sesion_estado = "No iniciada" # estado de la sesión. No iniciada, Preparado, Realizando, Completado
        self.orden_secuencia = list(range(1, 10))
        self.siguiente_seleccion = 1 # indica la imagen siguiente que debe elegirse
        self.imagen_seleccionada = 0 # imagen seleccionada (necesario debido al orden aleatorio de las imagenes)
        self.target_seleccionado = 0 # target seleccionado
        self.calibracion_tarea = 1 # permite cambiar entre las distintas tareas de calibración automaticamente
        self.cantidad_pasos = 9 # cantidad de pasos que contiene la actividad. Por defecto son 9 pasos
        self.mostrar_guia = True
        self.intentos = 0 # suma 1 cada vez que el sujeto se equivoca en la sesion de terapia
        self.modo_calibracion = False
        self.run = 0
        self.tiempo_inicial = 0
        self.tiempo_sesion = 0
        self.actividad_completada = False
        self.sesion_iniciada = False # con False se informará en el resumen una nueva sesión. con True se escribirá dentro de la misma

    # 
    # ///////////////////////////////////////////////////////////
    def restablecer(self):
        self.sesion_iniciada = False # debido a que se cambia de tipo de terapia, se vuelve a escribir la seccion de sesión
        self.run = 0
        self.calibracion_tarea = 1
        
    # TEMPORIZADOR
    # ///////////////////////////////////////////////////////////

    # Temporizador para conocer la duracion de cada sesion
    def iniciarTiempo(self):
        self.tiempo_inicial = datetime.now()

    def actualizarTiempo(self):
        diferencia = datetime.now() - self.tiempo_inicial
        tiempo_referencia = datetime(self.tiempo_inicial.year, self.tiempo_inicial.month, self.tiempo_inicial.day, 0, 0, 0)
        self.tiempo_sesion = tiempo_referencia + diferencia
