from BCI2000.prog.BCI2000Remote import BCI2000Remote
import cognitask.common.constantes as constantes
import cognitask.models.temporizador as temporizador
import cognitask.models.realimentacion as realimentacion
from PyQt5 import QtCore


class BCI2000(object):
    
    # INICIALIZACION
    # ///////////////////////////////////////////////////////////
    def __init__(self):
        self.bci2000 = BCI2000Remote()
        self.bci2000.WindowVisible = False  # hace invisible el operador de BCI2000
        self.modulos = [constantes.ADQUISICION, constantes.PROCESAMIENTO, constantes.APLICACION]
        self.bci2000.Connect()
        # inicializa los modulos de BCI2000
        self.bci2000.StartupModules(self.modulos)
        
        self.bci_estado = 'Suspended'

    # ESTADOS
    # ///////////////////////////////////////////////////////////
    def obtenerEstado(self, estado):
        return self.bci2000.GetStateVariable(estado)
    
    @property # GETTER
    def obtenerEstadoSistema(self):
        return self.bci2000.GetSystemState()
    
    # PARAMETROS
    # ///////////////////////////////////////////////////////////
    def cargarParametros(self, parametros):
        self.bci2000.LoadParametersRemote(parametros)

    def aplicarConfiguracion(self):
        self.bci2000.SetConfig()
    
    def cargarDatos(self, paciente, sesion, ubicacion_datos):
        self.bci2000.SubjectID = paciente
        self.bci2000.SessionID = sesion
        self.bci2000.DataDirectory = ubicacion_datos

    @property # GETTER
    def paciente(self):
        return self.bci2000.SubjectID

    def matrizClasificacion(self, parametro):
        return self.bci2000.GetMatrixParameter(parametro)

    # CONTROL DE BCI
    # ///////////////////////////////////////////////////////////
    def iniciar(self):
        self.bci2000.Start()

    def suspender(self):
        self.bci2000.Stop()

    def ejecutar(self, comando):
        self.bci2000.Execute(comando)

    def terminar(self):
        self.bci2000.Quit()
