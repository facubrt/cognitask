from PyQt5 import QtGui ###############################

## PROGRESO

def iniciar(self):
    
    if self.modo_calibracion == False:
        self.BCIAplicacion.progreso_lineal[0].setPixmap(QtGui.QPixmap("img/starget_v.png"))
        self.BCIAplicacion.progreso_grid[0].setPixmap(QtGui.QPixmap("img/starget_h.png"))
        for i in range(1, 9):
            if i < self.cantidad_pasos:
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/target_v.png"))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/target_h.png"))
            else:
                self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
                self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))
    
    if self.modo_calibracion == True and self.calibracion_tarea == 1:
        for i in range(0, 9):
            img = "calibracion/tarea 1/dimg" + str(i+1) + ".png"
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))
    
    if self.modo_calibracion == True and self.calibracion_tarea == 2:
        for i in range(0, 9):
            img = "calibracion/tarea 2/dimg" + str(i+1) + ".png"
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(img))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(img))

    if self.modo_calibracion == True and self.calibracion_tarea == 3:
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

def actualizar(self):

    if self.modo_calibracion == False:
        if self.siguiente_seleccion < self.cantidad_pasos:
            self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_v.png"))
            self.BCIAplicacion.progreso_grid[self.siguiente_seleccion].setPixmap(QtGui.QPixmap("img/starget_h.png"))
        img = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"
        p = QtGui.QPixmap(img)
        self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
    
    if self.modo_calibracion == True:
        img = "img/paso_completado.png"
        p = QtGui.QPixmap(img)
        self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))

def mostrarGuia(self):
    # queda ver si se puede poner opacidad en las imagenes de guia. También debería hacerse para calibracion
    for i in range(0, 9):
        if i < self.cantidad_pasos:
            img = self.ubicacion_img + "/img" + str(i+1) + ".png"
            p = QtGui.QPixmap(img)
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap(p))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap(p))
        else:
            self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
            self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  

