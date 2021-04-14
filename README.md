# Proyecto Final de Bioingeniería
<strong> desarrollado por Facundo Barreto </strong>

<p align="center">
  <img src="https://i.imgur.com/LNxxl9s.png">
</p>

<<<<<<< HEAD
### Prerequisitos
<ul>
  <li>BCI2000</li>
  <li>Python 3.6.8</li>
  <li>PyQt5</li>
</ul>

### Introducción
=======
## Introducción
>>>>>>> 425ca286722a0eeb84c336ef151a45f10b8f82d9
<p align="justify">
BCI basada en P300 para rehabilitación cognitiva de la atención por neurofeedback.
</p>

## Prerequisitos
- [x] BCI2000
- [x] Python 3.6.8
- [x] PyQt5

## Operador
<p align="justify">
Este módulo es visible para el operador. Permite configurar las sesiones, realizar calibraciones y observar la información del usuario en tiempo real mientras realiza una sesión de terapia o calibración.
</p>

<p align="center">
  <img src="https://i.imgur.com/lpwty13.png">
</p>

## Aplicación
<p align="justify">
Este módulo es visible para el usuario o paciente. Se trata de una matriz Donchin modificada para lograr la rehabilitación cognitiva de la atención mediante un sistema de recompensas gamificado. Cuando la sesión comienza, la matriz es cargada con imágenes correspondientes a una secuencia, y comienza a iluminar cada una de sus filas o columnas de manera aleatoria (esto se conoce como paradigma <em>oddball</em>. Cuando el usuario se enfoca en una celda de la matriz en particular, cada vez que dicha celda es iluminada se genera un P300, el cual es identificado por el sistema BCI, permitiendo así determinar cuál es la celda que el usuario está atendiendo.
</p>

<p align="center">
  <img src="https://i.imgur.com/JhVBTQ2.png">
</p>
