#!/bin/bash

#  EwD Lexicon CLI - Readme.pdf" \
    cp "readme.md"  "_knowledge/EwD Lexicon CLI - Readme.md"

#  EwD Lexicon CLI - Readme.pdf" \
    pandoc "readme.md" -o "_knowledge/EwD Lexicon CLI - Readme.pdf" \
    --pdf-engine=xelatex --template=eisvogel --listings \
    -V mainfont="Linux Libertine PI" \
    -V sansfont="Linux Libertine PI" \
    -V monofont="Linux Libertine PI" \
    -V disable-header-and-footers

#  Changelog do IcD.pdf" \
    pandoc "ewd_changelog.md" -o "_knowledge/Changelog do IcD.pdf" \
    --pdf-engine=xelatex --template=eisvogel --listings \
    -V mainfont="Linux Libertine PI" \
    -V sansfont="Linux Libertine PI" \
    -V monofont="Linux Libertine PI" \
    -V disable-header-and-footers

# corpus_1000.txt
cp "corpora/corpus_1000.txt"  "_knowledge/"

# corpus_misc.txt
cp "corpora/corpus_misc.txt"  "_knowledge/"

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
