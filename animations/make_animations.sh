#!/bin/bash

#mkdir -p $1

rm $1/*.txt
rm $1/*.jpg

ffmpeg -i $2 -vf scale="720:480" -y $1/output.mp4
mplayer -ao null $1/output.mp4 -vo jpeg:outdir=$1

# read myrows mycols < <(stty size)

# newrows=`echo "$myrows * 1" | bc`
# newcols=`echo "$mycols * 0.47" | bc`

# echo $newrows $newcols
# python3 ascii_movie.py $1/output.mp4 4 15 $1  $newrows $newcols


