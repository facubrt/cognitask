import modulos.temporizador as temporizador
from PyQt5 import QtCore
import modulos.mensajes as mensajes


def observar(self):
    while self.bci_estado == 'Running':
        # la actualización se realiza en este lugar para aprovechar el while de Observacion
        temporizador.actualizar(self)
        QtCore.QCoreApplication.processEvents()
        # me da el numero de target seleccionado (1 a 9)
        starget = self.bci.obtenerEstado('SelectedTarget')
        starget = int(starget)

        if starget != 0 and self.consultar_seleccion == True:
            # con esto puedo conocer que imagen se encuentra en este target (necesario debido al orden aleatorio de las imagenes)
            self.imagen_seleccionada = self.orden_secuencia[starget-1]
            self.target_seleccionado = starget
            mensajes.realimentacion(self)
            self.consultar_seleccion = False

        elif starget == 0 and self.consultar_seleccion == False:
            self.consultar_seleccion = True
        self.bci_estado = self.bci.obtenerEstadoSistema()
