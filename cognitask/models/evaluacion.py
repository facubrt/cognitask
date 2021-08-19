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

UBICACION_PUNTO = 4
UBICACION_ESPACIO = 6

# REALIMENTACION
class Evaluacion():
      
    def evaluar_seleccion(tipo_tarea, sesion):
        '''------------
        DOCUMENTACIÓN -
        Evalua la seleccion en una sesion de terapia dependiendo del tipo de tarea utilizada.
        - Determina si una seleccion es correcta segun el tipo utilizado
        ------------'''
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
        '''------------
        DOCUMENTACIÓN -
        Evalua la seleccion correcta / incorrecta en el tipo de tarea Palabras.
        - Determina si una seleccion es correcta durante la realizacion de un tipo de tarea Palabras
        ------------'''
        # cuando acierta
        if sesion.imagen_seleccionada == sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif sesion.imagen_seleccionada != sesion.siguiente_seleccion:
            return False
    
    def modo_palabras_invertido(sesion):
        '''------------
        DOCUMENTACIÓN -
        Evalua la seleccion correcta / incorrecta en el tipo de tarea Palabras en sentido invertido.
        - Determina si una seleccion es correcta durante la realizacion de un tipo de tarea Palabras cuando se deben seleccionar las letras de forma invertida
        ------------'''
        siguiente_seleccion = (sesion.cantidad_pasos + 1) - sesion.siguiente_seleccion
        # cuando acierta
        if sesion.imagen_seleccionada == siguiente_seleccion:
            return True 
        # cuando no acierta
        elif sesion.imagen_seleccionada != siguiente_seleccion:
            return False
    
    def modo_sucesiones(sesion):
        '''------------
        DOCUMENTACIÓN -
        Evalua la seleccion correcta / incorrecta en el tipo de tarea Sucesiones.
        - Determina si una seleccion es correcta durante la realizacion de un tipo de tarea Sucesiones
        ------------'''
        # cuando acierta
        if sesion.imagen_seleccionada == sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif sesion.imagen_seleccionada != sesion.siguiente_seleccion:
            return False
    
    def modo_rompecabezas(sesion):
        '''------------
        DOCUMENTACIÓN -
        Evalua la seleccion correcta / incorrecta en el tipo de tarea Rompecabezas.
        - Determina si una seleccion es correcta durante la realizacion de un tipo de tarea Rompecabezas
        ------------'''
        # cuando acierta
        if sesion.imagen_seleccionada == sesion.siguiente_seleccion:
            return True
        # cuando no acierta
        elif sesion.imagen_seleccionada != sesion.siguiente_seleccion:
            return False
    
    def modo_rompecabezas_me(sesion):
        '''------------
        DOCUMENTACIÓN -
        Evalua la seleccion correcta / incorrecta en el tipo de tarea Rompecabezas cuando se utiliza el modo de memoria espacial.
        - Determina si una seleccion es correcta durante la realizacion de un tipo de tarea Rompecabezas en el modo de memoria espacial. Solo pueden seleccionarse un punto o un espacio en este modo.
        ------------'''
        punto = os.path.isfile(sesion.ubicacion_img + "/img" + str(sesion.siguiente_seleccion) + " - punto.png")
        if sesion.imagen_seleccionada == UBICACION_PUNTO and punto:
            return True
        elif sesion.imagen_seleccionada == UBICACION_ESPACIO and punto is False:
            return True
        else:
            return False