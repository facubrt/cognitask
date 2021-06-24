from datetime import datetime

# Temporizador para conocer la duracion de cada sesion
def iniciar(self):
    self.tiempo_inicial = datetime.now()

def actualizar(self, operador):
    diferencia = datetime.now() - self.tiempo_inicial
    tiempo_referencia = datetime(self.tiempo_inicial.year, self.tiempo_inicial.month, self.tiempo_inicial.day, 0, 0, 0)
    self.tiempo_sesion = tiempo_referencia + diferencia
    operador.tiempo_resumen_texto.setText(str(self.tiempo_sesion.minute).zfill(2) + ' min ' + str(self.tiempo_sesion.second).zfill(2) + ' s')