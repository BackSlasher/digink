#!/bin/bash
cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")"
RESOLUTION="800x600"
find digink/images/ -type f -print0 | parallel -0 mogrify -resize "$RESOLUTION"^ -gravity center -extent "$RESOLUTION"
