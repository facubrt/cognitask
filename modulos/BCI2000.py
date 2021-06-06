from utils.singleton import singleton
from BCI2000.prog.BCI2000Remote import BCI2000Remote
import modulos.constantes as constantes


@singleton
class BCI2000(object):
    def __init__(self):
        self.bci2000 = BCI2000Remote()
        self.bci2000.WindowVisible = False  # hace invisible el operador de BCI2000
        self.modulos = [constantes.ADQUISICION,
                        constantes.PROCESAMIENTO, constantes.APLICACION]
        self.bci2000.Connect()
        # inicializa los modulos de BCI2000
        self.bci2000.StartupModules(self.modulos)

    def cargarParametros(self, parametros):
        self.bci2000.LoadParametersRemote(parametros)

    def aplicarConfiguracion(self):
        self.bci2000.SetConfig()

    def iniciar(self):
        self.bci2000.Start()

    def suspender(self):
        self.bci2000.Stop()

    def ejecutar(self, comando):
        self.bci2000.Execute(comando)

    def paciente(self):
        return self.bci2000.SubjectID

    def matrizClasificacion(self, parametro):
        return self.bci2000.GetMatrixParameter(parametro)

    def obtenerEstado(self, estado):
        return self.bci2000.GetStateVariable(estado)

    def obtenerEstadoSistema(self):
        return self.bci2000.GetSystemState()

    def cargarDatos(self, paciente, sesion, ubicacion_datos):
        self.bci2000.SubjectID = paciente
        self.bci2000.SessionID = sesion
        self.bci2000.DataDirectory = ubicacion_datos

    def terminar(self):
        self.bci2000.Quit()
