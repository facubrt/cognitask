import os

UBICACION_PUNTO = 4
UBICACION_ESPACIO = 6

# REALIMENTACION
class EvaluacionSelecciones():
    
    # MODO POR DEFECTO. Palabras, Sucesiones, Rompecabezas
    def evaluar_seleccion(self):
        # cuando acierta
        if self.sesion.imagen_seleccionada == self.sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif self.sesion.imagen_seleccionada != self.sesion.siguiente_seleccion:
            return False
        
    def evaluar_palabras_reves(self):
        siguiente_seleccion = (self.sesion.cantidad_pasos + 1) - self.sesion.siguiente_seleccion
        # cuando acierta
        if self.sesion.imagen_seleccionada == siguiente_seleccion:
            return True 
        # cuando no acierta
        elif self.sesion.imagen_seleccionada != siguiente_seleccion:
            return False
 
    def evaluar_rompecabezas_me(self):
        punto = os.path.isfile(self.sesion.ubicacion_img + "/img" + str(self.sesion.siguiente_seleccion) + " - punto.png")
        if self.sesion.imagen_seleccionada == UBICACION_PUNTO and punto:
            return True
        elif self.sesion.imagen_seleccionada == UBICACION_ESPACIO and punto is False:
            return True
        else:
            return False