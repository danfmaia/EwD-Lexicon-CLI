# PI Text Processor

## Components:

- Main Code

  > `main.py`

- PI Transcriber

  > `trancriber.py`

- PI DictGen (Dictionary Generator)

  > `dict_gen.py`

This is a script for processing a SE text and converting it (word by word) to PI, while incrementing the PI corpora during the process.

## Interactive Transcription

Command

### Motivation

The main motivation is incrementing PI's word collection, while also developing a text transcriber in the process.

### Actors

1. User

2. Script

### Steps

1. User runs

1. Before running the script, User puts the input text in the “io” folder, under the name “input.txt”.

1. User runs Script.

1. Script processes the corpus rows contained on the 3 corpora files located in the “corpora” folder. The files are named “corpus_1000.txt”, “corpus_misc.txt” and “corpus_auto.txt”. The word entry follows the format explained in the “corpus_info.md” file.

   3.1) Script process the files in the following order: “corpus_1000.txt” then “corpus_misc.txt” then “corpus_auto.txt”.

   3.2) Script converts each corpus row into word entries. Each word entry has a minimum of 1 value (the SE word) and a maximum of 5 values (the SE word and its respective L1, L2, L3 and full mode words).

   3.3) Scripts store all word entries in a single variable of suitable type.

   3.4) Script doesn't store a given word more than once. If a given word is located on more than one corpus (or twice in a single corpus), only the first occurrence is considered.

1. Script ask User to select the PI level or mode which he pretends to transcribe the text for. The available options are L1, L2, L3 and full mode.

1. Script start showing to User the words from the input text in the following manner:

   5.1) Script shows to User 1 to 7 words from the current sentence, including punctuation and any special characters between each word, and respecting words' capitalization. It starts from the first sentence. A given word is always the “selected one”. This word will be placed between the characters > and <. E.g., >bird<.

   5.2) A maximum of 3 words located to the left and 3 words located to the right of the selected word are also shown to User. That's why Script shows to User a minimum of 1 word (in case of single-word sentence) and a maximum of 7 words (in case of sentence with 7 or more words). [TODO - Give examples.]

1. With the current sentence being shown to User:

   6.1) Script browse the word entries for the currently selected word. In the word entry side, the word used for comparison (key) is always the SE word. The word comparison is case insensitive.

   6.2) If a match happens:

   6.2a) [To be continued]

## PI Transcriber

[TODO]
