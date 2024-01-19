import re
import sys

from typing import List

from dict.dictionary import Dictionary
from util import Util


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

        self.pi_dictionary = Dictionary(self.preliminar_replacements)

        self.pi_entry = None
        self.current_sentence_index = 0
        self.selected_word_index = 0

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
        processed_text = self.perform_preliminar_replacements(input_text)
        processed_text = self.update_words_for_piss_variation(
            processed_text, self.pi_dictionary, variation)
        processed_text = self.transform_words_with_s_suffix(
            processed_text, self.pi_dictionary, variation)
        return processed_text

    def process_sentence_interactively(self, sentences, current_sentence_index, variation):
        # Iterating through sentences
        while current_sentence_index < len(sentences):
            sentence = sentences[current_sentence_index]
            words = self.split_sentence_into_words(sentence)
            selected_word_index = 0

            # Iterating through words in the current sentence
            while selected_word_index < len(words):
                selected_word = words[selected_word_index]  # type: ignore
                display_sentence = self.highlight_selected_word(
                    sentence, selected_word)
                Util.print_with_spacing(display_sentence)

                # Lookup in PI dictionary for the selected word
                pi_entry = self.pi_dictionary.lookup_pi_entry(selected_word)
                if pi_entry:
                    Util.print_with_spacing(
                        f"PI Entry: {pi_entry['whole']}\n{variation} word: {pi_entry['PI'][variation]}")
                else:
                    print("No PI entry found for this word.")

                # User action input
                print()
                user_action = input(
                    "Options: (a)ccept, (n)ext (or hit 'Enter'), (p)revious, (s)kip sentence, (q)uit: ").lower()

                # Accept action: replace the word and move to the next
                if user_action == 'a' and pi_entry:
                    pi_word = pi_entry['PI'][variation]
                    for i in range(len(sentences)):  # type: ignore
                        sentences[i] = self.replace_word_in_sentence(
                            sentences[i], selected_word, pi_word)
                    print(
                        f"All occurrences of '{selected_word}' replaced with '{pi_word}'")

                    # Update the current sentence with the latest changes
                    sentence = sentences[current_sentence_index]
                    words = self.split_sentence_into_words(sentence)

                    # Move to the next word after replacement, ensuring we don't exceed the list length
                    selected_word_index += 1
                    if selected_word_index >= len(words):
                        current_sentence_index += 1
                        if current_sentence_index < len(sentences):
                            sentence = sentences[current_sentence_index]
                            words = self.split_sentence_into_words(sentence)
                            selected_word_index = 0  # Start at the first word of the new sentence
                # Next word action
                elif user_action == 'n' or user_action == '':
                    selected_word_index += 1
                    # Move to the next sentence if end of current sentence is reached
                    if selected_word_index >= len(words):
                        current_sentence_index += 1
                        if current_sentence_index < len(sentences):
                            sentence = sentences[current_sentence_index]
                            words = self.split_sentence_into_words(sentence)
                            selected_word_index = 0
                # Previous word action
                elif user_action == 'p':
                    if selected_word_index > 0:
                        selected_word_index -= 1
                    else:
                        # Move to the previous sentence
                        if current_sentence_index > 0:
                            current_sentence_index -= 1
                            sentence = sentences[current_sentence_index]
                            words = self.split_sentence_into_words(sentence)
                            selected_word_index = len(words) - 1
                # Skip to the next sentence
                elif user_action == 's':
                    current_sentence_index += 1
                    if current_sentence_index < len(sentences):
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        selected_word_index = 0
                # Quit action
                elif user_action == 'q':
                    print("Exiting interactive transcription.")
                    return
                else:
                    print(
                        "Invalid input. Please choose 'a', 'n', '', 'p', 's', or 'q'.")

            # Update the sentence in the list after processing
            sentences[current_sentence_index] = sentence

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

    def replace_word_in_sentence(self, sentence, word, replacement):
        def replace(match):
            # Preserve case of the original word
            matched_word = match.group(0)
            if matched_word.isupper():
                return replacement.upper()
            elif matched_word.istitle():
                return replacement.capitalize()
            else:
                return replacement

        # Use regular expression to replace only whole words, case-insensitively
        pattern = rf'\b{re.escape(word)}\b'
        return re.sub(pattern, replace, sentence, flags=re.IGNORECASE)
