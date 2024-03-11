© Danilo Florentino Maia, 2024

# PI Text Processor

## Overview

The PI Text Processor is an experimental Python-based tool designed to convert English texts into the PI format. The PI format, also known as PI Scaffold-Spelling, is an adaptation of English orthography designed to facilitate the learning of pronunciation and listening in English.

## Purpose

This tool plays a central role in the research project titled "Didactics with Scaffolding Strategies," which aims to investigate and compare the efficiency of different methodologies for teaching pronunciation and listening. One of the methodologies being investigated is the PI Method, a new didactic approach that proposes integrating individualizable educational strategies with intelligent audiovisual tools, in an effort to make phonetic learning more efficient and engaging.

## Components

- **Python Files**:

  - `main.py`: The main script for executing commands.
  - `config.py`: Configuration settings.
  - `transcriber.py`: Handles the transcription of English to PI.
  - `dictionary.py`: Manages the English-to-PI dictionary.
  - `corpora_manager.py`: Manages corpus files for dictionary updates.

- **Corpus Files**:

  - `corpus_misc.txt` and `corpus_1000.txt`: Contain English-to-PI word mappings.

- **Dictionary Files**:

  - `pi_dictionary.json`: Conversion dictionary.
  - `dictionary_schema.json`: Dictionary schema.

- **Documentation**:
  - `corpus_info.md` and `transcriber_steps.md`: Information on corpus structure and transcription steps.
  - `Manifesto of PI.pdf`: A comprehensive pitch document that argues for the existence of the PI methodology.
  - `Summary of PI Scaffold-Spelling v2.1.pdf`: A summary of the didactic spelling system proposed by PI.

## Installation

1. Install Python 3.x.
2. Clone/download the source code.
3. Install dependencies: `pip install -r requirements.txt`.

## Usage

The tool offers a CLI for converting English text to PI, supporting file-based and interactive modes.

### Transcribe Command

Converts English text to PI using various options.

```
python main.py transcribe [--text TEXT] [--file FILE] [--output OUTPUT] [--variation VARIATION]
```

- `--text TEXT`: Directly specify the text.
- `--file FILE`: Path to the English text file.
- `--output OUTPUT`: Path for the transcribed output.
- `--variation VARIATION`: PI variation (L1, L2, L3, or FM — ).

### Interactive Mode

For real-time transcription, use the option `--interactive`:

```
python main.py transcribe --interactive
```

## Research Context and Methodology

- **NLP Algorithms Development**: Analyzing pronunciation patterns to enhance scaffolded learning approaches.
- **User-Centric Approach**: A feedback loop for system improvement, focusing on adaptability and individualization.

## Impact and Vision

- **Improvements in Linguistic Skills**: Advancements in pronunciation and comprehension skills.
- **Adaptive Learning System**: An AI system that adapts teaching strategies to individual learner needs.
- **Interdisciplinary Collaboration**: Collaboration across linguistics, pedagogy, and computer science.

## Challenges and Future Directions

- **Academic Acceptance and Practical Implementation**: Addressing challenges in academic acceptance and practical implementation.
- **Scalability and Resources**: Discussing scalability and resource needs for expanding to different languages and educational contexts.

## Ethical Considerations and Impact Measurement

- **Ethical Guidelines Adherence**: Following ethical guidelines in data collection and analysis.
- **Impact Measurement**: Performance evaluations, statistical analysis, and satisfaction surveys.

## Conclusion

The PI Text Processor is instrumental in a pioneering research project, seeking to revolutionize language teaching with AI-enhanced methods, especially in pronunciation and oral comprehension.

## Contributing

Contributions are welcome. Please refer to `CONTRIBUTING.md` for guidelines.

## License

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit [http://creativecommons.org/licenses/by/4.0/](http://creativecommons.org/licenses/by/4.0/) or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

## Contact

For inquiries or assistance, get in touch with [contact@thepimethod.org](mailto:contact@thepimethod.org).

---

© Danilo Florentino Maia, 2024
