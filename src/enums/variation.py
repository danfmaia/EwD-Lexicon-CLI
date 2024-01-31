from enum import Enum

from dict.preliminary_replacements import PRELIMINARY_REPLACEMENTS


class Variation(Enum):
    L1 = 0
    L2 = 1
    L3 = 2
    FM = 3

    def get_dict(self) -> dict[str, str]:
        """
        Get a PI Variation dictionary based on the PI Variation enum
        """
        try:
            variation_index = self.value
            variation_dict: dict[str, str] = {}
            for se_word, values in PRELIMINARY_REPLACEMENTS.items():
                variation_dict[se_word] = values[variation_index]
            return variation_dict
        except KeyError as exc:
            raise KeyError from exc

    # def get_word(self, se_word: str):
    #     """
    #     Retrieve a PI word of PRELIMINARY_REPLACEMENTS based on the SE word and Variation enum.
    #     """
    #     try:
    #         variation_index = self.value
    #         # type: ignore
    #         # type: ignore
    #         return PRELIMINARY_REPLACEMENTS[se_word][variation_index]
    #     except (KeyError, IndexError):
    #         return None
