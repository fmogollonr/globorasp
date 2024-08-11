home=$1
sstv_mode=$2
echo SSTV mode is $sstv_mode
#rm $home/*.wav
#home=$1
set -x
resolution="640x496"

for i in $home/*.jpg 
do 
    if [[ $sstv_mode == "Robot36" ]]
    then 
        resolution="320x240"
    elif [[ $sstv_mode == "PD120" ]]
    then
        resolution="640x496"
    fi
    convert $i -resize $resolution! $i\_peq.jpg
    python3 -m pysstv --mode $sstv_mode --vox  $i\_peq.jpg $i.wav
    rm $i\_peq.jpg
done
