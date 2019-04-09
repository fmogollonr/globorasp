#!/bin/sh
#La duración de un ciclo de hacer foto -> transmformación a sonido sstv, reproducción de sonido dura aproximadamente 62 segundos en una raspberry pi 3 B+
#intervalos en segundos
intervalo=1
intervalo2=120
indicativo="EA2CZO-11"
mision="ARANZADI"
#directorio donde se guardan las fotos
home="/home/pi/sstv/"
#contador de transmisiones
contador=0
#numero de transmisiones con el primer intervalo
ntrans=10
while true
do
#echo $contador
# tomamos la hora
fecha=$(date +"%Y-%m-%d_%H%M%S")
#hacemos una foto y la guardamos como fecha_hora.jpg
raspistill -o $home"/"$fecha.big.jpg
#redimensionamos la foto a 320x240
convert $home"/"$fecha.big.jpg -resize 320x240! $home"/"$fecha.jpg
#Insertamos el nombre de la misión arriba a la izquierda en rojo
convert -pointsize 20 -fill red -draw 'text 5,20 '$mision $home"/"$fecha.jpg $home"/"$fecha._.jpg
# insertamos el indicativo abajo a la derecha en rojo
convert -pointsize 20 -fill red -draw 'text 210,235 '$indicativo $home"/"$fecha._.jpg $home"/"$fecha.jpg

#convertimos la foto a a un wav que contiene el sstv
python3 -m pysstv --mode Robot36 --vox $home"/"$fecha.jpg $home"/"$fecha.wav
# reproducimos el wav
aplay $home"/"$fecha.wav
#borramos foto temporal
rm $home"/"$fecha._.jpg
#borramos el wav
rm $home"/"$fecha.wav
# comprobamos si llevamos menos transmisiones que laqs que queremos para el primer intervalo
if [ $contador -lt $ntrans ]
then
	#si llevamos menos, paramos lun tiempo que dura el primer intervalo
	sleep $intervalo
else
	# Si ya hemos hecho más transmisiones paramos el segundo intervalo
	sleep $intervalo2
fi
#actualizamos el contador de transmisiones
contador=`expr $contador + 1`
done
