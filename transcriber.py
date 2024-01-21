import regex as re

from dictionary import Dictionary
from util import Util


class Transcriber:
    """
    Handles the transcription of Standard English text to the PI format.

    This class is responsible for processing text and converting it into the PI format based on specified transcription rules. It includes methods for handling word-level transcription, managing sentence structure, and applying specific transcription variations.

    Attributes:
        preliminary_replacements (dict): Predefined replacements for certain words.
        pi_dictionary (Dictionary): An instance of the Dictionary class for accessing the PI dictionary.
        current_sentence_index (int): Tracks the current sentence index during transcription.
        selected_word_index (int): Tracks the current word index in a sentence during transcription.

    Methods:
        refresh_dictionary: Reloads the PI dictionary.
        update_words_for_piss_variation: Applies specific PI variation rules to the text.
        transform_words_with_s_suffix: Handles words with 's' suffix based on PI rules.
        perform_preliminary_replacements: Performs initial word replacements in the text.
        transcribe: Transcribes the entire text to PI format.
        process_sentence_interactively: Processes sentences interactively for manual transcription.
        split_into_sentences: Splits text into sentences.
        split_sentence_into_words: Splits a sentence into words.
        highlight_selected_word: Highlights a word in a sentence for interactive processing.
        replace_word_in_sentence: Replaces a word in a sentence with its PI transcription.
    """

    def __init__(self):
        """
        Initializes the Transcriber class.

        Sets up the preliminary replacements, loads the PI dictionary, and initializes sentence and word index tracking for transcription processes.
        """
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

        self.dictionary = Dictionary(self.preliminar_replacements)

        self.pi_entry = None
        self.current_sentence_index = 0
        self.selected_word_index = 0

    def refresh_dictionary(self):
        """
        Reloads the PI dictionary.

        This method is used to refresh the dictionary data in case of updates or changes in the dictionary file.
        """
        self.dictionary = Dictionary(self.preliminar_replacements)
        print("Dictionary refreshed successfully.")

    def update_words_for_pi_variation(self, input_text: str, pi_dictionary, variation: str):
        """
        Applies PI variation rules to the input text.

        Args:
            input_text (str): The text to be processed.
            pi_dictionary (Dictionary): The PI dictionary instance.
            variation (str): The specified PI variation.

        Returns:
            str: The processed text with PI variation applied.
        """

        # Build a dictionary for replacements
        replacement_dict = {word: pi_dictionary[word]["PI"][variation]
                            for word in pi_dictionary
                            if pi_dictionary[word]["PI"][variation]}

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
        Transforms words with 's' suffix according to PI rules.

        Args:
            input_text (str): The text to be processed.
            pi_dictionary (Dictionary): The PI dictionary instance.
            variation (str): The specified PI variation.

        Returns:
            str: The text with transformed 's' suffix words.
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
        Performs initial replacements in the text based on predefined rules.

        Args:
            input_text (str): The text to be processed.

        Returns:
            str: The text after applying the preliminary replacements.
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
        for word in self.preliminar_replacements:
            input_text = re.sub(r'\b{}\b'.format(
                word), replacement_callback, input_text, flags=re.IGNORECASE)

        return input_text

    def transcribe(self, input_text, variation='L1'):
        """
        Transcribes the entire text to PI format.

        Args:
            input_text (str): The text to be transcribed.
            variation (str): The specified PI variation (default is 'L1').

        Returns:
            str: The transcribed text in PI format.
        """
        pi_dictionary = self.dictionary.pi_dictionary
        processed_text = self.update_words_for_pi_variation(input_text, pi_dictionary, variation)
        processed_text = self.transform_words_with_s_suffix(
            processed_text, pi_dictionary, variation)
        return processed_text

    def transcribe_interactively(self, sentences, variation, extension='.txt'):
        """
        Processes sentences interactively for manual transcription.

        Args:
            sentences (List[str]): The list of sentences to be processed.
            variation (str): The specified PI variation.

        Returns:
            Tuple[List[str], int]: The updated list of sentences and the updated sentence index.
        """
        # Initialize the current sentence index
        current_sentence_index = 0

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
                pi_entry = self.dictionary.get_entry(selected_word.lower())

                if pi_entry:
                    Util.print_with_spacing(f"PI Entry: {pi_entry['whole']}")
                    print(f"{variation} word: {pi_entry['PI'][variation]}")
                else:
                    Util.print_with_spacing("No PI entry found for this word.")
                    print()

                # Dynamically set the dictionary action option based on whether the entry exists
                dict_action = 'add' if not pi_entry else 'edit'
                user_action = Util.input_with_spacing(
                    f"Options: (a)ccept, (c)ustomize, (n)ext (or hit Enter), (p)revious, {dict_action} dictionary (e)ntry, next (s)entence, (q)uit: ").lower()

                entry_updated = False

                #
                # User Actions
                #

                # Accept action: replace the word and move to the next
                if user_action == 'a' and pi_entry:
                    pi_word = pi_entry['PI'][variation]
                    self.replace_word_in_all_sentences(
                        sentences, selected_word, pi_word)
                    Util.print_with_spacing(
                        f"All occurrences of '{selected_word}' replaced with '{pi_word}'")

                    entry_updated = True

                    # # Update the current sentence with the latest changes
                    # sentence = sentences[current_sentence_index]
                    # words = self.split_sentence_into_words(sentence)

                    # # Increment the index to move to the next word
                    # selected_word_index += 1

                elif user_action == 'c' and pi_entry:
                    pi_word = pi_entry['PI'][variation]
                    custom_word = input(
                        f"Enter a customized version for '{pi_word}': ").strip() or pi_word

                    self.replace_word_in_all_sentences(
                        sentences, selected_word, custom_word)
                    Util.print_with_spacing(
                        f"Word '{selected_word}' replaced with customized version '{custom_word}'")

                    entry_updated = True

                    # # Update the current sentence with the latest changes
                    # sentence = sentences[current_sentence_index]
                    # words = self.split_sentence_into_words(sentence)

                    # selected_word_index += 1  # Move to the next word

                if entry_updated:
                    # Update the current sentence with the latest changes
                    sentence = sentences[current_sentence_index]
                    words = self.split_sentence_into_words(sentence)

                    # Find the new position of the updated word or the next word
                    if selected_word in words:
                        selected_word_index = words.index(selected_word)
                    else:
                        selected_word_index = min(
                            selected_word_index, len(words) - 1)

                    output_text = self.rejoin_sentences(sentences)
                    Util.save_temp_text(output_text, extension)

                    # Increment the index to move to the next word
                    selected_word_index += 1

                # Next word action
                elif user_action == 'n' or user_action == '':
                    # Move to the next word or the first word of the next sentence
                    selected_word_index += 1
                    if selected_word_index >= len(words):
                        current_sentence_index = (
                            current_sentence_index + 1) % len(sentences)
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        selected_word_index = 0

                # Previous word action
                elif user_action == 'p':
                    # Move to the previous word or the last word of the previous sentence
                    if selected_word_index > 0:
                        selected_word_index -= 1
                    else:
                        current_sentence_index = (
                            current_sentence_index - 1 + len(sentences)) % len(sentences)
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        selected_word_index = len(words) - 1

                elif user_action == 'e':
                    entry_updated = False
                    if dict_action == 'add':
                        entry_updated = self.dictionary.add_entry(
                            selected_word.lower())
                    elif dict_action == 'edit':
                        entry_updated = self.dictionary.edit_entry(
                            selected_word.lower())

                    # Refresh the dictionary after modification
                    if entry_updated:
                        self.refresh_dictionary()

                    # The word index remains the same, so the user can review changes and decide the next action

                    # Refresh the current sentence and words list
                    # sentence = sentences[current_sentence_index]
                    # words = self.split_sentence_into_words(sentence)
                    # # Adjust selected index if needed
                    # selected_word_index = min(
                    #     selected_word_index, len(words) - 1)

                # Skip to the next sentence
                elif user_action == 's':
                    current_sentence_index += 1
                    if current_sentence_index < len(sentences):
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        selected_word_index = 0

                # Quit action
                elif user_action == 'q':
                    save_confirmation = Util.input_with_spacing(
                        "Do you want to save the changes? (y/n): ").strip().lower()
                    if save_confirmation == 'y':
                        output_text = self.rejoin_sentences(sentences)
                        Util.save_output_text(output_text, extension)
                        Util.print_with_spacing("Transcription saved.")
                    Util.print_with_spacing(
                        "Exiting interactive transcription.")
                    return

                else:
                    Util.print_with_spacing(
                        "Invalid input. Please choose a valid option or skip for (n)ext.")

            # end while

            sentences[current_sentence_index] = sentence

            # Update the sentence in the list after processing
            sentences[current_sentence_index] = sentence

        # end while

    def split_into_sentences(self, text):
        """
        Splits text into sentences.

        Args:
            text (str): The text to be split.

        Returns:
            List[str]: The list of sentences extracted from the text.
        """
        # Simple sentence splitting based on punctuation
        # Consider using more sophisticated methods for complex texts
        sentences = re.split(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s', text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

        # Placeholder function for processing each sentence interactively

    def rejoin_sentences(self, sentences):
        return '\n\n'.join(sentences)

    def split_sentence_into_words(self, sentence):
        """
        Splits a sentence into words, accounting for words with combining diacritics.

        Args:
            sentence (str): The sentence to be split.

        Returns:
            List[str]: The list of words extracted from the sentence.
        """
        # Correctly escape or position the hyphen in the character class
        cleaned_sentence = re.sub(r'^[+#*\s-]+', '', sentence)

        # Split the sentence into words based on spaces and punctuation, preserving words with diacritics
        words = re.findall(r'[\p{L}\p{M}]+', cleaned_sentence, re.UNICODE)
        return words

    def highlight_selected_word(self, sentence, selected_word):
        """
        Highlights a word in a sentence for interactive processing.

        Args:
            sentence (str): The sentence containing the word.
            selected_word (str): The word to be highlighted.

        Returns:
            str: The sentence with the selected word highlighted.
        """
        def replace(match):
            return f'>{match.group(0)}<'

        # Use a regular expression to replace only whole words
        highlighted_sentence = re.sub(
            rf'\b{re.escape(selected_word)}\b', replace, sentence, count=1)
        return highlighted_sentence

    def replace_word_in_sentence(self, sentence, word, replacement):
        """
        Replaces a word in a sentence with its PI transcription.

        Args:
            sentence (str): The sentence containing the word to be replaced.
            word (str): The word to be replaced.
            replacement (str): The PI transcription to replace the word.

        Returns:
            str: The sentence with the word replaced by its PI transcription.
        """
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

    def replace_word_in_all_sentences(self, sentences, original_word, new_word):
        """
        Replaces all occurrences of a word in a list of sentences with a new word.

        Args:
            sentences (List[str]): The list of sentences to process.
            original_word (str): The word to be replaced.
            new_word (str): The word to replace with.

        Returns:
            None: The method modifies the sentences list in place.
        """
        for i in range(len(sentences)):  # type: ignore
            sentences[i] = self.replace_word_in_sentence(
                sentences[i], original_word, new_word)
