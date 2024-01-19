# This is PI's Dictionary Generator (word_entries_gen). It will be used by the bigger script PI Text Processor. It is the first part of that script that is being developed.

# Row Format:
# SE | PI L1 < PI L2 > PI L3 ¦ PI full mode

import os
import json
import re


class DictionaryGenerator:
    def __init__(self):
        corpus_folder = 'corpora'
        corpus_files = ['corpus_1000.txt',
                        'corpus_misc.txt', 'corpus_auto.txt']
        pi_dictionary = {}

        for file_name in corpus_files:
            file_path = os.path.join(corpus_folder, file_name)
            lines = self.read_corpus_file(file_path)
            if lines:
                word_entries = self.process_corpus_data(lines)
                pi_dictionary.update(word_entries)

        try:
            with open('dict/pi_dictionary.json', 'w', encoding='utf-8') as json_file:
                json.dump(pi_dictionary, json_file,
                          indent=4, ensure_ascii=False)
            print(
                "Dictionary updated successfully. Result file written to 'dict/pi_dictionary.json'")
        except IOError as e:
            print(f"Error writing to file 'dict/pi_dictionary.json.json': {e}")

    def read_corpus_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return []

    def extract_pi_parts(self, pi_string):
        # Split the string and ensure all PI parts are present
        pi_parts = re.split(r' < | > | ¦ ', pi_string)
        while len(pi_parts) < 4:
            pi_parts.append(None)  # Append None for missing PI parts
        return pi_parts

    def handle_special_cases(self, pi_transcription, default):
        if pi_transcription in ['*', '**']:
            return default
        return pi_transcription if pi_transcription else None

    def process_corpus_line(self, line):
        sf = None
        whole_line = line.strip()

        sf_match = re.search(r'….*\{(.+?)\}', line)
        if sf_match:
            sf = sf_match.group(1)
            line = line.split('…')[0]

        parts = line.split('|')
        se_word = parts[0].strip()

        if len(parts) > 1:
            pi_transcriptions_parts = self.extract_pi_parts(parts[1].strip())
        else:
            pi_transcriptions_parts = [se_word, None,
                                       None, None]  # Default to SE word

        pi_entry = {
            "L1": self.handle_special_cases(pi_transcriptions_parts[0], se_word),
            "L2": self.handle_special_cases(pi_transcriptions_parts[1], pi_transcriptions_parts[0] or se_word),
            "L3": self.handle_special_cases(pi_transcriptions_parts[2], pi_transcriptions_parts[0] or se_word),
            "FM": self.handle_special_cases(pi_transcriptions_parts[3], pi_transcriptions_parts[1] or pi_transcriptions_parts[0] or se_word)
        }

        return se_word, {"whole": whole_line, "PI": pi_entry, "Sf": sf}

    def process_corpus_data(self, lines):
        word_entries = {}
        skip_section = False
        for line in lines:
            if "::::::::::" in line.strip():
                skip_section = not skip_section
                continue

            if skip_section or not line.strip():
                continue

            se_word, word_entry = self.process_corpus_line(line)
            if se_word not in word_entries:
                word_entries[se_word] = word_entry

        return word_entries

    # def update_dictionary(self):
        # Additional method to handle the overall process of updating the dictionary
        # This might involve calling the above methods in a specific sequence
