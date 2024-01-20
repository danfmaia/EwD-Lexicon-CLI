import argparse
import os
import sys

from transcriber import Transcriber
from corpora_manager import CorporaManager
from util import Util


def main():
    """
    Main function to handle command-line arguments and execute the appropriate actions.

    It sets up the argument parser for different commands like updating the dictionary and transcribing text. Based on the user's choice, it calls the respective functions to perform these actions.
    """
    parser = argparse.ArgumentParser(
        description='PI Text Processor Command Line Tool')
    # Setting up subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for dictionary update
    update_dict_parser = subparsers.add_parser(
        'update-dict', help='Update the PI dictionary from corpus files')

    # Subparser for transcription
    transcribe_parser = subparsers.add_parser(
        'transcribe', help='Transcribe text from Standard English to PI')
    # Adding arguments for the transcribe command
    transcribe_parser.add_argument(
        '--text', help='Text to transcribe', type=str)
    transcribe_parser.add_argument(
        '--file', help='File path for text to transcribe', type=str, default='io/input.md')
    transcribe_parser.add_argument(
        '--output', help='Output file path', type=str)
    transcribe_parser.add_argument(
        '--variation', help='PISS variation to use (L1, L2, L3, Full Mode)', type=str, default='L1')
    transcribe_parser.add_argument(
        '--interactive', action='store_true', help='Enable interactive transcription mode')

    # Parsing the arguments and executing the corresponding function
    args = parser.parse_args()
    if args.command == 'transcribe':
        if args.interactive:
            transcribe_text_interactively(args)
        else:
            transcribe_text(args)
    elif args.command == 'update-dict':
        update_dictionary()
    else:
        parser.print_help()


def update_dictionary():
    """
    Updates the PI dictionary using the CorporaManager.

    This function generates the PI dictionary by processing corpus files. It is called when the 'update-dict' command is used.
    """
    CorporaManager({}).generate_dictionary()


def transcribe_text(args):
    """
    Handles the transcription of text from Standard English to PI.

    Args:
        args: Command-line arguments containing input file, output file, and PISS variation information.
    """
    print("Welcome to the PI Transcriber Tool!")
    print("This tool assists in converting standard English texts to the PI Scaffold-Spelling (PISS) format.")

    input_filename = args.file
    extension = os.path.splitext(input_filename)[1]
    input_text = read_input_file(input_filename)

    user_response = input(
        "Do you want to proceed with preliminary replacements? (y/n/q): ").lower()
    exit_if_user_aborted(user_response)

    transcriber = Transcriber()
    output_text = transcriber.perform_preliminar_replacements(input_text)

    Util.save_temp_text(output_text, extension)

    chosen_variation = choose_piss_variation()
    output_text = transcriber.transcribe(
        output_text, chosen_variation)

    Util.save_output_text(output_text, extension)


def transcribe_text_interactively(args):
    """
    Provides an interactive interface for transcription.

    This function allows the user to transcribe text interactively, offering a more hands-on approach to text conversion.

    Args:
        args: Command-line arguments containing input file and PISS variation information.
    """
    input_filename = args.file
    extension = os.path.splitext(input_filename)[1]
    input_text = read_input_file(args.file)

    user_response = Util.input_with_spacing(
        "Do you want to update the dictionary before starting transcription? (y/n): [n]").lower()
    if user_response == 'y':
        update_dictionary()

    chosen_variation = choose_piss_variation()

    transcriber = Transcriber()

    # Split the text into sentences
    sentences = transcriber.split_into_sentences(input_text)

    extension = os.path.splitext(input_filename)[1]
    transcriber.transcribe_interactively(
        sentences, chosen_variation, extension)


def read_input_file(file_path):
    """
    Reads text from the specified input file.

    Args:
        file_path (str): The path to the file containing text to be transcribed.

    Returns:
        str: The text read from the file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit()


def exit_if_user_aborted(response):
    """
    Exits the program if the user decides to abort the operation.

    Args:
        is_aborted (bool): Flag to indicate if the user has chosen to abort.

    Raises:
        SystemExit: If the user has chosen to abort.
    """
    if response == 'q':
        print("Operation aborted by the user.")
        sys.exit()
    elif response != 'y':
        print("Operation not confirmed. Exiting.")
        sys.exit()


def choose_piss_variation():
    """
    Provides a user interface to choose the PISS variation for transcription.

    Prompts the user to select from available PISS variations (L1, L2, L3, Full Mode) and validates the input.

    Returns:
        str: The chosen PISS variation.
    """
    piss_variations = ['L1', 'L2', 'L3', 'FM']
    Util.print_with_spacing("Please choose a PISS variation:")
    print("L1 - Level 1, L2 - Level 2, L3 - Level 3, FM - Full Mode")
    chosen_variation = Util.input_with_spacing(
        "Enter your choice (L1/L2/L3/FM): [default=L1]").upper()
    if (chosen_variation == ''):
        chosen_variation = 'L1'
    while chosen_variation not in piss_variations:
        Util.print_with_spacing(
            "Invalid choice. Please choose from L1, L2, L3, or FM.")
        chosen_variation = Util.input_with_spacing(
            "Enter your choice (L1/L2/L3/FM): [default=L1]").upper()
    return chosen_variation


if __name__ == "__main__":
    main()
