#! /usr/bin/env bash
filename=$(basename -- "$1")
ext="${filename##*.}"
fname="${filename%.*}"
echo $filename
echo $ext
echo $fname

if [[ $ext != "wav" ]]
	then
	ffmpeg -i $filename $fname.wav
fi
file=$fname.wav

rubberband -t 1.25 $file "$fname-slowed.wav" --pitch-hq --threads -P
## pitch -300 is the right one for lemonade slerb!
sox $file "$fname-slerbified.wav" pitch -300 reverb 50 50 100
