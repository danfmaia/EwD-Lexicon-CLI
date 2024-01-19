import json


class Dictionary:
    def __init__(self, excluded_list):
        """
        Load the PI dictionary, excluding a list of word.
        """
        with open('dict/pi_dictionary.json', 'r') as file:
            pi_dictionary = json.load(file)

        if excluded_list:
            # Remove excluded words
            for word in excluded_list:
                pi_dictionary.pop(word, None)

        self.pi_dictionary = pi_dictionary

    def lookup_pi_entry(self, word):
        """
        Look up the PI dictionary entry for the given word.
        """
        word_lower = word.lower()
        if word_lower in self.pi_dictionary:
            return self.pi_dictionary[word_lower]
        return None
