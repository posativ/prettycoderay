#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "please provide a css class"
    exit 1
fi

for VAR in `python -c "from pygments.styles import get_all_styles; print '\n'.join(get_all_styles())"`; do
    pygmentize -S $VAR -f html | python convert.py --class $1 > css/$VAR.css
done
