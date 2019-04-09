# Utilidades para globos estratosféricos basadas en raspberry pi

Este proyecto contiene diferentes utilidades para realizar la transmisión en SSTV de imágenes obtenidas con una raspberry pi 3

# Instalación

* Crear un directorio */home/pi/sstv* y copiar todos los ficheros en ese directorio.

* Ejecutar el script *install.sh*

$ sudo ./install.sh

* Reiniciar la raspberry

El sistema comenzará a hacer fotos y a transmitirlas por SSTV

# Hardware

* Raspberry pi 3 B+
* Baofeng UV 3 con *VOX* habilitado

# Funcionamiento


* Captura de imágen con la cámara de la raspberry
* Reducción de la imágen a 360x240
* Se añade el indicativo y la misión a la imágen modificada
* Se transforma la imágen en un wav codificado para su transmisión en SSTV Robot 36
* Se reproduce el wav
* Durante las primeras *ntrans* transmisiones el sistema esperará el intervalo *intervalo* para volver a capturar una imágen, modificarla, codificarla en SSTV y reproducirla
* Transcurridas *ntrans* transmisiones el sistema esperará *intervalo2* para volver a capturar una imágen, modificarla, codificarla en SSTV y reproducirla

# Configuración

La configuración de la captura y transmisión de imágenes SSTV se realiza modificando el archivo *capture.sh*

* indicativo : Indicativo de radioaficionado que tendrá el globo (se muestra abajo a la derecha de las imágenes capturadas)
* mision: Nombre de la misión del globo (se muestra arriba a la izquierda de las imágenes capturadas)
* intervalo: Tiempo que el sistema espera entre una transmisión y la siguiente captura de imágen
* intervalo2: Tiempo que el sistema espera entre una transmisión y la siguiente captura de imágen
* ntrans: Número de transmisiones durante las cuales el sistema esperará el primer intervalo



