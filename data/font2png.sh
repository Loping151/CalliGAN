#!/bin/bash

FONT_DIR="data/font_files"

process_font() {
    local font=$1
    echo "Processing $font..."
    python data/font2png.py "$font"
}

for font in "$FONT_DIR"/*.{ttf,otf}
do
    if [[ -f "$font" ]]; then
        process_font "$font" &
    fi
done

wait
echo "All fonts processed."
