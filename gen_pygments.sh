#!/bin/bash

for VAR in `python -c "from pygments.styles import get_all_styles; print '\n'.join(get_all_styles())"`; do
    pygmentize -S $VAR -f html | python convert.py --class $1 > css/$VAR.css
done