# import os
# from PyQt5 import QtGui, QtCore
# import cognitask.common.ubicaciones as ubicaciones
# import cognitask.common.constantes as constantes

class Progreso():
    
    def evaluar_seleccion():
        pass

#     def __init__(self):
#         pass
    
#     def iniciar(self, calibracion):
    
#         if calibracion:
            
#             for i in range(0, constantes.PASOS_CALIBRACION):
#                 self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                 self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
        
#             self.__indicar_siguiente(self, 0)  
    
#         else:
            
#             if self.BCIOperador.guiaVisual == 'Mantener':
#                 for i in range(0, self.cantidad_pasos):
#                     self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                     self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                    
#             else:
#                 for i in range(0, self.cantidad_pasos):
#                     self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/target_v.png"))
#                     self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                     self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/target_h.png"))
#                     self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                        
#             self.__indicar_siguiente(self, 0)        
        
#     def actualizar(self, calibracion):
#         if calibracion is False:
#             if self.siguiente_seleccion < self.cantidad_pasos:
#                 self.__indicar_siguiente(self, self.siguiente_seleccion)
                
#             # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
#             if os.path.isfile(self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"):
#                 extension = ".png"
#             else:
#                 extension = " - punto.png"
#             img = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + extension
#             p = QtGui.QPixmap(img)
#             self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
#             self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
        
#         if calibracion is True:
#             if self.siguiente_seleccion < constantes.PASOS_CALIBRACION:
#                 self._indicar_siguiente(self, self.siguiente_seleccion)
#             img = "img/paso_completado.png"
#             p = QtGui.QPixmap(img)
#             self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
#             self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
    
#     def mostrar_guia(self, calibracion):
#         if calibracion is False:
#             for i in range(0, 9):
#                 if i < self.cantidad_pasos:
#                     # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
#                     if os.path.isfile(self.ubicacion_img + "/img" + str(i+1) + ".png"):
#                         extension = ".png"
#                     else:
#                         extension = " - punto.png"
                    
#                     img = self.ubicacion_img + "/img" + str(i+1) + extension
                    
#                     new_pix = QtGui.QPixmap(img)
#                     new_pix.fill(QtCore.Qt.transparent)
#                     painter = QtGui.QPainter(new_pix)
#                     painter.setOpacity(0.4)
#                     painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
#                     painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
#                     painter.end()
                    
#                     self.BCIAplicacion.progreso_lineal[i].setPixmap(new_pix)
#                     self.BCIAplicacion.progreso_grid[i].setPixmap(new_pix)
#                     self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                     self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                        
#                 else:
#                     self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
#                     self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  
                    
#         elif calibracion is True:
            
#             if self.calibracion_tarea == 1:
#                 ubicacion_img = ubicaciones.UBICACION_TAREA1
#             elif self.calibracion_tarea == 2:
#                 ubicacion_img = ubicaciones.UBICACION_TAREA2
#             elif self.calibracion_tarea == 3:
#                 ubicacion_img = ubicaciones.UBICACION_TAREA3
        
#             for i in range(0, 9):  
#                 if i < constantes.PASOS_CALIBRACION:
#                     extension = ".png"
#                     img = ubicacion_img + "/img" + str(i+1) + extension
                    
#                     new_pix = QtGui.QPixmap(img)
#                     new_pix.fill(QtCore.Qt.transparent)
#                     painter = QtGui.QPainter(new_pix)
#                     painter.setOpacity(0.4)
#                     painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
#                     painter.drawPixmap(QtCore.QPoint(), QtGui.QPixmap(img))
#                     painter.end()
                    
#                     self.BCIAplicacion.progreso_lineal[i].setPixmap(new_pix)
#                     self.BCIAplicacion.progreso_grid[i].setPixmap(new_pix)
#                     self.BCIAplicacion.progreso_lineal[i].setStyleSheet("")
#                     self.BCIAplicacion.progreso_grid[i].setStyleSheet("")
                        
#                 else:
#                     self.BCIAplicacion.progreso_lineal[i].setPixmap(QtGui.QPixmap("img/bloqueado_v.png"))
#                     self.BCIAplicacion.progreso_grid[i].setPixmap(QtGui.QPixmap("img/bloqueado_h.png"))  
        
            
#         self.__indicar_siguiente(self, 0) 
    
#     def siguiente_paso(self):
#         if self.siguiente_seleccion < self.cantidad_pasos:
#                 self.__indicar_siguiente(self, self.siguiente_seleccion)
        
#         # las imagenes utilizadas para memoria espacial llevan el sufijo - punto
#         if os.path.isfile(self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + ".png"):
#             extension = ".png"
#         else:
#             extension = " - punto.png"
                    
#         img = self.ubicacion_img + "/img" + str(self.siguiente_seleccion) + extension
#         p = QtGui.QPixmap(img)
#         self.BCIAplicacion.progreso_lineal[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
#         self.BCIAplicacion.progreso_grid[self.siguiente_seleccion - 1].setPixmap(QtGui.QPixmap(p))
    
#     def __indicar_siguiente(self, siguiente_seleccion):
#         if siguiente_seleccion != 0:
#             self.BCIAplicacion.progreso_lineal[siguiente_seleccion - 1].setStyleSheet("")
#             self.BCIAplicacion.progreso_grid[siguiente_seleccion - 1].setStyleSheet("")
                
#         self.BCIAplicacion.progreso_lineal[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
#         self.BCIAplicacion.progreso_grid[siguiente_seleccion].setStyleSheet("border: 3px solid #23B59C;")
    
    
#     def informar_seleccion(self, siguiente_seleccion, seleccion, calibracion):
#         seleccion_correcta = 0
#         seleccion_incorrecta = 0 
#         # CALIBRACION
#         if calibracion:    
#             if siguiente_seleccion < constantes.PASOS_CALIBRACION:
                
#                 # if self.calibracion_tarea == 1:
#                 #     msg_calibracion = "Elige la letra " + constantes.TAREA_UNO[self.siguiente_seleccion]
#                 # elif self.calibracion_tarea == 2:
#                 #     msg_calibracion = "Elige la letra " + constantes.TAREA_DOS[self.siguiente_seleccion]
#                 # elif self.calibracion_tarea == 3:
#                 #     msg_calibracion = "Elige la letra " + constantes.TAREA_TRES[self.siguiente_seleccion]
                
#                 # self.BCIAplicacion.mostrarMensajes(msg_calibracion, constantes.CSS_MSG_CALIBRACION, True)
#                 #progreso.actualizar(self, calibracion)
#                 siguiente_seleccion = siguiente_seleccion + 1
#                 #selecciones_realizadas += 1

#             elif self.siguiente_seleccion == constantes.PASOS_CALIBRACION:
#                 if self.imagen_seleccionada != self.siguiente_seleccion:
#                     self.selecciones_incorrectas += 1
#                 else:
#                     self.selecciones_correctas += 1
#                 self.selecciones_realizadas += 1
#                 #progreso.actualizar(self, calibracion)
#                 self.finalizarCalibracion()
        
#         # TERAPIA
#         else:
            
#             if self.BCIOperador.tipoTarea == 'Rompecabezas - mem. espacial':
#                 img_seleccionada = self.ubicacion_img + "/img" + str(self.imagen_seleccionada) + " - punto.png"
#                 img_siguiente = self.ubicacion_img + "/img" + str(self.siguiente_seleccion) + " - punto.png"
#                 # si la imagen seleccionada es un punto (TRUE) y si la imagen siguiente que debe seleccionarse es punto (TRUE)
#                 # si son TRUE y TRUE es correcto, si son FALSE y FALSE es correcto
#                 if os.path.isfile(img_seleccionada) == os.path.isfile(img_siguiente):
#                     seleccionCorrecta(self, calibracion)
#                 else:
#                     seleccionIncorrecta(self, calibracion)
                
#             elif self.BCIOperador.tipoTarea == 'Palabras - al revés':
#                 siguiente_seleccion = (self.cantidad_pasos + 1) - self.siguiente_seleccion
#                 # cuando acierta
#                 if self.imagen_seleccionada == siguiente_seleccion:
#                     seleccionCorrecta(self, calibracion) 
#                 # cuando no acierta
#                 elif self.imagen_seleccionada != siguiente_seleccion:
#                     seleccionIncorrecta(self, calibracion)
                
#             # otros tipos de tarea    
#             else:
#                 # cuando acierta
#                 if self.imagen_seleccionada == self.siguiente_seleccion:
#                     seleccionCorrecta(self, calibracion) 
#                 # cuando no acierta
#                 elif self.imagen_seleccionada != self.siguiente_seleccion:
#                     seleccionIncorrecta(self, calibracion)
    
#     def __seleccion_correcta(self):
#         pass
    
#     def __seleccion_incorrecta(self):
#         pas

