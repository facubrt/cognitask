# Proyecto Final de Bioingeniería
<strong> Facundo Barreto </strong>

<p align="center">
  <img src="https://i.imgur.com/LNxxl9s.png">
</p>

## Introducción
<p align="justify">
Cognitask forma parte del Proyecto Final de Bioingeniería titulado "Desarrollo de una BCI basada en P300 para rehabilitación cognitiva de adultos con déficit de atención" desarrollado en la Facultad de Ingeniería (UNER).
</p>

## Desarrolado con
- [x] BCI2000
- [x] Python 3.6.8

## Interfaz de usuario profesional
<p align="justify">
La interfaz de usuario profesional permite cargar los datos del paciente, configurar los parámetros de la sesión, y obtener información relevante de la misma en tiempo real (ver imagen). A través de esta interfaz, el profesional puede iniciar, detener, suspender, reanudar o reconfigurar el funcionamiento del sistema. Comúnmente la interfaz de usuario paciente se presenta sola en una pantalla para el paciente, mientras que la interfaz de usuario profesional se muestra en una segunda pantalla y es solamente visible para el profesional que lleva a cabo la terapia.
</p>

<p align="center">
  <img src="https://i.imgur.com/AFX2eVe.png">
</p>

## Interfaz de usuario paciente
<p align="justify">
La interfaz de usuario paciente presenta las tareas que éste debe realizar, el progreso durante el curso de una sesión, y la realimentación sobre su desempeño. En esta interfaz se pueden observar tres áreas: la matriz de estimulación, el progreso y la realimentación (ver imagen). El área de progreso proporciona información visual relacionada con la tarea que debe realizar, tanto antes como durante la realización de la misma. El área de realimentación proporciona al paciente mensajes sobre su desempeño y también sobre los estados de la tarea (por ejemplo, si la tarea es interrumpida o ha finalizado). El área de la matriz de estimulación visual presenta la tarea propiamente dicha, la cual consiste en un conjunto de imágenes ubicadas de manera aleatoria que el paciente debe ordenar correctamente. Existen tres tipos de tareas: Palabras, Sucesiones y Rompecabezas. Si bien todos contienen la misma consigna, cada uno permite realizar tareas diferentes, y pueden resultar más o menos complejas para el paciente.

Cuando la sesión comienza, la matriz comienza a iluminar cada una de sus filas o columnas de manera aleatoria (esto se conoce como paradigma <em>oddball</em>). Cuando el usuario se enfoca en una celda de la matriz en particular, cada vez que dicha celda es iluminada se genera un P300, el cual es identificado por el sistema, permitiendo así determinar cuál es la celda que el usuario está atendiendo.
</p>

<p align="center">
  <img src="https://i.imgur.com/fYV82KH.png">
</p>

## Diagrama de funcionamiento del sistema Cognitask
<p align="justify">
En este diagrama de funcionamiento se muestra de manera resumida cada uno de los pasos y procesos por los que atraviesa el usuario final (profesional y paciente) al utilizar el sistema Cognitask, las diferentes acciones posibles y las funciones más relevantes asociadas, como también los procesos externos que se realizan, las decisiones que el sistema toma a lo largo de una sesión y la comunicación entre la interfaz de usuario profesional y la interfaz de usuario paciente.
</p>
<p align="center">
  <img src="https://i.imgur.com/ZAHQFif.png">
</p>
