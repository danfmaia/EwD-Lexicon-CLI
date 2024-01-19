import json
import re
import sys


class Transcriber:
    def __init__(self):
        # Mapping for preliminary replace operations
        self.preliminar_replacements = {
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

    def load_pi_dictionary(self):
        """
        Function to load the PI dictionary, excluding words from preliminary replacements
        """
        # Implementation of load_pi_dictionary
        with open('dict/pi_dictionary.json', 'r') as file:
            pi_dictionary = json.load(file)

        # Remove words already handled in preliminary replacements
        for word in self.preliminar_replacements:
            pi_dictionary.pop(word, None)

        return pi_dictionary

    def update_words_for_piss_variation(self, input_text, pi_dictionary, variation):
        """
        Function to update words according to the chosen PISS variation
        """
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

    def transform_words_with_s_suffix(self, input_text, pi_dictionary, variation):
        """
        Function to handle words with 's' suffix
        """
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

    def perform_preliminar_replacements(self, input_text):
        """
        Function to perform preliminary text replacements
        """
        # Callback function for regex substitution
        def replacement_callback(match):
            word = match.group(0)
            replacement = self.preliminar_replacements[word.lower()]
            # Preserve case of the original word
            if word.istitle():
                return replacement.capitalize()
            elif word.isupper():
                return replacement.upper()
            else:
                return replacement

        # Perform replace operations
        for word in self.preliminar_replacements.keys():
            input_text = re.sub(r'\b{}\b'.format(
                word), replacement_callback, input_text, flags=re.IGNORECASE)

        return input_text

    def transcribe(self, input_text, variation='L1'):
        """
        Transcribe the provided text to PI format according to the specified variation.
        """
        pi_dictionary = self.load_pi_dictionary()
        processed_text = self.perform_preliminar_replacements(input_text)
        processed_text = self.update_words_for_piss_variation(
            processed_text, pi_dictionary, variation)
        processed_text = self.transform_words_with_s_suffix(
            processed_text, pi_dictionary, variation)
        return processed_text

    def process_sentence_interactively(self, sentences, current_sentence_index, variation):
        # Continues from the current sentence index
        while current_sentence_index < len(sentences):
            sentence = sentences[current_sentence_index]
            words = self.split_sentence_into_words(sentence)
            selected_index = 0

            while selected_index < len(words):
                display_sentence = self.highlight_selected_word(
                    sentence, words[selected_index])
                print()
                print(display_sentence)

                # Lookup in PI dictionary for the selected word
                pi_entry = self.lookup_pi_entry(words[selected_index])
                print()
                if pi_entry:
                    print(f"PI Entry: {pi_entry['whole']}")
                    print(f"{variation} word: {pi_entry['PI'][variation]}")
                else:
                    print("No PI entry found for this word.")

                print()
                user_action = input(
                    "Navigate: (n)ext, (p)revious, (s)kip sentence, (q)uit: ").lower()

                if user_action == 'n':
                    if selected_index < len(words) - 1:
                        selected_index += 1
                    else:
                        current_sentence_index += 1
                        break  # Break to move to the next sentence
                elif user_action == 'p':
                    if selected_index > 0:
                        selected_index -= 1
                    elif current_sentence_index > 0:
                        current_sentence_index -= 1
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        # Set to last selectable word
                        selected_index = len(words) - 1
                elif user_action == 's':
                    current_sentence_index += 1
                    break
                elif user_action == 'q':
                    print("Exiting interactive transcription.")
                    sys.exit()
                else:
                    print("Invalid input. Please choose 'n', 'p', 's', or 'q'.")

    def split_into_sentences(self, text):
        """
        Function to split text into sentences
        """
        # Simple sentence splitting based on punctuation
        # Consider using more sophisticated methods for complex texts
        sentences = re.split(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s', text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

        # Placeholder function for processing each sentence interactively

    def split_sentence_into_words(self, sentence):
        # Include only words, excluding characters like colons
        return re.findall(r'\b\w+\b', sentence)

        # Split based on spaces while keeping punctuation, but filter out non-word elements
        # words_with_punctuation = re.findall(r'\w+|[^\w\s]+|\s+', sentence)
        # return [word for word in words_with_punctuation if word.strip() and not word.isspace()]

    def highlight_selected_word(self, sentence, selected_word):
        def replace(match):
            return f'>{match.group(0)}<'

        # Use a regular expression to replace only whole words
        highlighted_sentence = re.sub(
            rf'\b{re.escape(selected_word)}\b', replace, sentence, count=1)
        return highlighted_sentence

    def lookup_pi_entry(self, word):
        """
        Look up the PI dictionary entry for the given word.
        """
        pi_dictionary = self.load_pi_dictionary()
        word_lower = word.lower()
        if word_lower in pi_dictionary:
            return pi_dictionary[word_lower]
        return None
