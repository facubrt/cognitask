import cognitask.common.constantes as constantes
from PyQt5 import QtCore


# MENSAJES

def terminar(app):
    app.feedback_label.hide()
    app.feedback_label.setStyleSheet(constantes.CSS_MSG_CORRECTO) # restaura valores por defecto

# ocultar indica si se incluye un temporizador o no en el mensaje.
def mostrar(self, mensaje, estilo, ocultar):
    
    self.BCIAplicacion.feedback_label.setText(mensaje)
    self.BCIAplicacion.feedback_label.setStyleSheet(estilo)
    self.BCIAplicacion.feedback_label.show()
    if ocultar == True:
        QtCore.QTimer.singleShot(2000, lambda: terminar(self.BCIAplicacion))

def restablecer(self):
    terminar(self.BCIAplicacion)    