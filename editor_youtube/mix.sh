#!/bin/bash
# usage: mix.sh OUTNAME ; needs out/video_silent.mp4 and out/music.wav. Voice normalised to a file first (single-graph loudnorm truncated the tail).
set -e; P=/home/claude/project; O=${1:-GTA6_might_be_worse_v1.mp4}
[ -f $P/out/voice_norm.wav ] || ffmpeg -v error -y -i $P/assets/narration_declan_sage.mp3 -af "aformat=sample_rates=44100:channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=9" $P/out/voice_norm.wav
ffmpeg -v error -y -i $P/out/video_silent.mp4 -i $P/out/voice_norm.wav -i $P/out/music.wav \
 -filter_complex "[2:a]volume=0.40[m];[1:a][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.85,volume=0.85[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -t 514.1 $P/out/$O
ffprobe -v error -show_entries format=duration:stream=codec_type,duration -of csv=p=0 $P/out/$O
