from BCI2000.prog.BCI2000Remote import BCI2000Remote
import cognitask.common.constantes as constantes


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
    @property
    def obtener_seleccion(self):
        return self.bci2000.GetStateVariable('SelectedTarget')
    
    @property # GETTER
    def obtener_estado_sistema(self):
        return self.bci2000.GetSystemState()
    
    # PARAMETROS
    # ///////////////////////////////////////////////////////////
    def cargar_parametros(self, parametros):
        self.bci2000.LoadParametersRemote(parametros)

    def aplicar_configuracion(self):
        self.bci2000.SetConfig()
    
    def cargar_datos(self, paciente, sesion, ubicacion_datos):
        self.bci2000.SubjectID = paciente
        self.bci2000.SessionID = sesion
        self.bci2000.DataDirectory = ubicacion_datos

    @property # GETTER
    def paciente(self):
        return self.bci2000.SubjectID

    @property # GETTER
    def matriz_clasificacion(self):
        return self.bci2000.GetMatrixParameter("Classifier")

    # CONTROL DE BCI
    # ///////////////////////////////////////////////////////////
    def iniciar(self):
        self.bci2000.Start()

    def suspender(self):
        #self.ejecutar("Wait for Suspended 5")
        self.bci2000.Stop()

    def ejecutar(self, comando):
        self.bci2000.Execute(comando)

    def terminar(self):
        self.bci2000.Quit()
