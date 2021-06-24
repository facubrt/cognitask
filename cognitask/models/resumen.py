import os
from PyQt5 import QtCore
from datetime import date

def decorador(escribir_resumen):
    pass

def escribirResumen(self, seccion, calibracion):
    QtCore.QCoreApplication.processEvents()
    path = self.ubicacion_datos + "/" + self.bci.paciente + "/resumen_sesiones.txt"
    file_exists = os.path.isfile(path)
    fout = open(path, "a")
    
    if not file_exists:
        header = "Resumen de todas las sesiones [" + self.bci.paciente + "]\n"
        fout.write(header)
    _escribirSeccion(self, seccion, calibracion, fout)
    fout.close()
    
def _escribirSeccion(self, seccion, calibracion, fout):    
    if seccion == "sesion":
        today = date.today()
        d = today.strftime("%d-%m-%y")
        if calibracion is True and self.sesion_iniciada is False:
            sesion = "\n--- Sesión del día " + d + " [CALIBRACIÓN] ---\n"
            sesion = "\n---------------------------------------------" + \
                sesion + "---------------------------------------------\n"
            fout.write(sesion)
            self.sesion_iniciada = True
        elif calibracion is False and self.sesion_iniciada is False:
            sesion = "\n--- Sesión del día " + d + " [TERAPIA] ---\n"
            sesion = "\n-----------------------------------------" + \
                sesion + "-----------------------------------------\n"
            fout.write(sesion)
            matriz_text = "\nMatriz de clasificación ---\n"
            fout.write(matriz_text)
            # me dice la matriz usada en la corrida
            matriz = self.bci.matrizClasificacion("Classifier")
            for c in range(len(matriz)):
                m = str(matriz[c][0]) + " " + str(matriz[c][1]) + " " + \
                    str(matriz[c][2]) + " " + str(matriz[c][3]) + "\n"
                fout.write(m)
            self.sesion_iniciada = True

    elif seccion == "corrida":
        r = "\n--------------- Corrida R" + str(self.run).zfill(2) + "\n"
        fout.write(r)
        if calibracion is True:
            sec = "\n[Tarea Nro. " + str(self.calibracion_tarea) + "]\n"
            fout.write(sec)
        else:
            modo = "\nModo ------- [" + \
                self.BCIOperador.tipoTarea + "]\n"
            fout.write(modo)
            if (self.BCIOperador.tipoTarea.startswith("Rompecabezas")):
                sec = "Imagen ----- [" + \
                    os.path.basename(self.ubicacion_img) + "]\n"
            elif (self.BCIOperador.tipoTarea.startswith("Sucesiones")):
                sec = "Actividad -- [" + \
                    os.path.basename(self.ubicacion_img) + "]\n"
            elif (self.BCIOperador.tipoTarea.startswith("Palabras")):
                sec = "Palabra ---- [" + \
                    os.path.basename(self.ubicacion_img) + "]\n"
            fout.write(sec)
            n = "Nivel ------ [" + self.BCIOperador.nivel + "]\n"
            fout.write(n)

    elif seccion == "resumen":
        act = "\nACTIVIDAD INTERRUMPIDA -"
        if self.actividad_completada is True:
            act = "\nACTIVIDAD COMPLETADA ---"
        fout.write(act)
        tiempo = "\nDuración ------[" + str(self.tiempo_sesion.minute).zfill(
            2) + ' min ' + str(self.tiempo_sesion.second).zfill(2) + ' s' + "]"
        fout.write(tiempo)
        selecciones = "\nSelecciones realizadas  [" + \
            str(self.selecciones_realizadas).zfill(2) + "]"
        fout.write(selecciones)
        correctas = "\nSelecciones correctas   [" + \
            str(self.selecciones_correctas).zfill(2) + "]"
        fout.write(correctas)
        incorrectas = "\nSelecciones incorrectas [" + \
            str(self.selecciones_incorrectas).zfill(2) + "]\n"
        fout.write(incorrectas)
        aciertos = "\nPorcentaje de aciertos [" + \
            str(self.porcentaje_aciertos) + "%]\n"
        fout.write(aciertos)
        observaciones = "\nObservaciones ----\n"
        fout.write(observaciones)