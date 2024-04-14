#!/bin/bash

#  EwD Lexicon CLI - Readme.md&pdf" \
    cp "readme.md"  "_knowledge/EwD Lexicon CLI - Readme.md"
    pandoc "readme.md" -o "_knowledge/EwD Lexicon CLI - Readme.pdf" \
    --pdf-engine=xelatex --template=eisvogel --listings \
    -V mainfont="Linux Libertine PI" \
    -V sansfont="Linux Libertine PI" \
    -V monofont="Linux Libertine PI" \
    -V disable-header-and-footers

#
# docs
#

# Cheatsheet IPA p/ Vogais do Português e do Inglês.pdf
pandoc "docs/course/Cheatsheet IPA de Vogais.md" -o "docs/course/Curso IcD – Cheatsheet IPA de Vogais pro Português e Inglês.pdf" \
--pdf-engine=xelatex --template=eisvogel --listings \
-V mainfont="Linux Libertine PI" \
-V sansfont="Linux Libertine PI" \
-V monofont="Linux Libertine PI" \
-V disable-header-and-footers

# EwD Corpora & General Info (in EwD v2.8 L1).pdf
pandoc "corpora/corpora_info_in_ewd.md" -o "_knowledge/EwD Corpora & General Info (in EwD v2.8 L1).pdf" \
--pdf-engine=xelatex --template=eisvogel --listings \
-V mainfont="Linux Libertine PI" \
-V sansfont="Linux Libertine PI" \
-V monofont="Linux Libertine PI" \
-V disable-header-and-footers

# EwD Corpora & General Info.pdf
    pandoc "corpora/corpora_info.md" -o "_knowledge/EwD Corpora & General Info.pdf" \
    --pdf-engine=xelatex --template=eisvogel --listings \
    -V mainfont="Linux Libertine PI" \
    -V sansfont="Linux Libertine PI" \
    -V monofont="Linux Libertine PI" \
    -V disable-header-and-footers
