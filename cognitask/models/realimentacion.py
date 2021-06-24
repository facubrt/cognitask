import os
import cognitask.common.constantes as constantes
import cognitask.models.progreso as progreso
import cognitask.models.informacion as informacion
import cognitask.models.mensajes as mensajes

# REALIMENTACION
def realimentar(self, calibracion):
    # TERAPIA
    if calibracion is False:
        
        if self.tipo_tarea_opciones.currentText() == 'Rompecabezas - mem. espacial':
            img_seleccionada = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + " - punto.png"
            img_siguiente = self.ubicacion_img + "/img" + str(self.siguiente_seleccion) + " - punto.png"
            # si la imagen seleccionada es un punto (TRUE) y si la imagen siguiente que debe seleccionarse es punto (TRUE)
            # si son TRUE y TRUE es correcto, si son FALSE y FALSE es correcto
            if os.path.isfile(img_seleccionada) == os.path.isfile(img_siguiente):
                seleccionCorrecta(self, calibracion)
            else:
                seleccionIncorrecta(self, calibracion)
            
        elif self.tipo_tarea_opciones.currentText() == 'Palabras - al revés':
            siguiente_seleccion = (self.cantidad_pasos + 1) - self.siguiente_seleccion
            # cuando acierta
            if self.imagen_seleccionada == siguiente_seleccion:
                seleccionCorrecta(self, calibracion) 
            # cuando no acierta
            elif self.imagen_seleccionada != siguiente_seleccion:
                seleccionIncorrecta(self, calibracion)
            
        # otros tipos de tarea    
        else:
            # cuando acierta
            if self.imagen_seleccionada == self.siguiente_seleccion:
                seleccionCorrecta(self, calibracion) 
            # cuando no acierta
            elif self.imagen_seleccionada != self.siguiente_seleccion:
                seleccionIncorrecta(self, calibracion)
        
    # CALIBRACION
    elif calibracion is True:    
        
        if self.siguiente_seleccion != constantes.PASOS_CALIBRACION:
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
            
            mensajes.mostrar(self, msg_calibracion, constantes.CSS_MSG_CALIBRACION, True)
            progreso.actualizar(self, calibracion)
            self.siguiente_seleccion = self.siguiente_seleccion + 1
            self.selecciones_realizadas += 1

        elif self.siguiente_seleccion == constantes.PASOS_CALIBRACION:
            if self.imagen_seleccionada != self.siguiente_seleccion:
                self.selecciones_incorrectas += 1
            else:
                self.selecciones_correctas += 1
            self.selecciones_realizadas += 1
            progreso.actualizar(self, calibracion)
            self.finalizarCalibracion()

    # INFORMAR SELECCION
    #informacion.actualizar(self, calibracion) # informa al operador de la seleccion
    
# ///////////////////////////////////////////////////////////

def seleccionCorrecta(self, calibracion):
    if self.siguiente_seleccion < self.cantidad_pasos:
        mensajes.mostrar(self, constantes.MSG_CORRECTO, constantes.CSS_MSG_CORRECTO, True)
        self.intentos = 0
        progreso.actualizar(self, calibracion)
        self.selecciones_correctas += 1
        self.selecciones_realizadas += 1
        informacion.actualizar(self, calibracion) # informa al operador de la seleccion
        self.siguiente_seleccion = self.siguiente_seleccion + 1
    else:
        progreso.actualizar(self, calibracion)
        self.intentos = 0
        self.selecciones_correctas += 1
        self.selecciones_realizadas += 1
        informacion.actualizar(self, calibracion)
        self.finalizarTerapia()
        
def seleccionIncorrecta(self, calibracion):
    if self.intentos < constantes.INTENTOS_MAXIMOS:
        mensajes.mostrar(self, constantes.MSG_INCORRECTO, constantes.CSS_MSG_INCORRECTO, True)
        self.intentos += 1
        self.selecciones_incorrectas += 1
        self.selecciones_realizadas += 1
        informacion.actualizar(self, calibracion) # informa al operador de la seleccion
    elif self.intentos == constantes.INTENTOS_MAXIMOS and self.siguiente_seleccion == self.cantidad_pasos:
        progreso.siguientePaso(self)
        self.intentos = 0 # restablecemos los valores de intentos
        self.selecciones_incorrectas += 1
        self.selecciones_realizadas += 1
        informacion.actualizar(self, calibracion)
        self.finalizarTerapia()
    elif self.intentos == constantes.INTENTOS_MAXIMOS and self.siguiente_seleccion != self.cantidad_pasos:
        mensajes.mostrar(self, constantes.MSG_PASAR, constantes.CSS_MSG_PASAR, True)
        progreso.siguientePaso(self)
        self.intentos = 0
        self.selecciones_incorrectas += 1
        self.selecciones_realizadas += 1
        self.siguiente_seleccion = self.siguiente_seleccion + 1
        informacion.actualizar(self, calibracion) # informa al operador de la seleccion