ADQUISICION = "Adquisicion"
PROCESAMIENTO = "Procesamiento"
APLICACION = "Aplicacion"

NIVEL_INICIAL = 0
NIVEL_INTERMEDIO = 0
NIVEL_AVANZADO = 0
INTENTOS_MAXIMOS = 0

NIVEL_CALIBRACION = 0
PASOS_CALIBRACION = 0

TAREA_UNO = "TAREA"
LISTA_UNO = ["A A 1 ", " B B 1 ",  " C C 1 ", " D D 1 ", " E E 1 ", " F F 1 ", " G G 1 ", " H H 1 ", " I I 1 "]
ORDEN_UNO = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

TAREA_DOS = "TAREA"
LISTA_DOS = ["A A 1 ", " B B 1 ",  " C C 1 ", " D D 1 ", " E E 1 ", " F F 1 ", " G G 1 ", " H H 1 ", " I I 1 "]
ORDEN_DOS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

TAREA_TRES = "TAREA"
LISTA_TRES = ["A A 1 ", " B B 1 ",  " C C 1 ", " D D 1 ", " E E 1 ", " F F 1 ", " G G 1 ", " H H 1 ", " I I 1 "]
ORDEN_TRES = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

MSG_CORRECTO = "CORRECTO"
MSG_INCORRECTO = "INCORRECTO"
MSG_PASAR = "PASA A LA SIGUIENTE"
MSG_TERMINADO = "TERMINADO"
MSG_COMENZAR = "COMENCEMOS"
MSG_SUSPENDIDO = "ESPERA"

MSG_REALIZANDO_TAREA = "Realizando..."
MSG_TAREA_SUSPENDIDA = "Esperando..."
MSG_TAREA_FINALIZADA = "Completado"

CSS_MSG_CALIBRACION = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(35, 181, 156);"
CSS_MSG_CORRECTO = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(35, 181, 156);"
CSS_MSG_INCORRECTO = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(234, 86, 61)"
CSS_MSG_PASAR = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(234, 202, 110)"
CSS_MSG_COMENZAR = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(35, 181, 156);"
CSS_MSG_TERMINADO = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(35, 181, 156);"
CSS_MSG_SUSPENDIDO = "color: rgb(242, 242, 242);border-color: rgb(0, 0, 0); border-radius: 6px; background-color: rgb(35, 181, 156);"

COMENZAR_BOTON_CSS = "QPushButton{color: rgb(242, 242, 242);border-radius:4px; background-color: rgb(35, 181, 156);border-style: solid;border-width:1px;border-color:  rgb(38, 43, 50);} QPushButton:hover{background-color: rgb(47, 193, 165);color: rgb(242, 242, 242);border-radius:4px;} QPushButton:disabled{color:rgb(116,123,141); border-radius:4px;border-style: solid;border-width:1px; border-color:  rgb(116, 123, 141); background-color: rgb(244, 244, 248);}"

SUSPENDER_BOTON_CSS = "QPushButton{color: rgb(242, 242, 242);border-radius:4px; background-color: rgb(234, 86, 61);border-style: solid;border-width:1px;border-color:  rgb(38, 43, 50);} QPushButton:hover{background-color: rgb(242, 95, 70);color: rgb(242, 242, 242);border-radius:4px;} QPushButton:disabled{color:rgb(116,123,141); border-radius:4px;border-style: solid;border-width:1px; border-color:  rgb(116, 123, 141); background-color: rgb(244, 244, 248);}"

# Carga los valores puestos en el archivo constantes.txt 
def cargar():
    with open('config/constantes.txt', 'r') as f:
        lineas = [linea.strip() for linea in f.readlines()]
        global ADQUISICION
        ADQUISICION = lineas[1].split(' = ')[1]
        global PROCESAMIENTO
        PROCESAMIENTO = lineas[2].split(' = ')[1]
        global APLICACION
        APLICACION = lineas[3].split(' = ')[1]
        global NIVEL_INICIAL
        NIVEL_INICIAL = int(lineas[6].split(' = ')[1])
        global NIVEL_INTERMEDIO
        NIVEL_INTERMEDIO = int(lineas[7].split(' = ')[1])
        global NIVEL_AVANZADO
        NIVEL_AVANZADO = int(lineas[8].split(' = ')[1])
        global INTENTOS_MAXIMOS
        INTENTOS_MAXIMOS = int(lineas[9].split(' = ')[1])
        global NIVEL_CALIBRACION
        NIVEL_CALIBRACION = int(lineas[12].split(' = ')[1])
        global PASOS_CALIBRACION
        PASOS_CALIBRACION = int(lineas[13].split(' = ')[1])
        global TAREA_UNO
        TAREA_UNO = lineas[15].split(' = ')[1]
        global LISTA_UNO
        LISTA_UNO =  lineas[16].split(' = ')[1].split('-')
        global ORDEN_UNO
        ORDEN_UNO =  lineas[17].split(' = ')[1].split('-')
        global TAREA_DOS
        TAREA_DOS = lineas[19].split(' = ')[1]
        global LISTA_DOS
        LISTA_DOS =  lineas[20].split(' = ')[1].split('-')
        global ORDEN_DOS
        ORDEN_DOS =  lineas[21].split(' = ')[1].split('-')
        global TAREA_TRES
        TAREA_TRES = lineas[23].split(' = ')[1]
        global LISTA_TRES
        LISTA_TRES =  lineas[24].split(' = ')[1].split('-')
        global ORDEN_TRES
        ORDEN_TRES =  lineas[25].split(' = ')[1].split('-')
        global MSG_CORRECTO
        MSG_CORRECTO = lineas[28].split(' = ')[1]
        global MSG_INCORRECTO
        MSG_INCORRECTO = lineas[29].split(' = ')[1]
        global MSG_PASAR
        MSG_PASAR = lineas[30].split(' = ')[1]
        global MSG_TERMINADO
        MSG_TERMINADO = lineas[31].split(' = ')[1]
        global MSG_COMENZAR
        MSG_COMENZAR = lineas[32].split(' = ')[1]
        global MSG_SUSPENDIDO
        MSG_SUSPENDIDO = lineas[33].split(' = ')[1]