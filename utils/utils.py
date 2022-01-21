import os
import sys

from definitions import DATA_DIR


def read_word_list_txt(filename):
    """Read all words in txt file, delimited by newline"""
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        words = f.read().splitlines()  # includes '\n' char
    return words


def get_input_escapable(prompt: str = None) -> str:
    """
    Get user input, checking for Keyboard interrupt and exiting if found
    :param prompt: str, prompt to print before input request
    :return: str
    """
    if prompt:
        print(prompt)
    try:
        result = input()
    except KeyboardInterrupt:
        print("Quitting app (ctrl-c)")
        sys.exit(1)
    return result
