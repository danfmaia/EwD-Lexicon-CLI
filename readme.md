© Danilo Florentino Maia, 2024

# EwD Lexicon CLI

## Overview

EwD Lexicon CLI, an experimental Python-based tool, is developed to convert English texts into the EwD (English with Diacritics) format. EwD, representing texts processed by the English Diacritical System (EDS), aims to facilitate the learning of English pronunciation and listening skills by employing diacritical marks to indicate pronunciation cues.

## Purpose

This tool is central to the "Didactics with Scaffolding Strategies" research project, exploring the efficiency of different methodologies in teaching pronunciation and listening. The PI Method, focusing on integrating individualizable educational strategies with intelligent audiovisual tools, utilizes EwD Lexicon CLI to make phonetic learning more efficient and engaging.

## Components

- **Python Files**:

  - `main.py`: Executes command-line instructions.
  - `config.py`: Contains configuration settings.
  - `transcriber.py`: Manages the transcription from English to EwD format.
  - `dictionary.py`: Oversees the English-to-EwD dictionary.
  - `corpora_manager.py`: Handles corpus files for dictionary enhancement.

- **Corpus Files**:

  - `corpus_misc.txt` and `corpus_1000.txt`: Include word mappings for English-to-EwD conversion.

- **Dictionary Files**:

  - `ewd_lexicon.json`: The conversion dictionary for EwD.
  - `dictionary_schema.json`: Outlines the structure of the conversion dictionary.

- **Documentation**:
  - `corpus_info.md` and `transcriber_steps.md`: Offer details on corpus structure and transcription methodology.
  - `Manifesto of PI.pdf`: Argues the foundation of the PI Method.
  - `Summary of English with Diacritics v2.1.pdf`: Summarizes the EDS proposed by the PI Project.

## Installation

1. Ensure Python 3.x is installed.
2. Download or clone the source code.
3. Run `pip install -r requirements.txt` to install dependencies.

## Usage

EwD Lexicon CLI provides a command-line interface for transforming English text into the EwD format, supporting both file-based and interactive modes.

### Transcribe Command

To convert English text to EwD:

```
python main.py transcribe [--text TEXT] [--file FILE] [--output OUTPUT] [--variation VARIATION]
```

Options include specifying text directly, defining input and output file paths, and selecting the EwD variation (L1, L2, L3, or FM).

### Interactive Mode

For real-time transcription, use:

```
python main.py transcribe --interactive
```

## Research Context and Methodology

- **Development of NLP Algorithms**: Enhances scaffolded learning approaches by analyzing pronunciation patterns.
- **User-Centric Approach**: Focuses on adaptability and individualization through a feedback loop for system refinement.

## Impact and Vision

- Aims to improve pronunciation and comprehension skills significantly.
- Develops an adaptive learning system tailored to individual learners' needs.
- Encourages interdisciplinary collaboration across linguistics, pedagogy, and computer science.

## Challenges and Future Directions

- Addresses the academic acceptance and practical implementation of the EwD system.
- Discusses scalability and resource requirements for broader application across languages and educational contexts.

## Ethical Considerations and Impact Measurement

- Adheres to ethical guidelines in data handling and analysis.
- Evaluates impact through performance assessments and statistical analysis of learner progress.

## Conclusion

EwD Lexicon CLI is a pivotal element of a pioneering research initiative aimed at transforming language teaching with AI-enhanced methodologies, focusing particularly on pronunciation and oral comprehension.

## Contributing

Contributions to EwD Lexicon CLI are encouraged. See `CONTRIBUTING.md` for more details.

## Contact

For inquiries or support, please email [contact@ewdproject.org](mailto:contact@ewdproject.org).

## License

[GNU GPLv3](./LICENCE.txt)

---

© Danilo Florentino Maia, 2024
