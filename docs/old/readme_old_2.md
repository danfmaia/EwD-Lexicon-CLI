# PI Text Processor

## Overview

The PI Text Processor is a comprehensive tool designed to convert standard English (SE) spelling into the Phonĕtic ‹I›nglish (PI) Scaffold-Spelling, a unique didactic spelling system. It supports different PI variations and integrates a dictionary for efficient word lookups and replacements.

## Key Components

- **Transcriber**: The core component that handles the interactive transcription of SE to PI. It supports 4 PI variations (L1, L2, L3, and Full Mode).
- **Dictionary**: A module managing the lookup and editing of PI dictionary entries.
- **Corpora Manager**: Manages corpus files, generates and updates the PI dictionary.

## Features

- **Interactive Transcription**: Users can transcribe texts interactively, reviewing and accepting PI transcriptions for each word.
- **Dictionary Editing**: Allows users to edit existing dictionary entries or add new entries to the PI dictionary.
- **Corpora Handling**: Handles updates to the corpus files and ensures the PI dictionary reflects these updates.

## Usage Instructions

1. **Starting the Transcription**: Run the script with the `--interactive` flag to start the interactive transcription mode. You can choose the desired PI variation (L1, L2, L3, FM).
2. **Interactive Mode Options**:
   - `(a)ccept`: Accept the current PI transcription and replace the SE word in the text.
   - `(n)ext`: Move to the next word in the text.
   - `(p)revious`: Go back to the previous word.
   - `(e)dit dictionary entry`: Edit the current word's dictionary entry.
   - `(s)kip sentence`: Skip to the next sentence.
   - `(q)uit`: Exit the interactive mode.
3. **Dictionary Editing**: When selecting to edit a dictionary entry, the current entry is displayed, and you can input a new or modified entry.
4. **Corpora Management**: The system automatically handles updates to corpus files and reflects these changes in the PI dictionary.

## File Structure

- `main.py`: The main script to run the PI Text Processor.
- `transcriber.py`: Contains the Transcriber class for handling the transcription process.
- `dictionary.py`: Manages dictionary lookups and editing.
- `corpora_manager.py`: Responsible for managing corpus files and updating the dictionary.

## Running the Script

To start the PI Text Processor, use the following command:

```
python main.py transcribe --interactive --file [input_file_path]
```

Replace `[input_file_path]` with the path to your input text file.
