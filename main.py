import sys
import argparse
from transcriber import Transcriber
from dict_gen import DictionaryGenerator


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='PI Text Processor Command Line Tool')

    # Define arguments
    parser.add_argument(
        '--transcribe', help='Transcribe text from Standard English to PI', action='store_true')
    parser.add_argument(
        '--update-dict', help='Update the PI dictionary from corpus files', action='store_true')
    parser.add_argument('--text', help='Text to transcribe', type=str)
    parser.add_argument(
        '--file', help='File path for text to transcribe', type=str)
    parser.add_argument('--output', help='Output file path', type=str)
    parser.add_argument(
        '--variation', help='PISS variation to use (L1, L2, L3, Full Mode)', type=str, default='L1')

    # Parse arguments
    args = parser.parse_args()

    # Process commands
    if args.transcribe:
        transcribe_text(args)
    elif args.update_dict:
        update_dictionary()
    else:
        parser.print_help()


def transcribe_text(args):
    """
    Transcribe text using the Transcriber module.
    """
    transcriber = Transcriber()

    # Read text from file or command line
    if args.file:
        with open(args.file, 'r') as file:
            text = file.read()
    else:
        text = args.text

    # Transcribe text
    transcribed_text = transcriber.transcribe(text, args.variation)

    # Output transcribed text
    if args.output:
        with open(args.output, 'w') as file:
            file.write(transcribed_text)
    else:
        print(transcribed_text)


def update_dictionary():
    """
    Update the PI dictionary using the DictionaryGenerator module.
    """
    dict_gen = DictionaryGenerator()
    dict_gen.update_dictionary()
    print("Dictionary updated successfully.")


if __name__ == "__main__":
    main()
