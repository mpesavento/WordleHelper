"""
Tools for creating the output 5 letter word dictionary
"""
import os
from definitions import DATA_DIR
from utils import read_word_list_txt

TARGET_LEN = 5  # target number of characters in selected words


class ConvertWordList:
    def __init__(self, word_length=TARGET_LEN):
        self.target_length = word_length
        self.word_list = None

    @staticmethod
    def load_full_dictionary():
        """Load the full original dictionary from /data """
        return read_word_list_txt("words_alpha.txt")

    def filter_word_lengths(self, target_length):
        return list(filter(lambda w: len(w) == target_length, self.word_list))

    def write_filtered_list(self):
        self.word_list = self.load_full_dictionary()
        filtered_words = self.filter_word_lengths(self.target_length)
        with open(os.path.join(DATA_DIR, f"words_alpha_{TARGET_LEN}.txt"), "w") as f:
            f.write('\n'.join(filtered_words))


if __name__ == "__main__":
    ConvertWordList().write_filtered_list()
