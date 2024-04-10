# pylint: disable=missing-module-docstring

from typing import Dict, List

PRELIMINARY_REPLACEMENTS: Dict[str, List[str]] = {
    'the': ['the̬', 'the̬', 'the', 'the̬'],
    'a': ['a̬', 'a̬', 'a', 'a̬'],
    'an': ['a̬n', 'a̬n', 'an', 'a̬n'],
    'of': ['o̬f', 'o̬f', 'of', 'o̬f'],
    'to': ['to̬', 'to̬', 'to', 'to̬'],
    'you': ['yöu', 'yöu', 'yöu', 'yöu'],
    'your': ['yöur', 'yöur', 'yöur', 'yöur'],
    'this': ['this̩', 'this̩', 'this̩', 'this̩'],
    'and': ['and', 'and', 'and', 'and'],
    'for': ['for', 'for', 'for', 'for'],
    'from': ['fro̬m', 'fro̬m', 'from', 'fro̬m'],
    # alphabetical order
    'been': ['be͝en', 'be͝en', 'be͝en', 'be͝en'],
    'was': ['was', 'wa̬s', 'wa̬s', 'was']
}
