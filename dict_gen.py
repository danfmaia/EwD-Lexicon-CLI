"""
This script, PI's Dictionary Generator (word_entries_gen), is a crucial component of the PI Text Processor. It is responsible for generating a PI dictionary by processing various corpus files. The script reads corpus files, extracts PI transcriptions, and compiles them into a comprehensive dictionary format. The result is a JSON file that forms a key part of the PI Text Processor, allowing for efficient lookup and translation of standard English to PI.

# Row Format for Corpus Files:
# SE | PI L1 < PI L2 > PI L3 ¦ PI FM
"""


# Row Format:
# SE | PI L1 < PI L2 > PI L3 ¦ PI full mode

import os
import json
import re


class DictionaryGenerator:
    def __init__(self):
        """
        Initializes the Dictionary Generator.
        - Sets up the corpus folder and the list of corpus files to be processed.
        - Initializes an empty dictionary to store the PI dictionary data.
        """
        corpus_folder = 'corpora'
        corpus_files = ['corpus_1000.txt',
                        'corpus_misc.txt', 'corpus_auto.txt']
        pi_dictionary = {}

        # Iterate over each corpus file and process the data
        for file_name in corpus_files:
            file_path = os.path.join(corpus_folder, file_name)
            rows = self.read_corpus_file(file_path)
            if rows:
                word_entries = self.process_corpus_data(rows)
                pi_dictionary.update(word_entries)

        # Write the PI dictionary data to a JSON file
        try:
            with open('dict/pi_dictionary.json', 'w', encoding='utf-8') as json_file:
                json.dump(pi_dictionary, json_file,
                          indent=4, ensure_ascii=False)
            print(
                "Dictionary updated successfully. Result file written to 'dict/pi_dictionary.json'")
        except IOError as e:
            print(f"Error writing to file 'dict/pi_dictionary.json.json': {e}")

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
            print(f"Error reading file {file_path}: {e}")
            return []

    def extract_pi_parts(self, pi_string):
        """
        Splits a PI transcription string into its constituent parts.
        If certain parts are missing in the PI transcription, they are filled with None.

        Args:
            pi_string (str): The PI transcription string to be split.
        Returns:
            list: A list containing the split parts of the PI transcription.
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

    def process_corpus_row(self, row):
        """
        Processes a single row from the corpus row and extracts the relevant information.
        The dictionary entry includes the whole row, PI transcriptions, and special flags if any.

        Args:
            row (str): A row from the corpus row.
        Returns:
            tuple: A tuple containing the SE word and its corresponding dictionary entry.
        """
        sf = None
        whole_row = row.strip()

        sf_match = re.search(r'….*\{(.+?)\}', row)
        if sf_match:
            sf = sf_match.group(1)
            row = row.split('…')[0]

        parts = row.split('|')
        se_word = parts[0].strip()

        if len(parts) > 1:
            corpus_row_parts = [se_word] + \
                self.extract_pi_parts(parts[1].strip())
        else:
            # Default to SE word
            corpus_row_parts = [se_word, se_word, se_word, se_word, se_word]

        L1_word = self.handle_special_cases(
            corpus_row_parts[1], corpus_row_parts, se_word)
        L2_word = self.handle_special_cases(
            corpus_row_parts[2], corpus_row_parts, L1_word or se_word)
        L3_word = self.handle_special_cases(
            corpus_row_parts[3], corpus_row_parts, L1_word or se_word)
        L4_word = self.handle_special_cases(
            corpus_row_parts[4], corpus_row_parts, L2_word or se_word)

        pi_entry = {"L1": L1_word, "L2": L2_word, "L3": L3_word, "FM": L4_word}

        return se_word, {"whole": whole_row, "PI": pi_entry, "Sf": sf}

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

    # def update_dictionary(self):
        # Additional method to handle the overall process of updating the dictionary
        # This might involve calling the above methods in a specific sequence
