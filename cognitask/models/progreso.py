from PyQt5 import QtGui, QtCore ###############################
import os

## PROGRESO
def _indicarSiguiente(self, siguiente_seleccion):

    if siguiente_seleccion != 0:
        self.BCIAplicacion.progreso_lineal[siguiente_seleccion - 1].setStyleSheet("")
        self.BCIAplicacion.progreso_grid[siguiente_seleccion - 1].setStyleSheet("")
            
    self.BCIAplicacion.progreso_lineal[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
    self.BCIAplicacion.progreso_grid[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")

def iniciar(self, modo, calibracion):
    
    if calibracion is False:

        if modo == 'Mantener':
            for i in range(0, 9):
                if i < self.cantidad_pasos:
                    self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
                    self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                else:
                    self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                    self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))
                
        else:
            for i in range(0, 9):
                if i < self.cantidad_pasos:
                    self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/target_v.png"))
                    self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
                    self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/target_h.png"))
                    self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                else:
                    self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                    self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))
                    
        _indicarSiguiente(self, 0)        
                    
        
    if calibracion is True and self.calibracion_tarea == 1:
        for i in range(0, 9):
            img = "calibracion/tarea 1/dimg" + str(i+1) + ".png"
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))
    
    if calibracion is True and self.calibracion_tarea == 2:
        for i in range(0, 9):
            img = "calibracion/tarea 2/dimg" + str(i+1) + ".png"
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))

    if calibracion is True and self.calibracion_tarea == 3:
        for i in range(0, 9):
            img = "calibracion/tarea 3/dimg" + str(i+1) + ".png"
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))

def siguientePaso(self):
    if self.siguiente_seleccion < self.cantidad_pasos:
        self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_v.png"))
        self.BCIAplicacion.progreso_grid[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_h.png"))
    img = self.ubicacion_img + "/img" + str(self.siguiente_seleccion) + ".png"
    p = QtGui.QPixmap(img)
    self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
    self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

def actualizar(self, calibracion):
  
    if calibracion is False:
        if self.siguiente_seleccion < self.cantidad_pasos:
            _indicarSiguiente(self, self.siguiente_seleccion)
            #self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_v.png"))
            #self.BCIAplicacion.progreso_grid[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_h.png"))
        
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
        img = "img/paso_completado.png"
        p = QtGui.QPixmap(img)
        self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

def mostrarGuia(self):
    
    for i in range(0, 9):
        if i < self.cantidad_pasos:
            # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
            if os.path.isfile(self.ubicacion_img + "/img" + str(i+1) + ".png"):
                extension = ".png"
            else:
                extension = " - punto.png"
            
            img = self.ubicacion_img + "/img" + str(i+1) + extension
            
            new_pix = QtGui.QPixmap(img)
            new_pix.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(new_pix)
            painter.setOpacity(0.4)
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