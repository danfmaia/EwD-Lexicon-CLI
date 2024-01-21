import argparse
import os
import sys

from transcriber import Transcriber
from corpora_manager import CorporaManager
from util import Util


def main():
    """
    Entry point for the PI Text Processor CLI.

    Parses command-line arguments to execute dictionary updates or text transcription. Supports two main commands:
    - 'update-dict': Update the PI dictionary from corpus files.
    - 'transcribe': Transcribe text from Standard English to PI with various options.
    """
    parser = argparse.ArgumentParser(
        description='PI Text Processor CLI')
    # Setting up subparsers for different commands
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for Update Dictionary command
    # update_dict_parser = subparsers.add_parser(
    #     'update-dict', help='Update the PI dictionary from corpus files')

    # Subparser for the Transcribe command
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
        '--variation', help='PI variation to use (L1, L2, L3, Full Mode)', type=str, default='L1')
    transcribe_parser.add_argument(
        '--interactive', action='store_true', help='Enable interactive transcription mode')

    # Parsing the arguments and executing the corresponding function
    args = parser.parse_args()
    if args.command == 'update-dict':
        update_dictionary_command()
    elif args.command == 'transcribe':
        transcribe_command(args)
    else:
        parser.print_help()


def update_dictionary_command():
    """
    Updates the PI dictionary using data from corpus files.
    """
    CorporaManager({}).generate_dictionary()
    Util.print_with_spacing("Dictionary updated successfully.")


def transcribe_command(args):
    """
    Handles transcription of text from Standard English to PI based on command-line arguments.

    Supports text input from a file and various transcription options, including interactive mode.
    Provides an initial welcome message and guides through the transcription process.

    Args:
        args (Namespace): Parsed command-line arguments containing options for transcription.
    """
    Util.print_with_spacing("Welcome to the PI Transcriber Tool!")
    print("This tool assists in converting standard English texts to the PI Scaffold-Spelling (PISS) format.")

    input_file_path = args.file
    ext = os.path.splitext(input_file_path)[1]
    input_text = read_input_file(input_file_path)

    transcriber = Transcriber()

    user_response = Util.input_with_spacing(
        "Do you want to update the dictionary before starting transcription? (y/n): [n] ").lower()
    if user_response == 'y':
        update_dictionary_command()

    temp_text = perform_preliminary_replacements(transcriber, input_text, ext)

    chosen_variation = choose_pi_variation()
    print(chosen_variation)

    if (not args.interactive):
        temp_text = transcriber.transcribe(temp_text, chosen_variation)
        Util.save_output_text(temp_text, ext)
    else:
        sentences = transcriber.split_into_sentences(temp_text)
        transcriber.transcribe_interactively(
            sentences, chosen_variation, ext)


def read_input_file(file_path):
    """
    Reads and returns text from a specified input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Content of the input file.
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
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


def perform_preliminary_replacements(transcriber: Transcriber, input_text, ext):
    """
    Performs preliminary text replacements before transcription.

    Asks the user if preliminary replacements are desired and applies them if confirmed. The modified text is
    temporarily saved, and the user is informed about the performed replacements.

    Args:
        transcriber (Transcriber): Instance of the Transcriber class to perform replacements.
        input_text (str): The initial text to process.
        extension (str): File extension of the input file for temporary saving.

    Returns:
        str: Text after performing preliminary replacements.
    """

    user_response = Util.input_with_spacing(
        "Do you want to perform preliminary replacements? (y/n): ").lower()

    temp_text = ''
    if user_response == 'y':
        temp_text = transcriber.perform_preliminar_replacements(input_text)
        Util.print_with_spacing('Preliminary replacements performed.')
        Util.save_temp_text(temp_text, ext)
    else:
        temp_text = input_text
        Util.print_with_spacing('Preliminary replacements NOT performed.')

    return temp_text


def choose_pi_variation():
    """
    Provides a user interface to choose the PI variation for transcription.

    Prompts the user to select from available PI variations (L1, L2, L3, Full Mode) and validates the input.

    Returns:
        str: The chosen PI variation.
    """
    piss_variations = ['L1', 'L2', 'L3', 'FM']
    Util.print_with_spacing("Please choose a PI variation:")
    print("L1 - Level 1, L2 - Level 2, L3 - Level 3, FM - Full Mode")
    chosen_variation = Util.input_with_spacing(
        "Enter your choice (L1/L2/L3/FM): [default=L1] ").upper()
    if (chosen_variation == ''):
        chosen_variation = 'L1'
    while chosen_variation not in piss_variations:
        Util.print_with_spacing(
            "Invalid choice. Please choose from L1, L2, L3, or FM.")
        chosen_variation = Util.input_with_spacing(
            "Enter your choice (L1/L2/L3/FM): [default=L1] ").upper()
    return chosen_variation


if __name__ == "__main__":
    main()
