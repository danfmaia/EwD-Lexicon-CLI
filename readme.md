# PI Text Processor

## Overview

The PI Text Processor is a versatile tool designed for transcribing Standard English texts into Phonetic English (PI) format, adhering to the PI Scaffold-Spelling (PISS) system. It consists of two main components: the Transcriber and the Dictionary Generator.

## Components

1. **Transcriber (`transcriber.py`)**:

   - Handles the conversion of Standard English to various PISS variations (L1, L2, L3, Full Mode).
   - Performs preliminary replacements and updates text based on selected PISS variation.

2. **Dictionary Generator (`dict_gen.py`)**:
   - Generates and updates the PI dictionary using corpus files.
   - Processes corpus rows into word entries, ensuring order and avoiding duplicates.

## Installation

Clone the repository or download the source code:

```bash
git clone https://github.com/your-repository/PI-Text-Processor.git
cd PI-Text-Processor
```

## Usage

### Transcription

To transcribe text from Standard English to PI:

```bash
python main.py transcribe --file <input_file_path>
```

- `--file`: Path to the input text file for transcription.

### Dictionary Update

To update the PI dictionary from corpus files:

```bash
python main.py update-dict
```

## Interactive Workflow

The tool prompts users for inputs and confirms actions at various stages:

- Confirming preliminary replacements.
- Selecting PISS variation.
- Saving intermediate and final results.

## Output

- Outputs are saved in dynamically named files to prevent overwriting.
- Intermediate results are stored temporarily for review.

## Contributing

Contributions to the PI Text Processor are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under [Your License Name].

## Contact

For questions or suggestions, please contact [Your Contact Information].
