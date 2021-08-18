import os

UBICACION_PUNTO = 4
UBICACION_ESPACIO = 6

# REALIMENTACION
class Evaluacion():
      
    def evaluar_seleccion(tipo_tarea, sesion):
        if tipo_tarea == 'Palabras':
            seleccion = Evaluacion.modo_palabras(sesion)
        elif tipo_tarea == 'Palabras - al revés':
            seleccion = Evaluacion.modo_palabras_invertido(sesion)
        elif tipo_tarea == 'Sucesiones':
            seleccion = Evaluacion.modo_sucesiones(sesion)
        elif tipo_tarea == 'Rompecabezas':
            seleccion = Evaluacion.modo_rompecabezas(sesion)
        elif tipo_tarea == 'Rompecabezas - mem. espacial':
            seleccion = Evaluacion.modo_rompecabezas_me(sesion)
        else:
            raise Exception('El tipo de tarea no es correcto')
        
        return seleccion
    
    def modo_palabras(sesion):
        # cuando acierta
        if sesion.imagen_seleccionada == sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif sesion.imagen_seleccionada != sesion.siguiente_seleccion:
            return False
    
    def modo_palabras_invertido(sesion):
        siguiente_seleccion = (sesion.cantidad_pasos + 1) - sesion.siguiente_seleccion
        # cuando acierta
        if sesion.imagen_seleccionada == siguiente_seleccion:
            return True 
        # cuando no acierta
        elif sesion.imagen_seleccionada != siguiente_seleccion:
            return False
    
    def modo_sucesiones(sesion):
        # cuando acierta
        if sesion.imagen_seleccionada == sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif sesion.imagen_seleccionada != sesion.siguiente_seleccion:
            return False
    
    def modo_rompecabezas(sesion):
        # cuando acierta
        if sesion.imagen_seleccionada == sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif sesion.imagen_seleccionada != sesion.siguiente_seleccion:
            return False
    
    def modo_rompecabezas_me(sesion):
        punto = os.path.isfile(sesion.ubicacion_img + "/img" + str(sesion.siguiente_seleccion) + " - punto.png")
        if sesion.imagen_seleccionada == UBICACION_PUNTO and punto:
            return True
        elif sesion.imagen_seleccionada == UBICACION_ESPACIO and punto is False:
            return True
        else:
            return False