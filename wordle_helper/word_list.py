import os
import csv

from utils import read_word_list_txt
from definitions import DATA_DIR

VOWELS = list("aeiou")


class WordList:
    DEFAULT_DICTIONARY_FILENAME = "words_alpha_5.txt"

    def __init__(self):
        self.words = read_word_list_txt(self.DEFAULT_DICTIONARY_FILENAME)

    def get_vowel_counts(self):
        """
        Get a nested dict per word with vowel counts and unique vowel counts for each word
        :return: Dict[str, Dict[str, int]]
            A dictionary with each word as the key, and the value with a dict of various vowel counts
        """
        word_dict = {}
        for w in self.words:
            word_dict[w] = {}
            vowel_ct = {ltr: w.count(ltr) for ltr in VOWELS}
            word_dict[w]["vowel_ct"] = vowel_ct
            word_dict[w]["unique_vowel_ct"] = sum([c > 0 for c in vowel_ct.values()])
        return word_dict


class LetterFrequencies:
    DEFAULT_LETTER_FREQ_FILENAME = "letter_frequency_en.csv"

    def __init__(self):
        self.letter_freq = self.load_letter_freq()

    def __getitem__(self, item: str):
        """Get the letter frequency by letter"""
        return self.letter_freq[item.lower()]

    def load_letter_freq(self) -> dict:
        """
        Get the letter frequency from the given table
        :return: Dict[str, float], key=letter, value = decimal frequency ratio
        """
        ltr_freq = {}
        with open(os.path.join(DATA_DIR, self.DEFAULT_LETTER_FREQ_FILENAME), "r") as csvfile:
            content = csv.DictReader(csvfile, fieldnames=["letter", "freq", "relative_ct"])
            for i, row in enumerate(content):
                if i == 0:
                    # header row, continue
                    continue
                ltr_freq[row["letter"].lower()] = float(row["freq"])
        return ltr_freq

    def sum_letter_freq(self, word: str):
        return sum([self.letter_freq[ltr] for ltr in list(word)])


def sort_by_letter_freq(words, common_first=True):
    """
    Sort the given list of words by the summed letter frequencies
    :param words: List[str] word strings
    :param common_first: sort by common first. If False, sort by rare first
    :return: sorted word strings
    """
    ltr_freq = LetterFrequencies()
    word_sum_freq = [(word, ltr_freq.sum_letter_freq(word)) for word in words]
    words_out = sorted(word_sum_freq, key=lambda x: x[1], reverse=common_first)
    return [w[0] for w in words_out]


def find_first_guess() -> list:
    """
    What's a good first guess? Probably something with a lot of vowels!

    :return: list, words returned from the target filter, sorted by decreasing letter frequency sum
    """
    word_list = WordList()

    # first attempt: what word has the most vowels in it?
    word_dict = word_list.get_vowel_counts()
    # find the word with the most unique vowels
    max_vowel = 0
    for w, v in word_dict.items():
        if v["unique_vowel_ct"] > max_vowel:
            max_vowel = v["unique_vowel_ct"]
    best_starters = [w for w, v in word_dict.items() if v["unique_vowel_ct"] == max_vowel]
    best_starters = sort_by_letter_freq(best_starters)
    return best_starters


if __name__ == "__main__":
    ltr_freq = LetterFrequencies()

