import cognitask.common.constantes as constantes

INSTALL_DIR = "INSTALL_DIR"
CONFIG_BASE = "CONFIG_BASE"
CONFIG_CALIBRACION = "CONFIG_CALIBRACION"
CONFIG_AMPLIFICADOR = "CONFIG_AMPLIFICADOR"
CONFIG_SECUENCIA = "CONFIG_SECUENCIA"
CONFIG_NIVEL = "CONFIG_NIVEL"
UBICACION_DATOS = "UBICACION_DATOS"
UBICACION_IMG = "UBICACION_IMG"
UBICACION_CLASIFICADOR = "UBICACION_CLASIFICADOR"

def cargar(DIR):
    global INSTALL_DIR
    INSTALL_DIR = DIR
    global CONFIG_BASE
    CONFIG_BASE = DIR + "/config/config.prm"
    global CONFIG_CALIBRACION
    CONFIG_CALIBRACION = DIR + "/config/calibracion.prm"
    global CONFIG_AMPLIFICADOR
    CONFIG_AMPLIFICADOR = DIR + "/config/" + constantes.ADQUISICION + ".prm"
    global CONFIG_SECUENCIA
    CONFIG_SECUENCIA = DIR + "/config/secuencia.prm"
    global CONFIG_NIVEL
    CONFIG_NIVEL = DIR + "/config/nivel.prm"
    global UBICACION_DATOS
    UBICACION_DATOS = DIR + "\datos"  # ubicacion de datos por defecto
    global UBICACION_IMG
    UBICACION_IMG = DIR + "/terapia/Palabras/Universal"  # por defecto
    