# Utilidades para globos estratosféricos basadas en raspberry pi

Este proyecto contiene diferentes utilidades para realizar la transmisión en SSTV en modo robot36 de imágenes obtenidas con una raspberry pi 3


# Funcionalidades

* Transmisión en modo robot 36 de un indicativo y un nombre de misión
* Transmisión de la posición GPS y la altura del globo si se dispone de un GPS USB compatible con gpsd

# Instalación

* Crear un directorio */home/pi/balloon/* y copiar todos los ficheros en ese directorio.

* Ejecutar el script *install.sh*

$ sudo ./install.sh

* Reiniciar la raspberry

El sistema comenzará a hacer fotos y a transmitirlas por SSTV

# Requisitos

* Raspbian 11
* Raspberry pi 4 
* GPS USB
* Baofeng UV 3 con *VOX* habilitado (Funciona con cualquier equipo con VOX)
* Cámara Raspberry

# GPS
Editar */etc/default/gpsd* 
```
# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyACM0"

# Other options you want to pass to gpsd
GPSD_OPTIONS=""

# Automatically hot add/remove USB GPS devices via gpsdctl
USBAUTO="true"
```
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



