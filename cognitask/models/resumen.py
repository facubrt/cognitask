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
from datetime import date
from PyQt5 import QtCore

class Resumen():
    
    def escribir_resumen(sesion, bci, operador, seccion, calibracion):
        '''------------
        DOCUMENTACIÓN -
        Escribe el documento resumen_sesiones.txt en la carpeta del paciente.
        - Escribe la seccion indicada, la cual puede ser SESION, CORRIDA, RESUMEN
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        path = sesion.ubicacion_datos + "/" + bci.paciente + "/resumen_sesiones.txt"
        file_exists = os.path.isfile(path)
        fout = open(path, "a")
        if not file_exists:
            header = "RESUMEN DE TODAS LAS SESIONES [" + bci.paciente + "]\n"
            fout.write(header)
        if seccion == 'sesion':
            if calibracion:
                Resumen.escribir_sesion_calibracion(fout, sesion.estado)
            else:
                Resumen.escribir_sesion_terapia(fout, sesion.estado, bci.matriz_clasificacion)
        
        elif seccion == 'corrida':
            if calibracion:
                Resumen.escribir_corrida_calibracion(fout, sesion.corrida, sesion.indice_tarea)
            else:
                Resumen.escribir_corrida_terapia(fout, sesion.corrida, operador.tipo_tarea, operador.nivel, sesion.ubicacion_img)
        
        elif seccion == 'resumen':
            if calibracion:
                Resumen.escribir_resumen_calibracion(fout, sesion.tiempo_sesion, sesion.selecciones_realizadas, sesion.actividad_completada)
            else:    
                Resumen.escribir_resumen_terapia(fout, sesion.tiempo_sesion, sesion.selecciones_realizadas, sesion.selecciones_correctas, sesion.selecciones_incorrectas, sesion.porcentaje_aciertos, sesion.actividad_completada)
        fout.close()
            
    def escribir_sesion_terapia(fout, estado_sesion, matriz_clasificacion):
        '''------------
        DOCUMENTACIÓN -
        Escribe la seccion SESION en el documento resumen_sesiones.txt en la carpeta del paciente.
        - Indica el tipo de sesion (TERAPIA) y la fecha de la misma
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        today = date.today()
        d = today.strftime("%d-%m-%y")
        if estado_sesion == 'No iniciada':
            sesion = "\n--- Sesión del día " + d + " [TERAPIA] ---\n"
            sesion = "\n-----------------------------------------" + sesion + "-----------------------------------------\n"
            fout.write(sesion)
            matriz_text = "\nMatriz de clasificación ---\n"
            fout.write(matriz_text)
            # me dice la matriz usada en la corrida
            matriz = matriz_clasificacion
            for c in range(len(matriz)):
                m = str(matriz[c][0]) + " " + str(matriz[c][1]) + " " + str(matriz[c][2]) + " " + str(matriz[c][3]) + "\n"
                fout.write(m)
            
    def escribir_sesion_calibracion(fout, estado_sesion):
        '''------------
        DOCUMENTACIÓN -
        Escribe la seccion SESION en el documento resumen_sesiones.txt en la carpeta del paciente.
        - Indica el tipo de sesion (CALIBRACION) y la fecha de la misma
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        today = date.today()
        d = today.strftime("%d-%m-%y")
        if estado_sesion == 'No iniciada':
            sesion = "\n--- Sesión del día " + d + " [CALIBRACIÓN] ---\n"
            sesion = "\n---------------------------------------------" + sesion + "---------------------------------------------\n"
            fout.write(sesion)
            
    def escribir_corrida_terapia(fout, corrida, tipo_tarea, nivel, ubicacion_img):
        '''------------
        DOCUMENTACIÓN -
        Escribe la seccion CORRIDA para una sesion de terapia en el documento resumen_sesiones.txt en la carpeta del paciente.
        - Indica el numero de corrida
        - Indica el tipo de tarea utilizada
        - Indica el nivel
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        r = "\n--------------- Corrida R" + str(corrida).zfill(2) + "\n"
        fout.write(r)
        
        modo = "\nModo ------- [" + tipo_tarea + "]\n"
        fout.write(modo)
        if tipo_tarea.startswith("Rompecabezas"):
            sec = "Imagen ----- [" + os.path.basename(ubicacion_img) + "]\n"
        elif tipo_tarea.startswith("Sucesiones"):
            sec = "Actividad -- [" + os.path.basename(ubicacion_img) + "]\n"
        elif tipo_tarea.startswith("Palabras"):
            sec = "Palabra ---- [" + os.path.basename(ubicacion_img) + "]\n"
        fout.write(sec)
        n = "Nivel ------ [" + nivel + "]\n"
        fout.write(n)
        
    def escribir_corrida_calibracion(fout, corrida, indice_tarea):
        '''------------
        DOCUMENTACIÓN -
        Escribe la seccion CORRIDA para una sesion de calibracion en el documento resumen_sesiones.txt en la carpeta del paciente.
        - Indica el numero de corrida
        - Indica el numero de tarea realizada
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        r = "\n--------------- Corrida R" + str(corrida).zfill(2) + "\n"
        fout.write(r)
        
        sec = "\n[Tarea Nro. " + str(indice_tarea) + "]\n"
        fout.write(sec)
            
    def escribir_resumen_terapia(fout, tiempo_sesion, selecciones_realizadas, selecciones_correctas, selecciones_incorrectas, porcentaje_aciertos, actividad_completada):
        '''------------
        DOCUMENTACIÓN -
        Escribe la seccion RESUMEN para una sesion de terapia en el documento resumen_sesiones.txt en la carpeta del paciente.
        - Indica el estado de la tarea
        - Indica las selecciones realizadas, correctas e incorrectas
        - Indica la duracion de la tarea
        - Indica el porcentaje de aciertos
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        act = "\nACTIVIDAD INTERRUMPIDA -"
        if actividad_completada is True:
            act = "\nACTIVIDAD COMPLETADA ---"
        fout.write(act)
        tiempo = "\nDuración ------[" + str(tiempo_sesion.minute).zfill(2) + ' min ' + str(tiempo_sesion.second).zfill(2) + ' s' + "]"
        fout.write(tiempo)
        selecciones = "\nSelecciones realizadas  [" + str(selecciones_realizadas).zfill(2) + "]"
        fout.write(selecciones)
        correctas = "\nSelecciones correctas   [" + str(selecciones_correctas).zfill(2) + "]"
        fout.write(correctas)
        incorrectas = "\nSelecciones incorrectas [" + str(selecciones_incorrectas).zfill(2) + "]\n"
        fout.write(incorrectas)
        aciertos = "\nPorcentaje de aciertos [" + str(porcentaje_aciertos) + "%]\n"
        fout.write(aciertos)
        observaciones = "\nObservaciones ----\n"
        fout.write(observaciones)
        
    def escribir_resumen_calibracion(fout, tiempo_sesion, selecciones_realizadas, actividad_completada):
        '''------------
        DOCUMENTACIÓN -
        Escribe la seccion RESUMEN para una sesion de calibracion en el documento resumen_sesiones.txt en la carpeta del paciente.
        - Indica el estado de la tarea
        - Indica la duracion de la tarea
        - Indica las selecciones realizadas
        ------------'''
        # Refrezca la interfaz grafica evitando que se congele
        QtCore.QCoreApplication.processEvents()
        act = "\nACTIVIDAD INTERRUMPIDA -"
        if actividad_completada is True:
            act = "\nACTIVIDAD COMPLETADA ---"
        fout.write(act)
        tiempo = "\nDuración ------[" + str(tiempo_sesion.minute).zfill(2) + ' min ' + str(tiempo_sesion.second).zfill(2) + ' s' + "]"
        fout.write(tiempo)
        selecciones = "\nSelecciones realizadas  [" + str(selecciones_realizadas).zfill(2) + "]"
        fout.write(selecciones)
        observaciones = "\nObservaciones ----\n"
        fout.write(observaciones)