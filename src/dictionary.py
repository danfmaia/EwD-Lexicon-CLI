import json

import pyperclip
from common.config import DICTIONARY_PATH
from corpora_manager import CorporaManager
from common.util import Util


class Dictionary:
    """
    Manages the PI dictionary, facilitating various operations such as loading, editing, and updating entries.

    This class is responsible for handling the PI dictionary, including the loading of dictionary data from a file, and providing functionalities for adding or editing entries. It integrates with the CorporaManager to ensure consistency between the corpus and the dictionary. The class supports customizing the dictionary by excluding specific words and offers methods for interacting with dictionary entries.

    Attributes:
        filepath (str): Path to the file containing the PI dictionary.
        excluded_words (list): List of words to be excluded when loading the dictionary.
        pi_dictionary (dict): The loaded PI dictionary, with exclusions applied if specified.
        corpora_manager (CorporaManager): An instance of CorporaManager for managing corpus-related operations.

    Methods:
        load_pi_dictionary: Loads the PI dictionary from the file, applying any specified exclusions.
        get_entry: Retrieves a specific entry from the dictionary.
        add_entry: Adds a new entry to the dictionary.
        edit_entry: Edits an existing entry in the dictionary.
    """

    def __init__(self, excluded_words=None):
        """
        Initializes the Dictionary class with specified exclusions.

        Args:
            excluded_words (list): A list of words to exclude from the dictionary.
        """
        self.filepath = DICTIONARY_PATH
        self.excluded_words = excluded_words
        self.pi_dictionary = self.load_pi_dictionary(excluded_words)
        self.corpora_manager = CorporaManager(self.pi_dictionary)

    def load_pi_dictionary(self, excluded_list=None):
        """
        Loads the PI dictionary from a file, optionally applying exclusions.

        This method reads the PI dictionary from a JSON file and excludes any words specified in the 'excluded_list'. This functionality allows for the customization of the dictionary based on specific requirements or contexts.

        Args:
            excluded_list (list, optional): A list of Standard English words to be excluded from the dictionary. Defaults to None.

        Returns:
            dict: The PI dictionary with specified exclusions applied, if any.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
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

    def add_entry(self, word):
        """
        Adds a new entry to the dictionary for a given word.

        This method facilitates the addition of a new dictionary entry for a specified word. It prompts the user to input details for the new entry and updates the corpus and dictionary accordingly.

        Args:
            word (str): The word for which the dictionary entry is to be added.

        Returns:
            bool: True if the entry was successfully added, False otherwise.
        """
        Util.print_with_spacing(f"Adding new dictionary entry for: {word}")

        # Prompt the user for the new entry details
        Util.print_("Corpus row format: SE | PI L1 < PI L2 > PI L3 ¦ PI FM")
        new_entry = Util.input_(f"New entry: {word} | ").strip()
        if new_entry == '':
            user_response = Util.input_with_spacing(
                "Are you sure the new entry contains only the SE word? (y/n): [y] ")
            if user_response in ['y', '']:
                new_entry = f"{word} | "
        else:
            new_entry = f"{word} | {new_entry}"

        # Save the new dictionary entry
        if new_entry and new_entry != '':
            self.corpora_manager.edit_corpus_row_and_update_dict(
                new_entry, new=True)
            Util.print_("Entry added successfully.")
            return True
        else:
            Util.print_with_spacing("No new entry added.")
            return False

        # # Check if the user provided input
        # if new_entry:
        #     full_entry = f"{word} | {new_entry}"
        #     self.corpora_manager.edit_corpus_row_and_update_dict(full_entry)
        #     # Append the new entry to 'corpus_new.md'
        #     with open("corpus_new.md", "a") as corpus_file:
        #         corpus_file.write(f"{full_entry}\n")

        #     # Update the in-memory dictionary
        #     # Assuming the dictionary format is as follows: { 'word': { 'whole': '...', 'PI': {...}, ... } }
        #     self.pi_dictionary[word] = {
        #         'whole': full_entry, 'PI': self.extract_pi_variations(new_entry)}
        #     Util.print_("New entry added successfully.")
        # else:
        #     Util.print_("No new entry added.")

    def edit_entry(self, word):
        """
        Provides an interactive interface to edit the dictionary entry for a given word.

        This method allows the user to modify the dictionary entry of a specified word. It displays the current entry, if it exists, and allows the user to provide a new or modified entry. The changes are then reflected in the corpus and dictionary.

        Args:
            word (str): The word for which the dictionary entry is to be edited.

        Returns:
            bool: True if the entry was successfully updated, False otherwise.
        """
        Util.print_with_spacing(f"Editing dictionary entry for: {word}")
        pi_entry = self.get_entry(word)
        if not pi_entry:
            Util.print_with_spacing("No dictionary entry found for this word.")
            return False

        # Display current entry
        current_corpus_row = pi_entry.get('whole', '')
        Util.print_(f"Current: {current_corpus_row}")

        # Copy the current entry to system clipboard
        # if not numpy.any(numpy.isnan(current_corpus_row.split('| ')[1])):
        if len(current_corpus_row.split('| ')) > 1:
            pyperclip.copy(current_corpus_row.split('| ')[1])

        # Prompt for new entry, pre-filling with the current entry
        new_entry = Util.input_(f"Editing: {word} | ")
        if new_entry == '':
            new_entry = current_corpus_row
        else:
            new_entry = f"{word} | {new_entry}"
        Util.print_('new entry: ' + new_entry)

        # Update the dictionary entry
        if new_entry and new_entry != current_corpus_row:
            self.corpora_manager.edit_corpus_row_and_update_dict(new_entry)
            Util.print_("Entry updated successfully.")
            return True
        else:
            Util.print_with_spacing("No changes made to the entry.")
            return False
