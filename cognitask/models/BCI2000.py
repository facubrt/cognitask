### Cognitask ############################################################
##########################################################################
## Autor: Facundo Barreto ### facubrt@outlook.com ########################
##                                                                      ##
## Sistema para rehabilitación cognitiva basado en BCI por P300 ##########
##                                                                      ##
## Pagina del proyecto ### https://facubrt.github.io/cognitask ###########
##                                                                      ##
## Proyecto Final de Bioingeniería ### 2021 ##############################
##########################################################################
##########################################################################

from BCI2000.prog.BCI2000Remote import BCI2000Remote
import cognitask.common.constantes as constantes

class BCI2000(object):
    
    # INICIALIZACION
    # ///////////////////////////////////////////////////////////
    def __init__(self):
        '''------------
        DOCUMENTACIÓN -
        Inicializa BCI2000Remote.
        - Se comunica con BCI2000 a través de BCI2000Remote.
        - Inicia los módulos de BCI2000.
        ------------'''
        self.bci2000 = BCI2000Remote()
        self.bci2000.WindowVisible = False  # hace invisible el operador de BCI2000
        self.modulos = [constantes.ADQUISICION, constantes.PROCESAMIENTO, constantes.APLICACION]
        self.bci2000.Connect()
        # inicializa los modulos de BCI2000
        self.bci2000.StartupModules(self.modulos)
        self.estado = 'Suspended'

    # ESTADOS
    # ///////////////////////////////////////////////////////////
    @property #GETTER
    def obtener_seleccion(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el estimulo atendido.
        - SelectedTarget es el estado de BCI2000 que indica el código del estimulo (fila/columna) atendido
        ------------'''
        return self.bci2000.GetStateVariable('SelectedTarget')
    
    @property # GETTER
    def obtener_estado_sistema(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el estado del sistema BCI2000.
        - El estado del sistema puede ser Suspended, Running, etc...
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        return self.bci2000.GetSystemState()
    
    # PARAMETROS
    # ///////////////////////////////////////////////////////////
    def cargar_parametros(self, parametros):
        '''------------
        DOCUMENTACIÓN -
        Carga los parametros correspondientes al amplificador y las configuraciones de sesion de terapia o calibracion.
        - Carga en BCI2000 los archivos .prm indicados
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.LoadParametersRemote(parametros)

    def aplicar_configuracion(self):
        '''------------
        DOCUMENTACIÓN -
        Aplica los parametros cargados en el sistema.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.SetConfig()
    
    def cargar_datos(self, paciente, sesion, ubicacion_datos):
        '''------------
        DOCUMENTACIÓN -
        Carga los datos correspondientes al paciente, la sesion y la ubicacion.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.SubjectID = paciente
        self.bci2000.SessionID = sesion
        self.bci2000.DataDirectory = ubicacion_datos

    @property # GETTER
    def paciente(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve el nombre o identificacion del paciente.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        return self.bci2000.SubjectID

    @property # GETTER
    def matriz_clasificacion(self):
        '''------------
        DOCUMENTACIÓN -
        Devuelve la matriz de clasificacion utilizada.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        return self.bci2000.GetMatrixParameter("Classifier")

    # CONTROL DE BCI
    # ///////////////////////////////////////////////////////////
    def iniciar(self):
        '''------------
        DOCUMENTACIÓN -
        Inicia la estimulacion visual de la matriz.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.Start()

    def suspender(self):
        '''------------
        DOCUMENTACIÓN -
        Suspende la estimulacion visual de la matriz.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.Stop()

    def ejecutar(self, comando):
        '''------------
        DOCUMENTACIÓN -
        Ejecuta un comando determinado.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.Execute(comando)

    def terminar(self):
        '''------------
        DOCUMENTACIÓN -
        Cierra la conexion con BCI2000.
        - Para mas informacion ver BCI2000Remote.py ubicado en BCI2000/prog
        ------------'''
        self.bci2000.Quit()
