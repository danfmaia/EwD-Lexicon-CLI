# pylint: disable=missing-module-docstring

from typing import Dict, List

# TODO: add L2, L3 and FM words (only L1 words are correct)
PRELIMINARY_REPLACEMENTS: Dict[str, List[str]] = {
    'the': ['the̬', 'the̬', 'the', 'the̬'],
    'a': ['a̬', 'a̬', 'a', 'a̬'],
    'an': ['a̬n', 'a̬n', 'an', 'a̬n'],
    'of': ['o̬‹v›', 'o̬‹v›', 'of', 'o̬‹v›'],
    'to': ['to̬', 'to̬', 'to', 'to̬'],
    'you': ['yöu', 'yöu', 'yöu', 'yöu'],
    'your': ['yöur', 'yöur', 'yöur', 'yöur'],
    'this': ['this̩', 'this̩', 'this̩', 'this̩'],
    'and': ['and', 'and', 'and', 'and'],
    'for': ['for', 'for', 'for', 'for'],
    'from': ['fro̬m', 'fro̬m', 'from', 'fro̬m'],
    # alphabetical order
    'been': ['be͝en', 'be͝en', 'be͝en', 'be͝en'],
}
