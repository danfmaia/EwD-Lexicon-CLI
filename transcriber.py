import json
import re
import os
import sys

# Mapping for preliminary replace operations
preliminar_replacements = {
    'the': 'the̬',
    'a': 'a̬',
    'an': 'a̬n',
    'of': '‹o̬v›',
    'to': 'to̬',
    'you': 'yöu',
    'this': 'thiṣ',
    'and': 'and',
    'for': 'for',
    'from': 'fro̬m'
}

# Function to load the PI dictionary, excluding words from preliminary replacements


def load_pi_dictionary():
    with open('dict/pi_dictionary.json', 'r') as file:
        pi_dictionary = json.load(file)

    # Remove words already handled in preliminary replacements
    for word in preliminar_replacements:
        pi_dictionary.pop(word, None)

    return pi_dictionary

# Function to update words according to the chosen PISS variation


def update_words_for_piss_variation(input_text, pi_dictionary, variation):
    # Build a dictionary for replacements
    replacement_dict = {word: pi_dictionary[word]["PI"].get(variation)
                        for word in pi_dictionary
                        if pi_dictionary[word]["PI"].get(variation)}

    # Function to replace a single word
    def replace_word(word):
        lower_word = word.lower()
        if lower_word in replacement_dict:
            replacement = replacement_dict[lower_word]
            # Preserve case of the original word
            if word.isupper():
                return replacement.upper()
            elif word[0].isupper():
                return replacement[0].upper() + replacement[1:]
            return replacement
        return word

    tokens = re.findall(r'\w+|[^\w\s]+|\s+', input_text)
    updated_tokens = [replace_word(
        token) if token.strip() != '' else token for token in tokens]
    return ''.join(updated_tokens)

# Function to handle words with 's' suffix


def transform_words_with_s_suffix(input_text, pi_dictionary, variation):
    # Function to transform a word with 's' suffix
    def transform_word(word):
        if word[-1] == 's' and (len(word) < 2 or word[-2] != 's'):
            base_word = word[:-1]
            lower_base_word = base_word.lower()

            # Check if the base word (without 's') is in the dictionary
            if lower_base_word in pi_dictionary and variation in pi_dictionary[lower_base_word]["PI"]:
                replacement = pi_dictionary[lower_base_word]["PI"][variation]

                # Ensure replacement is not None before concatenating 's'
                if replacement is not None:
                    # Preserve case of the original word
                    if base_word[0].isupper():
                        replacement = replacement.capitalize()
                    return replacement + 's'
        return word

    tokens = re.findall(r'\w+|[^\w\s]+|\s+', input_text)
    updated_tokens = [transform_word(
        token) if token.strip() != '' else token for token in tokens]
    return ''.join(updated_tokens)

# Function to perform preliminary text replacements


def perform_preliminar_replacements(input_text):
    # Callback function for regex substitution
    def replacement_callback(match):
        word = match.group(0)
        replacement = preliminar_replacements[word.lower()]
        # Preserve case of the original word
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

# Main function of the script


def main():
    print("Welcome to the PI Transcriber Tool!")
    print("This tool assists in converting standard English texts to the PI Scaffold-Spelling (PISS) format. It performs preliminary replacements and updates text according to the selected PISS variation.")

    # Load input file
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

    # Preliminary replacements
    user_response = input(
        "Do you want to proceed with preliminary replacements? (y/n/q): ").lower()
    if user_response == 'q':
        print("Operation aborted by the user.")
        sys.exit()
    elif user_response != 'y':
        print("Operation not confirmed. Exiting.")
        sys.exit()

    output_text = perform_preliminar_replacements(input_text)

    # Save intermediate result
    temp_filename = 'io/temp' + os.path.splitext(input_filename)[1]
    try:
        with open(temp_filename, 'w') as file:
            file.write(output_text)
        print(f"Intermediate result saved to {temp_filename}")
    except Exception as e:
        print(f"Error writing to file '{temp_filename}': {e}")
        return None

    # Choose PISS variation
    piss_variations = ['L1', 'L2', 'L3', 'FM']
    print("Please choose a PISS variation:")
    print("L1 - Level 1, L2 - Level 2, L3 - Level 3, FM - Full Mode")
    chosen_variation = input("Enter your choice (L1/L2/L3/FM): ").upper()
    while chosen_variation not in piss_variations:
        print("Invalid choice. Please choose from L1, L2, L3, or FM.")
        chosen_variation = input("Enter your choice (L1/L2/L3/FM): ").upper()

    # Process text based on the chosen variation
    print(
        f"Processing text based on the chosen PISS variation: {chosen_variation}")
    pi_dictionary = load_pi_dictionary()
    output_text = update_words_for_piss_variation(
        output_text, pi_dictionary, chosen_variation)
    output_text = transform_words_with_s_suffix(
        output_text, pi_dictionary, chosen_variation)

    # Save updated result again
    try:
        with open(temp_filename, 'w') as file:
            file.write(output_text)
        print(f"Intermediate result saved to {temp_filename}")
    except Exception as e:
        print(f"Error writing to file '{temp_filename}': {e}")
        return None

    # Final saving step
    user_response = input(
        "Do you want to save the final result? (y/n/q): ").lower()
    if user_response == 'q':
        print("Operation aborted by the user.")
        sys.exit()
    elif user_response != 'y':
        print("Operation not confirmed. Exiting.")
        sys.exit()

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
