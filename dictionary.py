from calendar import c
import json

import pyperclip
from config import Config
from corpora_manager import CorporaManager


class Dictionary:
    """
    Manages the operations related to the PI dictionary.

    This class handles the loading, editing, and updating of the PI dictionary. It includes methods for retrieving and modifying dictionary entries, which is essential for maintaining the accuracy and relevance of the PI dictionary.

    Attributes:
        filepath (str): File path to the PI dictionary.
        excluded_words (list): List of words to be excluded from the dictionary.
        pi_dictionary (dict): The loaded PI dictionary with applied exclusions.

    Methods:
        load_pi_dictionary: Loads the PI dictionary, excluding specified words.
        get_entry: Retrieves a specific entry from the dictionary.
        edit_entry: Provides an interface for editing a dictionary entry.
        update_entry: Updates a specific entry in the dictionary.
    """

    def __init__(self, excluded_words):
        """
        Initializes the Dictionary class with specified exclusions.

        Args:
            excluded_words (list): A list of words to exclude from the dictionary.
        """
        self.filepath = Config.DICTIONARY_FILEPATH
        self.excluded_words = excluded_words
        self.pi_dictionary = self.load_pi_dictionary(excluded_words)

    def load_pi_dictionary(self, excluded_list):
        """
        Loads the PI dictionary from a file, applying exclusions.

        Args:
            excluded_list (list): List of words to be excluded from the dictionary.

        Returns:
            dict: The PI dictionary with exclusions applied.
        """
        with open(self.filepath, 'r') as file:
            dictionary = json.load(file)

        if excluded_list:
            # Remove excluded words
            for word in excluded_list:
                dictionary.pop(word, None)

        return dictionary

    def get_entry(self, word):
        """
        Retrieves the dictionary entry for the specified word.

        Args:
            word (str): The word to look up in the dictionary.

        Returns:
            dict or None: The dictionary entry if found, otherwise None.
        """
        if word in self.pi_dictionary:
            return self.pi_dictionary[word]
        return None

    def edit_entry(self, word):
        """
        Provides an interactive interface to edit the dictionary entry for a given word.

        Allows the user to modify the dictionary entry of the specified word. If the word is not found in the dictionary, it informs the user.

        Args:
            word (str): The word for which the dictionary entry is to be edited.
        """
        print(f"Editing dictionary entry for: {word}")
        pi_entry = self.get_entry(word)
        if not pi_entry:
            print("No dictionary entry found for this word.")
            return

        # Display current entry
        current_corpus_row = pi_entry.get('whole', '')
        print("Current entry:", current_corpus_row)

        # Copy the current entry to system clipboard
        pyperclip.copy(current_corpus_row.split('| ')[1])

        # Prompt for new entry, pre-filling with the current entry
        new_entry = input(
            f"Editing entry: {word} | ")
        if new_entry == '':
            new_entry = current_corpus_row
        else:
            new_entry = f"{word} | {new_entry}"

        # Update the dictionary entry
        if new_entry and new_entry != current_corpus_row:
            self.update_entry(word, new_entry)
            print("Entry updated successfully.")
        else:
            print("No changes made to the entry.")

    def update_entry(self, word, new_entry):
        """
        Updates the dictionary entry for a specified word with a new entry.

        Args:
            word (str): The word for which the dictionary entry is to be updated.
            new_entry (str): The new entry to replace the existing one in the dictionary.
        """
        # TODO: check if this is really unnecessary
        # Update the dictionary entry
        # self.dictionary[word]['whole'] = new_entry

        # Update the corpus row and regenerate the dictionary
        corpora_manager = CorporaManager(self.pi_dictionary)
        corpora_manager.edit_corpus_row_and_update_dict(new_entry)

        # You might need additional logic here based on your dictionary structure
