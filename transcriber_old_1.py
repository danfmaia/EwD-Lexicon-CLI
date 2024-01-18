import json
import re
import os
import sys

# Mapping for preliminar replace operations
preliminar_replacements = {
    'the': 'the̬',
    'a': 'a̬',
    'an': 'a̬n',
    'of': '‹o̬v›',
    'to': 'to̬',
    'you': 'yöu',
    'this': 'thiṣ',
    'and': 'and',
}


def load_word_entries():
    with open('word_entries/word_entries.json', 'r') as file:
        word_entries = json.load(file)

    for word in preliminar_replacements:
        # Remove the word if it exists in word_entries
        word_entries.pop(word, None)

    return word_entries


def update_words_for_piss_variation(input_text, word_entries, variation):
    replacement_dict = {word.lower(): word_entries[word]["PI"].get(variation)
                        for word in word_entries
                        if word_entries[word]["PI"].get(variation)}

    def replace_word(word):
        lower_word = word.lower()
        if lower_word in replacement_dict:
            replacement = replacement_dict[lower_word]
            if word.isupper():
                return replacement.upper()
            elif word[0].isupper():
                return replacement[0].upper() + replacement[1:]
            return replacement
        return word

    tokens = re.findall(r'\w+|[^\w]', input_text)
    updated_tokens = [replace_word(
        token) if token.strip() != '' else token for token in tokens]
    return ''.join(updated_tokens)


def perform_preliminar_replacements(input_text):
    # Mapping for simple replace operations

    def replacement_callback(match):
        word = match.group(0)
        # Determine the replacement word
        replacement = preliminar_replacements[word.lower()]
        # Preserve the case of the original word
        if word.istitle():
            return replacement.capitalize()
        elif word.isupper():
            return replacement.upper()
        else:
            return replacement

    # Perform replace operations
    for word in preliminar_replacements.keys():
        input_text = re.sub(r'\b{}\b'.format(
            word), replacement_callback, input_text, flags=re.IGNORECASE)

    return input_text


def main():
    print("Welcome to the PI Transcriber Tool!")
    print("This tool performs preliminary text replacements based on specific rules.")

    input_filename = 'io/input.md'
    try:
        with open(input_filename, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{input_filename}': {e}")
        return None

    user_response = input(
        "Do you want to proceed with preliminary replacements? (y/n/q): ").lower()
    if user_response == 'q':
        print("Operation aborted by the user.")
        sys.exit()
    elif user_response != 'y':
        print("Operation not confirmed. Exiting.")
        sys.exit()

    output_text = perform_preliminar_replacements(input_text)

    # Save the intermediate result to a temp file
    temp_filename = 'io/temp' + os.path.splitext(input_filename)[1]
    try:
        with open(temp_filename, 'w') as file:
            file.write(output_text)
        print(f"Intermediate result saved to {temp_filename}")
    except Exception as e:
        print(f"Error writing to file '{temp_filename}': {e}")
        return None

    # Prompt for PISS variation
    piss_variations = ['L1', 'L2', 'L3', 'FM']
    print("Please choose a PISS variation:")
    print("L1 - Level 1, L2 - Level 2, L3 - Level 3, FM - Full Mode")
    chosen_variation = input("Enter your choice (L1/L2/L3/FM): ").upper()
    while chosen_variation not in piss_variations:
        print("Invalid choice. Please choose from L1, L2, L3, or FM.")
        chosen_variation = input("Enter your choice (L1/L2/L3/FM): ").upper()

    print(
        f"Processing text based on the chosen PISS variation: {chosen_variation}")

    word_entries = load_word_entries()
    output_text = update_words_for_piss_variation(
        output_text, word_entries, chosen_variation)

    # Save the updated result again to the temp file
    try:
        with open(temp_filename, 'w') as file:
            file.write(output_text)
        print(f"Intermediate result saved to {temp_filename}")
    except Exception as e:
        print(f"Error writing to file '{temp_filename}': {e}")
        return None

    # Final save prompt
    user_response = input(
        "Do you want to save the final result? (y/n/q): ").lower()
    if user_response == 'q':
        print("Operation aborted by the user.")
        sys.exit()
    elif user_response != 'y':
        print("Operation not confirmed. Exiting.")
        sys.exit()

    # Determine the output filename
    n = 1
    output_filename = 'io/output_{}.md'.format(n)
    while os.path.exists(output_filename):
        n += 1
        output_filename = 'io/output_{}.md'.format(n)

    try:
        with open(output_filename, 'w') as file:
            file.write(output_text)
        print(f"Final output saved to {output_filename}")
    except Exception as e:
        print(f"Error writing to file '{output_filename}': {e}")
        return None


if __name__ == "__main__":
    main()
