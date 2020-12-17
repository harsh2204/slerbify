#! /usr/bin/env bash
filename=$(basename -- "$1")
ext="${filename##*.}"
fname="${filename%.*}"

if [[ $ext != "wav" ]]
	then
	ffmpeg -i $filename $fname.wav
fi

rubberband -t 1.25 "$fname.wav" "$fname-slowed.wav" --pitch-hq --threads -P
# pitch -300 is the right one for slerb! lower ones work ok as well :/
sox "$fname-slowed.wav" "$fname-slerbified.wav" pitch -300 reverb 50 50 100

# Uncomment the following to cleanup everything after converting
#rm -rf "$fname-slowed.wav" "$fname.wav" 
