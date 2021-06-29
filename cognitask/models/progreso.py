from PyQt5 import QtGui, QtCore ###############################
import os
import cognitask.common.ubicaciones as ubicaciones
import cognitask.common.constantes as constantes

## PROGRESO
def _indicarSiguiente(self, siguiente_seleccion):

    if siguiente_seleccion != 0:
        self.BCIAplicacion.progreso_lineal[siguiente_seleccion - 1].setStyleSheet("")
        self.BCIAplicacion.progreso_grid[siguiente_seleccion - 1].setStyleSheet("")
            
    self.BCIAplicacion.progreso_lineal[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
    self.BCIAplicacion.progreso_grid[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")

# def iniciar(self, calibracion):
    
#     if calibracion is False:
        
#         if self.BCIOperador.guiaVisual == 'Mantener':
#             for i in range(0, self.cantidad_pasos):
#                 self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                 self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                
#         else:
#             for i in range(0, self.cantidad_pasos):
#                 self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/target_v.png"))
#                 self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                 self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/target_h.png"))
#                 self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                    
#         _indicarSiguiente(self, 0)        
                    
        
#     if calibracion is True:
        
#         for i in range(0, constantes.PASOS_CALIBRACION):
#             self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#             self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
    
#         _indicarSiguiente(self, 0)  

def siguientePaso(self):
    
    if self.siguiente_seleccion < self.cantidad_pasos:
            _indicarSiguiente(self, self.siguiente_seleccion)
    
    # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
    if os.path.isfile(self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"):
        extension = ".png"
    else:
        extension = " - punto.png"
                  
    img = self.ubicacion_img + "/img" + str(self.siguiente_seleccion) + extension
    p = QtGui.QPixmap(img)
    self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
    self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

def actualizar(self, calibracion):
  
    if calibracion is False:
        if self.siguiente_seleccion < self.cantidad_pasos:
            _indicarSiguiente(self, self.siguiente_seleccion)
            
        # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
        if os.path.isfile(self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"):
            extension = ".png"
        else:
            extension = " - punto.png"
        img = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + extension
        p = QtGui.QPixmap(img)
        self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
    
    if calibracion is True:
        if self.siguiente_seleccion < constantes.PASOS_CALIBRACION:
            _indicarSiguiente(self, self.siguiente_seleccion)
        img = "img/paso_completado.png"
        p = QtGui.QPixmap(img)
        self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

def mostrarGuia(self, calibracion):
    
    if calibracion is False:
        for i in range(0, 9):
            self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
            self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
            if i < self.sesion.cantidad_pasos:
                # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
                if os.path.isfile(self.sesion.ubicacion_img + "/img" + str(i+1) + ".png"):
                    extension = ".png"
                else:
                    extension = " - punto.png"
                
                img = self.sesion.ubicacion_img + "/img" + str(i+1) + extension
                
                new_pix = QtGui.QPixmap(img)
                new_pix.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(new_pix)
                painter.setOpacity(0.2)
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.end()
                
                self.BCIAplicacion.progreso_lineal[i].setPixmap(new_pix)
                self.BCIAplicacion.progreso_grid[i].setPixmap(new_pix)
                self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
                self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                    
            else:
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  
                
    elif calibracion is True:
        
        if self.sesion.indice_tarea == 1:
            ubicacion_img = ubicaciones.UBICACION_TAREA1
        elif self.sesion.indice_tarea == 2:
            ubicacion_img = ubicaciones.UBICACION_TAREA2
        elif self.sesion.indice_tarea == 3:
            ubicacion_img = ubicaciones.UBICACION_TAREA3
    
        for i in range(0, 9):  
            if i < constantes.PASOS_CALIBRACION:
                extension = ".png"
                img = ubicacion_img + "/img" + str(i+1) + extension
                
                new_pix = QtGui.QPixmap(img)
                new_pix.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(new_pix)
                painter.setOpacity(0.2)
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
                painter.end()
                
                self.BCIAplicacion.progreso_lineal[i].setPixmap(new_pix)
                self.BCIAplicacion.progreso_grid[i].setPixmap(new_pix)
                self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
                self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                    
            else:
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  
    
        
    _indicarSiguiente(self, 0) 