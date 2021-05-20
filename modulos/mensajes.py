import modulos.constantes as constantes
from PyQt5 import QtCore
import modulos.progreso as progreso
import modulos.informacion as informacion

# MENSAJES

def realimentacion(self):
    # modo terapia
    # cuando acierta y no es la ultima
    if self.imagen_seleccionada == self.siguiente_seleccion and self.siguiente_seleccion != self.cantidad_pasos and self.modo_calibracion == False:
        mostrar(self, constantes.MSG_CORRECTO, constantes.CSS_MSG_CORRECTO, True)
        self.intentos = 0
        progreso.actualizar(self)
        self.selecciones_correctas += 1
        self.selecciones_realizadas += 1
        self.siguiente_seleccion = self.siguiente_seleccion + 1
    # cuando acierta y es la ultima
    elif self.imagen_seleccionada == self.siguiente_seleccion and self.siguiente_seleccion == self.cantidad_pasos and self.modo_calibracion == False:
        progreso.actualizar(self)
        self.intentos = 0
        self.selecciones_correctas += 1
        self.selecciones_realizadas += 1
        informacion.actualizar(self)
        self.terapiaFinalizada()
    # cuando no acierta
    elif self.imagen_seleccionada != self.siguiente_seleccion and self.intentos < constantes.INTENTOS_MAXIMOS and self.modo_calibracion == False:
        mostrar(self, constantes.MSG_INCORRECTO, constantes.CSS_MSG_INCORRECTO, True)
        self.intentos += 1
        self.selecciones_incorrectas += 1
        self.selecciones_realizadas += 1
    
    # cuando se equivoca INTENTOS_MAXIMOS veces, y es la ultima selección
    elif self.imagen_seleccionada != self.siguiente_seleccion and self.siguiente_seleccion == self.cantidad_pasos and self.modo_calibracion == False and self.intentos == constantes.INTENTOS_MAXIMOS:
        progreso.siguientePaso(self)
        self.intentos = 0 # restablecemos los valores de intentos
        self.selecciones_incorrectas += 1
        self.selecciones_realizadas += 1
        informacion.actualizar(self)
        self.terapiaFinalizada()
    
    # cuando se equivoca INTENTOS_MAXIMOS veces y no es la ultima
    elif self.imagen_seleccionada != self.siguiente_seleccion and self.intentos == constantes.INTENTOS_MAXIMOS and self.modo_calibracion == False and self.siguiente_seleccion != self.cantidad_pasos:
        mostrar(self, constantes.MSG_PASAR, constantes.CSS_MSG_PASAR, True)
        progreso.siguientePaso(self)
        self.intentos = 0
        self.selecciones_incorrectas += 1
        self.selecciones_realizadas += 1
        self.siguiente_seleccion = self.siguiente_seleccion + 1
    
    # modo calibracion
    if self.modo_calibracion == True and self.siguiente_seleccion != constantes.PASOS_CALIBRACION:
        if self.imagen_seleccionada != self.siguiente_seleccion:
            self.selecciones_incorrectas += 1
        else:
            self.selecciones_correctas += 1
        
        if self.calibracion_tarea == 1:
            msg_calibracion = "Elige la letra " + constantes.TAREA_UNO[self.siguiente_seleccion]
        elif self.calibracion_tarea == 2:
            msg_calibracion = "Elige la letra " + constantes.TAREA_DOS[self.siguiente_seleccion]
        elif self.calibracion_tarea == 3:
            msg_calibracion = "Elige la letra " + constantes.TAREA_TRES[self.siguiente_seleccion]
        
        mostrar(self, msg_calibracion, constantes.CSS_MSG_CALIBRACION, True)
        progreso.actualizar(self)
        self.siguiente_seleccion = self.siguiente_seleccion + 1
        self.selecciones_realizadas += 1

    elif self.modo_calibracion == True and self.siguiente_seleccion == constantes.PASOS_CALIBRACION:
        if self.imagen_seleccionada != self.siguiente_seleccion:
            self.selecciones_incorrectas += 1
        else:
            self.selecciones_correctas += 1
        self.selecciones_realizadas += 1
        progreso.actualizar(self)
        self.calibracionFinalizada()

    informacion.actualizar(self) # informa al operador de la seleccion

def terminar(app):
    app.feedback_label.hide()
    app.feedback_label.setStyleSheet(constantes.CSS_MSG_CORRECTO) # restaura valores por defecto

# ocultar indica si se incluye un temporizador o no en el mensaje.
def mostrar(self, mensaje, estilo, ocultar):
    
    self.BCIAplicacion.feedback_label.setText(mensaje)
    self.BCIAplicacion.feedback_label.setStyleSheet(estilo)
    self.BCIAplicacion.feedback_label.show()
    if ocultar == True:
        QtCore.QTimer.singleShot(2000, lambda: terminar(self.BCIAplicacion))

def restablecer(self):
    terminar(self.BCIAplicacion)    