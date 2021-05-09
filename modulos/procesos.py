import win32process ######################################################
import win32gui ##########################################################
import re ################################################################

# oculta los procesos de BCI2000 que se ejecutan de fondo
def ocultarProcesos(self):
    for i in range (0, 3):
        title = re.sub(r"(\w)([A-Z])", r"\1 \2", self.bci.modulos[i])
        hwnd = win32gui.FindWindow(None, title)
        pid = win32process.GetWindowThreadProcessId(hwnd)
        pid = str(pid[1])
        comando = "HIDE PROCESS " + pid 
        self.bci.ejecutar(comando)

# mantiene el P3 Speller embebido en la ventana de Aplicacion 
def incorporarMatriz(self):
    parent = self.BCIAplicacion.p3_frame.winId()
    child = win32gui.FindWindow(None, "P3 Speller")
    win32gui.SetParent(child, parent)
    win32gui.SetWindowPos(child, 0, 0, 0, 600, 600, 0)