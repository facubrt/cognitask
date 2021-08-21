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

import random
import os
from PyQt5 import QtCore
import cognitask.common.constantes as constantes
from cognitask.common import ubicaciones

class Parametros():
    
    def aplicar_nivel_terapia(nivel_seleccionado):
        '''------------
        DOCUMENTACIÓN -
        Escribe los parametros correspondientes al nivel seleccionado durante una sesion de terapia.
        - Modifica el documento nivel.prm ubicado en  cognitask/config
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        fout = open("config/nivel.prm", "wt")

        if nivel_seleccionado == "Avanzado":
            nivel = constantes.NIVEL_AVANZADO
        elif nivel_seleccionado == "Intermedio":
            nivel = constantes.NIVEL_INTERMEDIO
        else:
            nivel = constantes.NIVEL_INICIAL

        NumberOfSequences = "Application:Sequencing int NumberOfSequences= " + str(nivel) + " 15 1 % // number of sequences in a set of intensifications\n"
        EpochsToAverage = "Filtering:P3TemporalFilter int EpochsToAverage= " + str(nivel) + " 1 0 % // Number of epochs to average"
        fout.write(NumberOfSequences)
        fout.write(EpochsToAverage)
        fout.close()
    
    def aplicar_nivel_calibracion():
        '''------------
        DOCUMENTACIÓN -
        Escribe los parametros correspondientes al nivel seleccionado durante una sesion de calibracion.
        - Modifica el documento nivel.prm ubicado en  cognitask/config
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        fout = open("config/nivel.prm", "wt")
        
        nivel = constantes.NIVEL_CALIBRACION

        NumberOfSequences = "Application:Sequencing int NumberOfSequences= " + str(nivel) + " 15 1 % // number of sequences in a set of intensifications\n"
        EpochsToAverage = "Filtering:P3TemporalFilter int EpochsToAverage= " + str(nivel) + " 1 0 % // Number of epochs to average"
        fout.write(NumberOfSequences)
        fout.write(EpochsToAverage)
        fout.close()
    
    def aplicar_tarea_calibracion(sesion):
        '''------------
        DOCUMENTACIÓN -
        Escribe los parametros correspondientes a la tarea seleccionada durante una sesion de calibracion.
        - Modifica el documento secuencia.prm ubicado en  cognitask/config
        - Utiliza tres tareas preestablecidas ubicadas en cognitask/calibracion
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        fout = open("config/secuencia.prm", "wt")
        fout.write("Application:Speller%20Targets matrix TargetDefinitions= 9 { Display Enter Display%20Size Icon%20File Sound Intensified%20Icon } ")
        
        if sesion.indice_tarea == 1:
            sesion.ubicacion_img = ubicaciones.INSTALL_DIR + "/calibracion/tarea 1"
            # esto es necesario para BCI2000, ya que permite conocer como se ordenaran las imagenes en la matriz
            lista = constantes.LISTA_UNO
            orden_sec = constantes.ORDEN_UNO
            text_to_spell = "Application:Speller string TextToSpell= " + constantes.TAREA_UNO + " // character or string to spell in offline copy mode"
        elif sesion.indice_tarea == 2:
            sesion.ubicacion_img = ubicaciones.INSTALL_DIR + "/calibracion/tarea 2"
            # esto es necesario para BCI2000, ya que permite conocer como se ordenaran las imagenes en la matriz
            lista = constantes.LISTA_DOS
            orden_sec = constantes.ORDEN_DOS
            text_to_spell = "Application:Speller string TextToSpell= " + constantes.TAREA_DOS + " // character or string to spell in offline copy mode"
        else:
            sesion.ubicacion_img = ubicaciones.INSTALL_DIR + "/calibracion/tarea 3"
            # esto es necesario para BCI2000, ya que permite conocer como se ordenaran las imagenes en la matriz
            lista = constantes.LISTA_TRES
            orden_sec = constantes.ORDEN_TRES
            text_to_spell = "Application:Speller string TextToSpell= " + constantes.TAREA_TRES + " // character or string to spell in offline copy mode"
            
        ubicacion_img = sesion.ubicacion_img.replace(' ', '%20')
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        for i in range(0, 9):
            orden_img = lista[i] + ubicacion_img + "/img" + str(orden_sec[i]) + ".png % % "
            fout.write(orden_img)
        fout.write("// speller target properties\n")
        fout.write(text_to_spell)
        fout.close()
        sesion.orden_secuencia = orden_sec
    
    def aplicar_tarea_terapia(sesion, tipo_tarea):
        '''------------
        DOCUMENTACIÓN -
        Escribe los parametros correspondientes al nivel seleccionado durante una sesion de terapia.
        - Modifica el documento secuencia.prm ubicado en  cognitask/config
        - Distribuye las imagenes de la tarea seleccionada en forma aleatoria
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        orden_secuencia = list(range(1, 10))
        # cuenta la cantidad de imagenes presentes en la tarea, considerando las correctas y los distractores
        elementos = sesion.cantidad_pasos + sesion.cantidad_distractores
        if elementos < 9:
            for i in range(elementos, 9):
                orden_secuencia[i] = 0
        # escribimos el archivo de configuracion BCI2000
        # el archivo de configuracion de BCI2000 necesita que los espacios sean indicados con '%20'
        img_path = sesion.ubicacion_img.replace(' ', '%20')
        install_path = ubicaciones.INSTALL_DIR.replace(' ', '%20')
        fout = open("config/secuencia.prm", "wt")
        fout.write("Application:Speller%20Targets matrix TargetDefinitions= 9 { Display Enter Display%20Size Icon%20File Sound Intensified%20Icon } ")
        # necesario para construir el archivo prm
        lista = ("A A 1 ", "B B 1 ", "C C 1 ", "D D 1 ", "E E 1 ", "F F 1 ", "G G 1 ", "H H 1 ", "I I 1 ")
          
        ## caso especial de matriz estática para memoria espacial
        if tipo_tarea == 'Bloque C2':
            orden_secuencia = list(range(1, 10))
            for i in range(0, 9):
                if i == 3:
                    matriz = lista[i] + install_path + "/img/punto.png % % "
                elif i == 5:
                    matriz = lista[i] + install_path + "/img/espacio.png % % "
                else:
                    matriz = lista[i] + install_path + "/img/img0.png % % "
                fout.write(matriz)
                sesion.orden_secuencia[i] = orden_secuencia[i]
        ##
        else:
            random.shuffle(orden_secuencia)
            for i in range(0, 9):
                if orden_secuencia[i] != 0:
                    if os.path.isfile(sesion.ubicacion_img + "/img" + str(orden_secuencia[i]) + ".png"):
                        orden_img = lista[i] + img_path + "/img" + str(orden_secuencia[i]) + ".png % % "
                    elif os.path.isfile(sesion.ubicacion_img + "/distractor - img" + str(orden_secuencia[i]) + ".png"):
                        orden_img = lista[i] + img_path + "/distractor%20-%20img" + str(orden_secuencia[i]) + ".png % % "
                    else:
                        orden_img = lista[i] + img_path + "/img" + str(orden_secuencia[i]) + "%20-%20punto.png % % "
                else:
                    orden_img = lista[i] + install_path + "/img" + "/img" + str(orden_secuencia[i]) + ".png % % "

                fout.write(orden_img)
                sesion.orden_secuencia[i] = orden_secuencia[i]

        fout.write("// speller target properties")
        fout.close()
        