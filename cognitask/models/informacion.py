import os
from PyQt5 import QtCore
from datetime import date

# INFORMACION Y RESUMEN

def comoEmpezar(operador, seccion):
    if (seccion == "Nueva sesion"):
        operador.informacion_titulo.setText("¿Cómo empezar?")
        operador.informacion_stacked_widget.setCurrentIndex(0)
    elif (seccion == "Calibracion"):
        operador.informacion_titulo.setText("¿Cómo empezar?")
        operador.informacion_stacked_widget.setCurrentIndex(1)
    elif (seccion == "Terapia"):
        operador.informacion_titulo.setText("¿Cómo empezar?")
        operador.informacion_stacked_widget.setCurrentIndex(2)
        
def mostrarInformacion(operador, paciente):
    operador.informacion_titulo.setText(paciente)
    operador.informacion_stacked_widget.setCurrentIndex(3)

# se muestra el resumen de la sesion actual en la ventana de operador
def actualizar(self, operador, sesion_estado, calibracion):
    if sesion_estado == "Preparado":
        if calibracion is True:
            operador.modo_resumen_texto.setText("Calibración")
            operador.actividad_resumen_titulo.setText("Tarea")
            operador.actividad_resumen_texto.setText(os.path.basename(self.ubicacion_img))
            operador.nivel_resumen_texto.setText("-")
        else:
            operador.modo_resumen_texto.setText(operador.tipoTarea)
            if (operador.tipoTarea.startswith("Rompecabezas")):
                operador.actividad_resumen_titulo.setText("Imagen")
            elif (operador.tipoTarea.startswith("Sucesiones")):
                operador.actividad_resumen_titulo.setText("Actividad")
            elif (operador.tipoTarea.startswith("Palabras")):
                operador.actividad_resumen_titulo.setText("Palabra")
            operador.actividad_resumen_texto.setText(os.path.basename(self.ubicacion_img))
            operador.nivel_resumen_texto.setText(operador.nivel)
            operador.selecciones_resumen_texto.setText(str(self.selecciones_realizadas))
            operador.correctas_resumen_texto.setText(str(self.selecciones_correctas))
            operador.incorrectas_resumen_texto.setText(str(self.selecciones_incorrectas))
            operador.estado_resumen_texto.setText("Preparado")
    elif (sesion_estado == "Realizando"):
        operador.selecciones_resumen_texto.setText(str(self.selecciones_realizadas))
        operador.correctas_resumen_texto.setText(str(self.selecciones_correctas))
        operador.incorrectas_resumen_texto.setText(str(self.selecciones_incorrectas))
        operador.estado_resumen_texto.setText("Realizando")
    elif (sesion_estado == "Completado"):
        operador.estado_resumen_texto.setText("Completado")
    elif (sesion_estado == "Interrumpido"):
        operador.estado_resumen_texto.setText("Interrumpido")

