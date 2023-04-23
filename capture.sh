#!/bin/bash
#La duración de un ciclo de hacer foto -> transnformación a sonido sstv, reproducción de sonido dura aproximadamente 62 segundos en una raspberry pi 3 B+
#intervalos en segundos
intervalo=1
intervalo2=120
indicativo="EB2ELU-11"
mision="DEEP_SPACE"
#altitud en metros a partir de la cual se quiere pasar de enviar fotos tan rápido (intervalo1) como se pueda a mandarlas más pausada esperando intervalo2 entre cada transmisión
altitud_ref=100

#######################################################################
#######################################################################
#######################################################################
#NO TOCAR
#NO TOCAR
#NO TOCAR
#NO TOCAR
#NO TOCAR
#NO TOCAR
#NO TOCAR
#NO TOCAR
#directorio donde se guardan las fotos
home="/home/pi/sstv/"
mkdir -p $home
#home="/home/felipe/Documents/radio/soft/globorasp/"
gpsFile=$home"gps.log"

#contador de transmisiones
contador=0

set -x
altitud=0
while true
do
	echo $contador
	gpspipe -w -n 10 |   grep -m 1 lon | python -mjson.tool > /tmp/gps.pos ; lat=`cat /tmp/gps.pos | grep lat | sed 's/,//g' | sed 's/"lat": //g' | sed 's/ //g'` ; lon=`cat /tmp/gps.pos | grep lon | sed 's/,//g' | sed 's/"lon": //g' | sed 's/ //g' ` ; alt=`cat /tmp/gps.pos | grep altMSL | sed 's/,//g' | sed 's/"altMSL": //g' | sed 's/ //g'` 
	
	#extraer datos del fichero de logs del GPS, se lee la última línea
	#tmpgps=`tail -n 1 $gpsFile`
	#gpsmessage=""
	#if [[ $tmpgps == *"0.0;0.0;;0.0"* ]]
	#then
#		gpsmessage="0.0;0.0;;0.0"
#	else
#		gpsmessage=`echo $tmpgps | sed 's/: /\n/g' | grep T`
#	fi

	position=""
	altura=$alt
	altitud=$alt
	lati=${lat::5}
	long=${lon::5}
	#lat_len=$(echo -n $lat | wc -m)
	position=$lati"/"$long
	#Si la salida del GPS es correcta se parsean los datos
	#if [[ $gpsmessage != "0.0;0.0;;0.0" ]]
	#then
		# Separo por punto y coma
		#horaGPS;Lat;LatOrientación;Lon;LonOrientación;altitud en metros;velocidad
		#IFS=';' read -ra ADDR <<< "$gpsmessage"
		#utc_fecha=${ADDR[0]}
		#latitude=${ADDR[1]}
		#latO=${ADDR[2]}
		#longitude=${ADDR[3]}
		#lonO=${ADDR[4]}
		#altitude=${ADDR[5]}
		#speed=${ADDR[6]}


		#tmpLat=$(echo $latitude | sed 's/^0*//')
		#tmpLon=$(echo $longitude | sed 's/^0*//')


		#echo $tmpLon
		# Si latitud o longitud tienen un tamaño muy grande se recortan para que entren bien en la imágen
		#lat=`echo "print($tmpLat/100)" | python3`
		#lon=`echo "print($tmpLon/100)" | python3`
		#lat_len=$(echo -n $lat | wc -m)
		#lon_len=$(echo -n $lon | wc -m)
		#latRest=`echo "print($lat_len - 6)" | python3`
		#lonRest=`echo "print($lon_len - 5)" | python3`
		#lat=${lat::-$latRest}
		#lon=${lon::-$lonRest}
		#altitud=`echo ${altitude%.*}`
		#position=$lat$latO"/"$lon$lonO
		#altura="$altitud.M"
		# configuramos la hora de la raspberry desde el GPS
		#date -s "$utc_fecha"
	#fi

	# tomamos la hora
	fecha=$(date +"%Y-%m-%d_%H%M%S")
	#hacemos una foto y la guardamos como fecha_hora.jpg
	libcamera-jpeg -t 1 --width 2592  --height 1944  -o $home"/"$fecha.big.jpg
	# raspistill -o $home"/"$fecha.big.jpg
	# imágen en blanco
	#convert -size 320x240 xc:white $fecha.big.jpg
	#redimensionamos la foto a 320x240
	convert $home"/"$fecha.big.jpg -resize 320x240! $home"/"$fecha.jpg

	#imágen aleatoria jpg
	#mx=320;my=240;head -c "$((3*mx*my))" /dev/urandom | convert -depth 8 -size "${mx}x${my}" RGB:- $fecha.jpg

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
	#borramos foto temporal
	rm $home"/"$fecha.1.jpg
	rm $home"/"$fecha.2.jpg
	rm $home"/"$fecha.3.jpg
	lockfile=$home"/lock"
	# reproducimos el wav
	while test -f "$lockfile"
	do
		echo "locked"
		sleep 1
	done
	touch $lockfile
	aplay $home"/"$fecha.sstv.wav
	rm $lockfile
	echo "played"

	#borramos el wav
	rm $home"/"$fecha.sstv.wav
	# comprobamos si llevamos menos transmisiones que las que queremos para el primer intervalo
	#echo "DONE"
	if [ $((altitud)) -lt $altitud_ref ]
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
	
