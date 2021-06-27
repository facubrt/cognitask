import os

# REALIMENTACION
class EvaluacionSelecciones():
    
    def evaluar_atencion(self):
        # cuando acierta
        if self.imagen_seleccionada == self.siguiente_seleccion:
            return True
        # cuando no acierta
        elif self.imagen_seleccionada != self.siguiente_seleccion:
            return False
    
    def evaluar_atencion_inversa(self):
        siguiente_seleccion = (self.cantidad_pasos + 1) - self.siguiente_seleccion
        # cuando acierta
        if self.imagen_seleccionada == siguiente_seleccion:
            return True 
        # cuando no acierta
        elif self.imagen_seleccionada != siguiente_seleccion:
            return False

    def evaluar_memoria_espacial(self):
        # TRUE si el archivo existe, FALSE si no
        # Evaluo si la imagen seleccionada es un punto (TRUE) y si la imagen siguiente que debe seleccionarse es punto (TRUE)
        img_seleccionada = os.path.isfile(self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + " - punto.png")
        img_siguiente = os.path.isfile(self.ubicacion_img + "/img" + str(self.siguiente_seleccion) + " - punto.png")
        # si son TRUE y TRUE es correcto, si son FALSE y FALSE es correcto
        if img_seleccionada == img_siguiente:
            return True
        else:
            return False
