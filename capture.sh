#!/bin/bash
#La duración de un ciclo de hacer foto -> transmformación a sonido sstv, reproducción de sonido dura aproximadamente 62 segundos en una raspberry pi 3 B+
#intervalos en segundos
intervalo=1
intervalo2=120
indicativo="EB2ELU-11"
mision="DEEP_SPACE"
#directorio donde se guardan las fotos
#home="/home/pi/balloon/"
home="/home/felipe/Documents/radio/soft/globorasp/"
gpsFile=$home"gps.log"

#contador de transmisiones
contador=0
#numero de transmisiones con el primer intervalo
ntrans=10
while true
do
	#echo $contador

	#extraer datos del fichero de logs del GPS
	tmpgps=`tail -n 1 $gpsFile`
	gpsmessage=`echo $tmpgps | sed 's/: /\n/g' | grep T`

	position="."
	altura="."
	#Si la salida del GPS es correcta se parsean los datos
	if [[ $gpsmessage != "0.0;0.0;;0.0" ]]
	then	
		IFS=';' read -ra ADDR <<< "$gpsmessage"
		latitude=${ADDR[0]}
		longitude=${ADDR[1]}
		utc_fecha=${ADDR[2]}
		altitude=${ADDR[3]}
		lat_len=$(echo -n $latitude | wc -m)
		lon_len=$(echo -n $longitude | wc -m)
		# Si latitud o longitud tienen un tamaño muy grande se recortan para que entren bien en la imágen
		lat=$latitude
		long=$longitude
		if [[ $lat_len -gt 10 ]]
		then
			lat=${latitude::-4}
		fi
		if [[ $lon_len -gt 10 ]]
		then
			long=${longitude::-4}
		fi
		position=$lat"/"$long
		altura="$altitude.m"
		# configuramos la hora de la raspberry desde el GPS
		date -s "$utc_fecha"
	fi

# tomamos la hora
fecha=$(date +"%Y-%m-%d_%H%M%S")
#hacemos una foto y la guardamos como fecha_hora.jpg
#raspistill -o $home"/"$fecha.big.jpg
#random jpg
mx=320;my=240;head -c "$((3*mx*my))" /dev/urandom | convert -depth 8 -size "${mx}x${my}" RGB:- $fecha.big.jpg
#redimensionamos la foto a 320x240
convert $home"/"$fecha.big.jpg -resize 320x240! $home"/"$fecha.jpg
#Insertamos el nombre de la misión arriba a la izquierda en rojo
convert -pointsize 20 -fill red  -gravity NorthWest -annotate 0 $mision $home"/"$fecha.jpg $home"/"$fecha.1.jpg
# insertamos el indicativo abajo a la derecha en rojo
convert -pointsize 20 -fill red -gravity SouthEast -annotate 0 $indicativo $home"/"$fecha.1.jpg $home"/"$fecha.2.jpg
#Insertamos la altitud abajo a la izquierda
convert -pointsize 20 -fill red -gravity SouthWest -annotate 0 $altura $home"/"$fecha.2.jpg $home"/"$fecha.3.jpg
#Insertamos la posición arriba a la derecha
convert -pointsize 20 -fill red -gravity NorthEast -annotate 0 $position $home"/"$fecha.3.jpg $home"/"$fecha.jpg

#convertimos la foto a a un wav que contiene el sstv
python3 -m pysstv --mode Robot36 --vox $home"/"$fecha.jpg $home"/"$fecha.sstv.wav
# reproducimos el wav
aplay $home"/"$fecha.sstv.wav
#borramos foto temporal
rm $home"/"$fecha.1.jpg
rm $home"/"$fecha.2.jpg
rm $home"/"$fecha.3.jpg
#borramos el wav
rm $home"/"$fecha.sstv.wav
# comprobamos si llevamos menos transmisiones que laqs que queremos para el primer intervalo

echo "DONE"
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
