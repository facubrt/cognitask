import os ################################################################
from PyQt5 import QtCore ###############################
from datetime import date ######################################

## INFORMACION Y RESUMEN

def mostrar(self, informacion):
    if (informacion == "Nueva sesion"):
        self.informacion_titulo.setText("¿Cómo empezar?")
        self.informacion_stacked_widget.setCurrentIndex(0)
    elif (informacion == "Calibracion"):
        self.informacion_titulo.setText("¿Cómo empezar?")
        self.informacion_stacked_widget.setCurrentIndex(1)
    elif (informacion == "Terapia"):
        self.informacion_titulo.setText("¿Cómo empezar?")
        self.informacion_stacked_widget.setCurrentIndex(2)
    elif (informacion == "Resumen"):
        self.informacion_titulo.setText(self.bci.paciente())
        self.informacion_stacked_widget.setCurrentIndex(3)

# se muestra el resumen de la sesion actual en la ventana de operador
def actualizar(self):
    if (self.sesion_estado == "Preparado"):
        if (self.modo_calibracion == True):
            self.modo_resumen_texto.setText("Calibración")
            self.actividad_resumen_titulo.setText("Tarea")
            self.actividad_resumen_texto.setText(os.path.basename(self.ubicacion_img))
            self.nivel_resumen_texto.setText("-")
        else:
            self.modo_resumen_texto.setText(self.modo_terapia_opciones.currentText())
            if (self.modo_terapia_opciones.currentText() == "Rompecabezas"):
                self.actividad_resumen_titulo.setText("Imagen")
            elif (self.modo_terapia_opciones.currentText() == "Actividades"):
                self.actividad_resumen_titulo.setText("Actividad")
            elif (self.modo_terapia_opciones.currentText() == "Palabras"):
                self.actividad_resumen_titulo.setText("Palabra")
            self.actividad_resumen_texto.setText(os.path.basename(self.ubicacion_img))
            self.nivel_resumen_texto.setText(self.nivel_opciones.currentText())
            self.selecciones_resumen_texto.setText(str(self.selecciones_realizadas))
            self.correctas_resumen_texto.setText(str(self.selecciones_correctas))
            self.incorrectas_resumen_texto.setText(str(self.selecciones_incorrectas))
            self.estado_resumen_texto.setText("Preparado")
    elif (self.sesion_estado == "Realizando"):
        self.selecciones_resumen_texto.setText(str(self.selecciones_realizadas))
        self.correctas_resumen_texto.setText(str(self.selecciones_correctas))
        self.incorrectas_resumen_texto.setText(str(self.selecciones_incorrectas))
        self.estado_resumen_texto.setText("Realizando")
    elif (self.sesion_estado == "Completado"):
        self.estado_resumen_texto.setText("Completado")
    elif (self.sesion_estado == "Interrumpido"):
        self.estado_resumen_texto.setText("Interrumpido")

# Se escribe el documento con el resumen de todas las sesiones
def escribir(self, seccion):
    QtCore.QCoreApplication.processEvents()
    path = self.ubicacion_datos + "/" + self.bci.paciente() + "/resumen_sesiones.txt" 
    file_exists = os.path.isfile(path)
    fout = open(path, "a") 
    if not file_exists:  
        header = "Resumen de todas las sesiones [" + self.bci.paciente + "]\n"
        fout.write(header)
    
    if seccion == "sesion":
        today = date.today()
        d = today.strftime("%d-%m-%y")
        if self.modo_calibracion == True and self.sesion_iniciada == False:
            sesion = "\n--- Sesión del día " + d + " [CALIBRACIÓN] ---\n"
            sesion = "\n---------------------------------------------" + sesion + "---------------------------------------------\n"
            fout.write(sesion)
            self.sesion_iniciada = True
        elif self.modo_calibracion == False and self.sesion_iniciada == False:
            sesion = "\n--- Sesión del día " + d + " [TERAPIA] ---\n"
            sesion = "\n-----------------------------------------" + sesion + "-----------------------------------------\n"
            fout.write(sesion)
            matriz_text = "\nMatriz de clasificación ---\n"
            fout.write(matriz_text)
            matriz = self.bci.matrizClasificacion("Classifier") # me dice la matriz usada en la corrida
            for c in range(len(matriz)):
                m = str(matriz[c][0]) + " " + str(matriz[c][1]) + " " + str(matriz[c][2]) + " " + str(matriz[c][3]) + "\n"
                fout.write(m)
            self.sesion_iniciada = True 
    
    elif seccion == "corrida":
        r = "\n--------------- Corrida R" + str(self.run).zfill(2) + "\n"
        fout.write(r)
        if self.modo_calibracion == True:
            sec = "\n[Tarea Nro. " + str(self.calibracion_tarea) + "]\n"
            fout.write(sec)
        else:
            modo = "\nModo ------- [" + self.modo_terapia_opciones.currentText() + "]\n"
            fout.write(modo)
            if (self.modo_terapia_opciones.currentText() == "Rompecabezas"):
                sec = "Imagen ----- [" + os.path.basename(self.ubicacion_img) + "]\n"
            elif (self.modo_terapia_opciones.currentText() == "Actividades"):
                sec = "Actividad -- [" + os.path.basename(self.ubicacion_img) + "]\n"
            elif (self.modo_terapia_opciones.currentText() == "Palabras"):
                sec = "Palabra ---- [" + os.path.basename(self.ubicacion_img) + "]\n"
            fout.write(sec)
            n = "Nivel ------ [" + self.nivel_opciones.currentText() + "]\n"
            fout.write(n)

    elif seccion == "resumen":
        act = "\nACTIVIDAD INTERRUMPIDA -"
        if self.actividad_completada == True:
            act = "\nACTIVIDAD COMPLETADA ---" 
        fout.write(act)
        tiempo = "\nDuración ------[" + str(self.tiempo_sesion.minute).zfill(2) + ' min ' + str(self.tiempo_sesion.second).zfill(2) + ' s' + "]"
        fout.write(tiempo)
        selecciones = "\nSelecciones realizadas  [" + str(self.selecciones_realizadas).zfill(2) + "]"
        fout.write(selecciones)
        correctas = "\nSelecciones correctas   [" + str(self.selecciones_correctas).zfill(2) + "]"
        fout.write(correctas)
        incorrectas = "\nSelecciones incorrectas [" + str(self.selecciones_incorrectas).zfill(2) + "]\n"
        fout.write(incorrectas)
        aciertos = "\nPorcentaje de aciertos [" + str(self.porcentaje_aciertos) + "%]\n"
        fout.write(aciertos)
        observaciones = "\nObservaciones ----\n"
        fout.write(observaciones)
    
    fout.close()