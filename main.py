import argparse
import os
import sys
from transcriber import Transcriber
from dict_gen import DictionaryGenerator


def main():
    parser = argparse.ArgumentParser(
        description='PI Text Processor Command Line Tool')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for dictionary update
    update_dict_parser = subparsers.add_parser(
        'update-dict', help='Update the PI dictionary from corpus files')

    # Subparser for transcription
    transcribe_parser = subparsers.add_parser(
        'transcribe', help='Transcribe text from Standard English to PI')

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

    args = parser.parse_args()
    if args.command == 'transcribe':
        if args.interactive:
            interactive_transcription(args)
        else:
            transcribe_text(args)
    elif args.command == 'update-dict':
        update_dictionary()
    else:
        parser.print_help()


def update_dictionary():
    DictionaryGenerator()


def transcribe_text(args):
    print("Welcome to the PI Transcriber Tool!")
    print("This tool assists in converting standard English texts to the PI Scaffold-Spelling (PISS) format.")

    input_filename = args.file
    input_text = read_input_file(input_filename)

    user_response = input(
        "Do you want to proceed with preliminary replacements? (y/n/q): ").lower()
    exit_if_user_aborted(user_response)

    transcriber = Transcriber()
    output_text = transcriber.perform_preliminar_replacements(input_text)

    # Save intermediate result
    temp_filename = 'io/temp' + os.path.splitext(input_filename)[1]
    save_to_file(temp_filename, output_text)
    print(f"Intermediate result saved to {temp_filename}")

    chosen_variation = choose_piss_variation()
    output_text = transcriber.transcribe(output_text, chosen_variation)

    # Dynamically name and save final output
    output_filename = generate_output_filename()
    save_to_file(output_filename, output_text)
    print(f"Final output saved to {output_filename}")


def interactive_transcription(args):
    # Read the input text
    input_text = read_input_file(args.file)

    print()
    user_response = input(
        "Do you want to update the dictionary before starting transcription? (y/n): ").lower()
    if user_response == 'y':
        update_dictionary()

    chosen_variation = choose_piss_variation()

    transcriber = Transcriber()

    # Split the text into sentences
    sentences = transcriber.split_into_sentences(input_text)
    # print('sentences:')
    # print(sentences)

    # Initialize the current sentence index
    current_sentence_index = 0

    # Process each sentence interactively
    while current_sentence_index < len(sentences):
        transcriber.process_sentence_interactively(
            sentences, current_sentence_index, chosen_variation)
        current_sentence_index += 1  # Move to the next sentence after processing


def read_input_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit()


def exit_if_user_aborted(response):
    if response == 'q':
        print("Operation aborted by the user.")
        sys.exit()
    elif response != 'y':
        print("Operation not confirmed. Exiting.")
        sys.exit()


def choose_piss_variation():
    piss_variations = ['L1', 'L2', 'L3', 'FM']
    print()
    print("Please choose a PISS variation:")
    print("L1 - Level 1, L2 - Level 2, L3 - Level 3, FM - Full Mode")
    chosen_variation = input("Enter your choice (L1/L2/L3/FM): ").upper()
    while chosen_variation not in piss_variations:
        print("Invalid choice. Please choose from L1, L2, L3, or FM.")
        chosen_variation = input("Enter your choice (L1/L2/L3/FM): ").upper()
    return chosen_variation


def generate_output_filename():
    n = 1
    output_filename = f'io/output_{n}.md'
    while os.path.exists(output_filename):
        n += 1
        output_filename = f'io/output_{n}.md'
    return output_filename


def save_to_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")
        sys.exit()


if __name__ == "__main__":
    main()
