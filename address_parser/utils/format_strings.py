from typing import Iterable


def remove_special_characters(s: str) -> str:
    """
    Removes special characters from input string

    :param s: Input String
    :type s: str
    :return: Cleansed String
    :rtype: str
    """
    return s.upper().replace('.', '')


def tokenize(s: str) -> Iterable:
    """
    Tokenizes input string

    :param s: Input String
    :type s: str
    :return: iterable of tokens
    :rtype: Iterable
    """
    cleansed_addr = remove_special_characters(s)
    return iter(cleansed_addr.split()[::-1])
