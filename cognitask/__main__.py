
import inspect
import os
import sys
from PyQt5 import QtWidgets, QtGui

import cognitask.common.constantes as constantes
import cognitask.common.ubicaciones as ubicaciones
from cognitask.views.splash import Splash

# FIX Problem for High DPI and Scale above 100%
os.environ["QT_FONT_DPI"] = "96" 

# MAIN
# ///////////////////////////////////////////////////////////
if __name__ == '__main__':
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
    
    splash = Splash()
    splash.show()

    sys.exit(app.exec_())