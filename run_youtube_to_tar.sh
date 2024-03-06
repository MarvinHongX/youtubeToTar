#!/bin/bash
process_count=$(ps aux | grep "youtube_to_tar.py" | grep -v "grep" | wc -l)

if [ $process_count -gt 0 ]; then
    echo "youtube_to_tar.py is already running."
    exit 
fi

python3 /home/total/sh/youtubeToTar/youtube_to_tar.py  >> /home/total/log/youtube_to_tar.log 2>&1 &
