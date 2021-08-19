var form = document.getElementById('form');
var opcion = document.getElementById('opcion');
var acuerdo = document.getElementById('acuerdo');
var descarga = document.getElementById('boton-descarga');
var error = document.getElementById('error')

form.addEventListener

form.onsubmit = function(e) {
    e.preventDefault();
    if (acuerdo.checked) {
        if (opcion.value ==='R210') {
            error.className = "pt-2 small text-danger invisible"
            location.href = "https://github.com/facubrt/cognitask/releases/download/R210/Instalar.Cognitask.R210.exe"
          }
          else if (opcion.value ==='R212') {
            error.className = "pt-2 small text-danger invisible"
            location.href = "https://github.com/facubrt/cognitask/releases/download/R210/Instalar.Cognitask.R210.exe"
          }
          else {
            error.innerHTML = "Selecciona una versión de Cognitask"
            error.className = "pt-2 small text-danger visible"
          }
    } 
    else {
        error.innerHTML = "Debe estar de acuerdo con la licencia"
        error.className = "pt-2 small text-danger visible"
    }  
}