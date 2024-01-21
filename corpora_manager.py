"""
Generates the PI dictionary by processing each corpus file.

Iterates over each corpus file, reads its content, processes the data to extract PI transcriptions, and updates the PI dictionary. Finally, saves the updated dictionary to a file.

Raises:
    IOError: If there's an error in reading the corpus files or saving the dictionary.

Row Format for Corpus Files:
    SE | PI L1 < PI L2 > PI L3 ¦ PI FM
"""

import os
import json
import re

from config import Config
from common.util import Util


class CorporaManager:
    """
    Manages the operations related to the corpus files used in the PI Text Processor.

    This class is responsible for reading, processing, and writing corpus data. It generates and maintains the PI dictionary, ensuring it stays updated with the latest corpus changes. The class handles tasks such as adding or editing corpus rows, extracting PI transcriptions, and persisting the updated dictionary to a file.

    Methods:
        generate_dictionary: Generates the PI dictionary from corpus files.
        edit_corpus_row_and_update_dict: Edits or adds a new row to the corpus and updates the dictionary.
        process_corpus_row: Processes individual rows of the corpus.
        extract_pi_parts: Extracts different PI transcription levels from a corpus string.
        save_pi_dictionary: Saves the current state of the PI dictionary to a file.

    Usage:
        The class should be instantiated and used by other components responsible for managing the PI Text Processor's corpus data.
    """

    def __init__(self, current_dictionary):
        """
        Initializes the Corpora Manager.
        - Sets up the corpus folder and the list of corpus files to be processed.
        - Initializes an empty dictionary to store the PI dictionary data.
        """

        self.dictionary_filepath = Config.DICTIONARY_FILEPATH
        self.corpus_folder = 'corpora'
        self.corpus_file_names = ['corpus_1000.txt',
                                  'corpus_misc.txt', 'corpus_new.txt', 'corpus_edited.txt']
        self.pi_dictionary = current_dictionary

    def generate_dictionary(self):
        """
        Generates the PI dictionary by processing each corpus file.

        Iterates over each corpus file, reads its content, processes the data to extract PI transcriptions, and updates the PI dictionary. Finally, saves the updated dictionary to a file.

        Raises:
            IOError: If there's an error in reading the corpus files or saving the dictionary.
        """
        for file_name in self.corpus_file_names:
            file_path = os.path.join(self.corpus_folder, file_name)
            rows = self.read_corpus_file(file_path)
            if rows:
                word_entries = self.process_corpus_data(rows)
                self.pi_dictionary.update(word_entries)

        self.save_pi_dictionary()

    def read_corpus_file(self, file_path):
        """
        Reads and returns the content of a corpus file.
        If an error occurs during file reading, an empty list is returned and an error message is printed.

        Args:
            file_path (str): The path to the corpus file to be read.
        Returns:
            list: A list of strings, each representing a line from the file.
        """

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()
        except IOError as e:
            Util.print_(f"Error reading file {file_path}: {e}")
            return []

    def extract_pi_parts(self, pi_string):
        """
        Extracts PI transcription parts from the given PI string.

        Parses the PI string to separate it into different transcription levels (L1, L2, L3, and Full Mode). Handles special syntax used in the corpus for representing transcription variants.

        Args:
            pi_string (str): The string containing PI transcriptions.

        Returns:
            list: A list containing the extracted PI transcriptions for each level.
        """
        # Split the string and ensure all PI parts are present
        pi_parts = re.split(r' < | > | ¦ ', pi_string)
        while len(pi_parts) < 4:
            pi_parts.append(None)  # Append None for missing PI parts
        return pi_parts

    def handle_special_cases(self, variation_part, corpus_row_parts, default):
        """
        Handles special cases in PI transcription processing.
        Special cases are denoted by '*' or '**'. If encountered, the function returns the default value.

        Args:
            pi_transcription (str): The PI transcription to be processed.
            default (str): The default value to be used if the PI transcription is a special case.

        Returns:
            str: The processed PI transcription or the default value for special cases.
        """

        if variation_part == '*':
            return corpus_row_parts[1]
        elif variation_part == '**':
            return corpus_row_parts[0]
        elif variation_part:
            return variation_part
        else:
            return default

    def process_corpus_data(self, rows):
        """
        Processes the data from the corpus file, row by row.
        Rows containing section delimiters or empty rows are skipped. Each valid row is processed to extract the PI dictionary entry.

        Args:
            rows (list): A list of rows from the corpus file.
        Returns:
            dict: A dictionary of processed word entries with SE words as keys.
        """
        word_entries = {}
        skip_section = False
        for row in rows:
            if "::::::::::" in row.strip():
                skip_section = not skip_section
                continue

            if skip_section or not row.strip():
                continue

            se_word, word_entry = self.process_corpus_row(row)
            if se_word not in word_entries:
                word_entries[se_word] = word_entry

        return word_entries

    def process_corpus_row(self, row):
        """
        Processes a single row of the corpus file.

        Extracts the Standard English word, PI transcriptions, and special flags from a corpus row. Returns a list containing these elements.

        Args:
            row (str): A single row from the corpus file.

        Returns:
            list: A list containing the SE word, PI transcriptions, and special flags.
        """
        sf = None
        whole_row = row.strip()

        # Special flag extraction
        sf_match = re.search(r'….*\{(.+?)\}', row)
        if sf_match:
            sf = sf_match.group(1)
            # Removing the special flag part from the row
            row = row.split('…')[0]

        # Splitting the row into its components
        parts = row.split('|')
        se_word = parts[0].strip()

        # Process further if additional parts exist
        if len(parts) > 1:
            # Default to SE word if no additional parts
            corpus_row_parts = [se_word] + \
                self.extract_pi_parts(parts[1].strip())
        else:
            # Default to SE word
            corpus_row_parts = [se_word, se_word, se_word, se_word, se_word]

        L1_word = self.handle_special_cases(
            corpus_row_parts[1], corpus_row_parts, se_word)  # type: ignore
        L2_word = self.handle_special_cases(
            corpus_row_parts[2], corpus_row_parts, L1_word or se_word)  # type: ignore
        L3_word = self.handle_special_cases(
            corpus_row_parts[3], corpus_row_parts, L1_word or se_word)  # type: ignore
        L4_word = self.handle_special_cases(
            corpus_row_parts[4], corpus_row_parts, L2_word or se_word)  # type: ignore

        pi_entry = {"L1": L1_word, "L2": L2_word, "L3": L3_word, "FM": L4_word}

        return se_word, {"whole": whole_row, "PI": pi_entry, "Sf": sf}

    def edit_corpus_row_and_update_dict(self, new_row, new=False):
        """
        Edits a specific corpus row and updates the PI dictionary accordingly.

        This function locates the given SE word in the 'corpus_new.txt' or 'corpus_edited.txt' file. If found, it updates the existing row; otherwise, it adds the new row. It then sorts the entries alphabetically and updates the PI dictionary with the new or modified entry.

        Args:
            new_row (str): The new row to be added or updated in the corpus file.

        Raises:
            IOError: If there's an error in reading from or writing to the corpus file.
        """
        corpus_file_name = 'corpus_new.txt' if new else 'corpus_edited.txt'
        corpus_filepath = os.path.join(self.corpus_folder, corpus_file_name)

        se_word, word_entry = self.process_corpus_row(new_row)

        # Read existing entries from the respective corpus file
        with open(corpus_filepath, 'r', encoding='utf-8') as file:
            entries = file.readlines()

        # Check if the entry exists and update it
        entry_found = False
        for i in range(len(entries)):  # type: ignore
            existing_se_word, _ = self.process_corpus_row(entries[i])
            if existing_se_word == se_word:
                entries[i] = new_row.strip() + '\n'
                entry_found = True
                break

        # Add the new entry if it doesn't exist
        if not entry_found:
            entries.append(new_row.strip() + '\n')

        # Sort entries alphabetically
        sorted_entries = sorted(entries, key=lambda x: x.lower())

        # Write updated entries back to corpus_edited.txt
        with open(corpus_filepath, 'w', encoding='utf-8') as file:
            file.writelines(sorted_entries)

        # Update the specific word entry in the pi_dictionary
        self.pi_dictionary[se_word] = word_entry

        Util.print_with_spacing(
            f"{'Updated' if entry_found else 'Added'} corpus row in '{corpus_filepath}'")

        # Save the updated dictionary
        self.save_pi_dictionary()

    def add_corpus_row_and_update_dict(self, new_row):
        """
        Adds a new corpus row and updates the PI dictionary accordingly.

        This function checks if the given SE word already exists in the 'corpus_new.md' file.
        If it exists, an error is raised. Otherwise, it adds the new row and updates the PI dictionary.

        Args:
            new_row (str): The new row to be added to the corpus file.

        Raises:
            IOError: If there's an error in reading from or writing to the corpus file.
            ValueError: If an entry with the given SE word already exists in the corpus.
        """
        corpus_filename = os.path.join(self.corpus_folder, 'corpus_new.md')

        se_word, word_entry = self.process_corpus_row(new_row)

        # Check if the entry already exists in corpus_new.md
        with open(corpus_filename, 'r', encoding='utf-8') as file:
            existing_entries = file.readlines()

        for entry in existing_entries:
            existing_se_word, _ = self.process_corpus_row(entry)
            if existing_se_word == se_word:
                raise ValueError(
                    f"An entry for '{se_word}' already exists in the corpus.")

        # Append the new entry to corpus_new.md
        with open(corpus_filename, 'a', encoding='utf-8') as file:
            file.write(new_row.strip() + '\n')

        # Update the specific word entry in the pi_dictionary
        self.pi_dictionary[se_word] = word_entry

        Util.print_with_spacing(f"Added new corpus row in '{corpus_filename}'")

        # Save the updated dictionary
        self.save_pi_dictionary()

    def save_pi_dictionary(self):
        """
        Saves the current state of the PI dictionary to a file.

        This method serializes the PI dictionary and saves it to a predefined file. It ensures data persistence for the PI dictionary across sessions.

        Raises:
            IOError: If there's an error in writing to the dictionary file.
        """
        try:
            with open(self.dictionary_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(self.pi_dictionary, json_file,
                          indent=4, ensure_ascii=False)
        except IOError as e:
            Util.print_with_spacing(
                f"Error writing to file {self.dictionary_filepath}: {e}")
