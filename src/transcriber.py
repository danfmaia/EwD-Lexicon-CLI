import regex as re

from common.messages import Messages
from common.util import Util
from dictionary import Dictionary
from enums.variation import Variation


class Transcriber:
    """
    The Transcriber class handles the transcription of Standard English text to the PI format. It processes text to
    conform to the PI Scaffold-Spelling rules, offering both automated and interactive transcription modes.
    """

    def __init__(self, variation: Variation, perform_preliminary_replacements=False):
        """
        Initializes the Transcriber instance with necessary settings for transcription.

        Args:
            variation (str): Specifies the PI variation to be used for transcription.
            perform_preliminary_replacements (bool): Indicates whether to apply preliminary word replacements.
        """
        self.variation = variation.name

        self.performed_preliminar_replacements = perform_preliminary_replacements
        self.preliminary_replacements: dict[str, str] = {}
        self.dictionary: Dictionary
        if perform_preliminary_replacements:
            self.preliminary_replacements = variation.get_dict()
            self.dictionary = Dictionary(self.preliminary_replacements)
        else:
            self.dictionary = Dictionary()

        self.pi_entry = None
        self.current_sentence_index = 0
        self.selected_word_index = 0

    def refresh_dictionary(self):
        """
        Reloads the PI dictionary to reflect the latest updates or modifications.
        """
        if self.performed_preliminar_replacements:
            self.dictionary = Dictionary(self.preliminary_replacements)
        else:
            self.dictionary = Dictionary()
        Util.print_("Dictionary refreshed successfully.")

    def replace_words_for_pi_variation(self, input_text: int, pi_dictionary):
        """
        Transforms the input text according to the chosen PI variation by replacing words based on dictionary entries.

        Args:
            input_text (str): The text to be transformed.
            pi_dictionary (Dictionary): The dictionary containing PI entries.

        Returns:
            str: The transformed text with applied PI variations.
        """
        # Build a dictionary for replacements
        replacement_dict = {word: pi_dictionary[word]["PI"][self.variation]
                            for word in pi_dictionary
                            if pi_dictionary[word]["PI"][self.variation]}

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

        tokens = re.findall(r'\w+|[^\w\s]+|\s+', input_text)  # type: ignore
        updated_tokens = [replace_word(
            token) if token.strip() != '' else token for token in tokens]
        return ''.join(updated_tokens)

    def transform_words_with_s_suffix(self, input_text, pi_dictionary, variation):
        """
        Handles the transformation of words ending in 's', applying specific PI rules for these cases.

        Args:
            input_text (str): The text to be processed.
            pi_dictionary (Dictionary): The dictionary containing PI entries.
            variation (str): The chosen PI variation.

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
        updated_tokens = [
            transform_word(token) if token.strip() != '' else token for token in tokens]
        return ''.join(updated_tokens)

    def perform_preliminary_replacements(self, input_text):
        """
        Applies a set of predefined word replacements to the input text as an initial step in the transcription process.

        Args:
            input_text (str): The text to be processed.

        Returns:
            str: The text after applying preliminary replacements.
        """
        if self.preliminary_replacements == {}:
            raise ValueError("Preliminary replacements array not found.")

        def replacement_callback(match):
            word = match.group(0)
            replacement = self.preliminary_replacements[word.lower()]
            # Preserve case of the original word
            if word.istitle():
                return replacement.capitalize()
            elif word.isupper():
                return replacement.upper()
            else:
                return replacement

        # Perform replace operations
        for word in self.preliminary_replacements:
            input_text = re.sub(r'\b{}\b'.format(
                word), replacement_callback, input_text, flags=re.IGNORECASE)

        return input_text

    def transcribe(self, input_text):
        """
        Performs the complete transcription of the input text to the PI format using the specified PI variation.

        Args:
            input_text (str): The text to be transcribed.

        Returns:
            str: The transcribed text in the PI format.


        """
        pi_dictionary = self.dictionary.pi_dictionary
        processed_text = self.replace_words_for_pi_variation(
            input_text, pi_dictionary)
        processed_text = self.transform_words_with_s_suffix(
            processed_text, pi_dictionary, self.variation)
        return processed_text

    def transcribe_interactively(self, sentences, extension='.txt'):
        """
        Performs the complete transcription of the input text to the PI format using the specified PI variation.

        Args:
            input_text (str): The text to be transcribed.

        Returns:
            str: The transcribed text in the PI format.

        User Actions:
            a (when entry is found) - Accept action: Accepts the current PI word suggestion for the selected word.
            a (when no entry found) - Add dictionary entry action: Adds a new dictionary entry for the selected word.
            c - Customize action: Allows customizing the PI version of the selected word.
            n - Next word action: Moves to the next word in the current sentence.
            p - Previous word action: Moves to the previous word in the current sentence.
            ns - Next Sentence action: Moves to the next sentence in the list.
            ps - Previous Sentence action: Moves to the previous sentence in the list.
            q - Quit action: Exits the interactive transcription, with an option to save changes.
            e - Edit dictionary entry action: Edits an existing dictionary entry for the selected word.
        """
        variation = self.variation
        current_sentence_index = 0

        # Iterating through sentences
        while current_sentence_index < len(sentences):
            sentence = sentences[current_sentence_index]
            words = self.split_sentence_into_words(sentence)
            selected_word_index = 0
            enter_action = None

            # Iterating through words in the current sentence
            while selected_word_index < len(words):
                selected_word = words[selected_word_index]  # type: ignore

                # Display current sentence
                display_sentence = self.highlight_selected_word(
                    sentence, selected_word)
                Util.print_with_spacing(display_sentence)

                # from now on, the case doesn't matter
                selected_word = selected_word.lower()

                # Lookup in PI dictionary for the selected word
                pi_entry = self.dictionary.get_entry(selected_word)

                # Display word info
                if pi_entry:
                    pi_word = pi_entry['PI'][variation]
                    Util.print_with_spacing(f"PI Entry: {pi_entry['whole']}")
                    Util.print_(
                        f"{variation} word: {pi_word}")
                    if selected_word != pi_word:
                        Util.print_with_spacing(
                            f"    (A)ccept {variation} word {{ {pi_word} }} ?")
                    else:
                        Util.print_with_spacing(
                            f'    This is already a default {variation} word.')
                else:
                    print()
                    Util.print_with_spacing('No PI entry found for this word.')
                    Util.print_with_spacing(
                        f"    (A)dd dictionary entry for {{ {selected_word} }} ?")

                #
                # Prompt for a user action
                #

                if not enter_action:
                    enter_action = 'n'

                # # Dynamically set the dictionary action option based on whether the entry exists
                # dict_action = 'Add' if not pi_entry else 'Edit'
                # user_action = Util.input_with_spacing(
                #     f"Options: {'(A)ccept, ' if pi_entry else ''}{dict_action} dictionary (e)ntry, (C)ustomize, (N)ext, (P)revious, (S)kip sentence, (Q)uit: ").lower()

                Util.print_with_spacing('Options:')
                if pi_entry:
                    Util.print_(f'    a  -  Accept {variation} word')
                    Util.print_('    e  -  Edit dictionary entry')
                else:
                    print()
                    Util.print_('    a  -  Add dictionary entry')
                Util.print_('    c  -  Customize word')
                Util.print_('    n  -  Next word')
                Util.print_('    p  -  Previous word')
                Util.print_('    ns  - Next Sentence')
                Util.print_('    ps -  Previous Sentence')
                Util.print_('    q  -  Quit')
                user_action = Util.input_with_spacing(
                    f'Choose: [{enter_action}] ').lower()
                if user_action == '':
                    user_action = enter_action
                enter_action = user_action

                # Flags used in user actions
                word_updated = False
                switch_to_next_word = False

                #
                # User actions
                #

                # Accept action: replace the word and move to the next
                if user_action == 'a' and pi_entry:
                    pi_word = pi_entry['PI'][variation]

                    if selected_word != pi_word:
                        self.replace_word_in_all_sentences(
                            sentences, selected_word, pi_word)
                        Util.print_with_spacing(
                            f"All occurrences of '{selected_word}' replaced with '{pi_word}'")
                        word_updated = True
                    else:
                        Util.print_with_spacing(Messages.NO_CHANGES_MADE)

                    # # Update the current sentence with the latest changes
                    # sentence = sentences[current_sentence_index]
                    # words = self.split_sentence_into_words(sentence)

                    switch_to_next_word = True

                elif user_action == 'c':
                    if pi_entry:
                        pi_word = pi_entry['PI'][variation]
                    else:
                        pi_word = selected_word

                    custom_word = Util.input_with_spacing(
                        f"Enter a customized version for '{selected_word}': ").strip() or pi_word

                    if selected_word != custom_word:
                        self.replace_word_in_all_sentences(
                            sentences, selected_word, custom_word)
                        Util.print_with_spacing(
                            f"Word '{selected_word}' replaced with customized version '{custom_word}'")
                        word_updated = True
                    else:
                        Util.print_with_spacing(Messages.NO_CHANGES_MADE)

                    # # Update the current sentence with the latest changes
                    # sentence = sentences[current_sentence_index]
                    # words = self.split_sentence_into_words(sentence)

                    switch_to_next_word = True

                # Next word action
                elif user_action == 'n' or user_action == '':
                    switch_to_next_word = True

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

                # Add/Edit dictionary entry action
                elif (user_action == 'a' and not pi_entry) or (user_action == 'e'):
                    entry_updated = False
                    if not pi_entry:
                        entry_updated = self.dictionary.add_entry(
                            selected_word)
                    else:
                        entry_updated = self.dictionary.edit_entry(
                            selected_word)
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

                # Select next/previous sentence action
                elif user_action in ['ns', 'ps']:
                    current_sentence_index = (
                        current_sentence_index + (1 if user_action == 'ns' else -1)) % len(sentences)
                    if current_sentence_index < len(sentences):
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        selected_word_index = 0

                # Quit action
                elif user_action == 'q':
                    save_confirmation = Util.input_with_spacing(
                        "Save changes? (y/n): ").strip().lower()
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

                if word_updated:
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

                if switch_to_next_word:
                    # Move to the next word or the first word of the next sentence
                    selected_word_index += 1
                    if selected_word_index >= len(words):
                        current_sentence_index = (
                            current_sentence_index + 1) % len(sentences)
                        sentence = sentences[current_sentence_index]
                        words = self.split_sentence_into_words(sentence)
                        selected_word_index = 0

            # end while

            # Update the sentence in the list after processing
            sentences[current_sentence_index] = sentence

        # end while

    def split_into_sentences(self, text):
        """
        Splits the given text into individual sentences for processing.

        Args:
            text (str): The text to be split into sentences.

        Returns:
            List[str]: A list of individual sentences.
        """
        # Simple sentence splitting based on punctuation
        # Consider using more sophisticated methods for complex texts
        sentences = re.split(
            r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\n)\s', text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]

        # Placeholder function for processing each sentence interactively

    def rejoin_sentences(self, sentences):
        """
        Reassembles a list of sentences back into a single text string.

        Args:
            sentences (List[str]): A list of sentences to be joined.

        Returns:
            str: The reassembled text string.
        """
        return '\n\n'.join(sentences)

    def split_sentence_into_words(self, sentence):
        """
        Splits a sentence into individual words, taking into account combining diacritics.

        Args:
            sentence (str): The sentence to be split into words.

        Returns:
            List[str]: A list of words from the sentence.
        """
        # Correctly escape or position the hyphen in the character class
        cleaned_sentence = re.sub(r'^[+#*\s-]+', '', sentence)

        # Split the sentence into words based on spaces and punctuation, preserving words with diacritics
        words = re.findall(r'[\p{L}\p{M}]+', cleaned_sentence, re.UNICODE)
        return words

    def highlight_selected_word(self, sentence, selected_word):
        """
        Highlights the currently selected word in a sentence for interactive transcription.

        Args:
            sentence (str): The sentence containing the word.
            selected_word (str): The word to be highlighted.

        Returns:
            str: The sentence with the highlighted word.
        """
        def replace(match):
            return f'>{match.group(0)}<'

        # Use a regular expression to replace only whole words
        highlighted_sentence = re.sub(
            rf'\b{re.escape(selected_word)}\b', replace, sentence, count=1)
        return highlighted_sentence

    def replace_word_in_sentence(self, sentence, word, replacement):
        """
        Replaces a specific word in a sentence with its PI equivalent.

        Args:
            sentence (str): The sentence containing the word.
            word (str): The word to be replaced.
            replacement (str): The PI equivalent of the word.

        Returns:
            str: The updated sentence with the word replaced.
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
        Applies a word replacement across all sentences in a list.

        Args:
            sentences (List[str]): The list of sentences to be processed.
            original_word (str): The original word to be replaced.
            new_word (str): The replacement word.

        Returns:
            None: The sentences are modified in place.
        """
        if original_word == new_word:
            return

        # pylint: disable=consider-using-enumerate
        for i in range(len(sentences)):  # type: ignore
            sentences[i] = self.replace_word_in_sentence(
                sentences[i], original_word, new_word)
