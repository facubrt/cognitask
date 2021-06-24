from PyQt5 import QtCore
import cognitask.models.temporizador as temporizador
import cognitask.models.realimentacion as realimentacion

def observar(self, calibracion):
    while self.bci.bci_estado == 'Running':
        # la actualización se realiza en este lugar para aprovechar el while de Observacion
        temporizador.actualizar(self, self.BCIOperador)
        QtCore.QCoreApplication.processEvents()
        # me da el numero de target seleccionado (1 a 9)
        starget = self.bci.obtenerEstado('SelectedTarget')
        starget = int(starget)

        if starget != 0 and self.consultar_seleccion == True:
            # con esto puedo conocer que imagen se encuentra en este target (necesario debido al orden aleatorio de las imagenes)
            self.imagen_seleccionada = self.orden_secuencia[starget-1]
            self.target_seleccionado = starget
            realimentacion.realimentar(self, calibracion)
            self.consultar_seleccion = False

        elif starget == 0 and self.consultar_seleccion == False:
            self.consultar_seleccion = True
        self.bci.bci_estado = self.bci.obtenerEstadoSistema
