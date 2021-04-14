import inspect
import os


class Config():

    def __init__(self):
        super.__init__()
        
        # obtener la ubicacion de instalacion de Cognitask
        pyfile = inspect.getfile(inspect.currentframe())
        self.install_dir = os.path.dirname(os.path.realpath(pyfile))

        self.config = self.install_dir + "/config/config.prm"
        self.config_calibracion = self.install_dir + "/config/calibracion.prm"
        self.config_source = self.install_dir + "/config/" + self.modulos[0] + ".prm"
        self.secuencia = self.install_dir + "/config/secuencia.prm"
        self.nivel = self.install_dir + "/config/nivel.prm"
        self.ubicacion_datos = self.install_dir + "\datos" # ubicacion de datos por defecto
        self.directorio_entrada.setPlaceholderText(self.ubicacion_datos)
        self.ubicacion_img = self.install_dir + "/sec/Rompecabezas/Musica" # por defecto
