#!/bin/bash

script=$(readlink -f $0)
script_dir=$(dirname $script)

tracklist_raw=$(xclip -selection c -out)

tracklist_formatted=$(echo "$tracklist_raw" | $script_dir/bandcamp-tracklist-to-rym.pl)

echo "$tracklist_formatted" | xclip -selection c -in

echo -e "Tracklist Replaced in Xclip Buffer!\n"
echo "$tracklist_formatted" | sed 's/^/  /'
