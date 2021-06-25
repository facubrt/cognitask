import inspect
import os
import sys
from PyQt5 import QtWidgets, QtGui

import cognitask.common.constantes as constantes
import cognitask.common.ubicaciones as ubicaciones
import cognitask.common.procesos as procesos

from cognitask.views.aplicacion import BCIAplicacion
from cognitask.views.operador import BCIOperador

from cognitask.models.BCI2000 import BCI2000
from cognitask.models.sesion import Sesion

from cognitask.controller.cognitask import Cognitask


# FIX Problem for High DPI and Scale above 100%
os.environ["QT_FONT_DPI"] = "96" 

# MAIN
# ///////////////////////////////////////////////////////////

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('img/icon_cognitask.ico'))
    
    # agrego las fuentes de texto Gilroy utilizadas
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Light.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Gilroy-Bold.ttf')
    
    # carga constantes de archivo constantes.txt
    constantes.cargar()
    
    # obtengo la direccion en la que se encuentra instalado cognitask
    PYFILE = inspect.getfile(inspect.currentframe())
    DIR_MAIN = os.path.dirname(os.path.realpath(PYFILE))
    DIR_CTASK = os.path.dirname(DIR_MAIN)
    # cargo las rutas de los archivos de parametros y configuraciones por defecto
    ubicaciones.cargar(DIR_CTASK)

    splash_dir = DIR_CTASK + '\img\splash.png'
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(splash_dir))
    splash.show()
    
    bci = BCI2000()
    operator = BCIOperador()
    aplicacion = BCIAplicacion()
    sesion = Sesion()
    
    # PROCESOS
    # introduce P3Speller dentro del modulo de Aplicacion Cognitask
    procesos.incorporarMatriz(aplicacion.p3_frame.winId())
    # hace invisible los procesos de BCI2000
    procesos.ocultarProcesos(bci)
    
    ctask = Cognitask(bci, sesion, operator, aplicacion)
    splash.close()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()