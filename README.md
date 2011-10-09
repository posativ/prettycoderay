# Usage

A [pygments][1] CSS to [CodeRay][2] converter. It can handle most tokens, but some are not available in CodeRay and/or a CodeRay-only token. Early beta and only tested with some python and YAML.

    git clone https://posativ.org/git/prettycoderay

You need *pygments* installed (CodeRay is not required). Do `easy_install pygments`. Use this, to render the "trac" theme. Available themes: monokai, manni, perldoc, borland, colorful, default, murphy, vs, trac, tango, fruity, autumn, bw, emacs, vim, pastie, friendly and native.

    pygmentize -S trac -f html | python pygments2coderay.py --class .syntaxhl

See `/css` for a static compilation of the current pygments css files. Done via `./gen.sh .syntaxhl`


[1]: http://pygments.org/
[2]: http://coderay.rubychan.de/
