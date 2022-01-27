import argparse
import re
from typing import List, Union

from utils import get_input_escapable
from wordle_helper.word_list import WordList, find_first_guess, sort_by_letter_freq


class WordleFilters:
    def __init__(self, is_verbose=False):
        self.word_list_full = WordList().words
        self.is_verbose = is_verbose

    def run_iter(self, excluded_letters: str, positioned_letters: str, unpositioned_letters: Union[str, List[str]]):
        """
        Given the selected letters, run the filters and get the possible remaining words
        :param excluded_letters: str, the list of letters that have already been used that don't match
        :param positioned_letters: str, a RegEx that declares the position of known letters.
            '.' is a placeholder for any unknown letter, eg "..RE."
        :param unpositioned_letters: str or List of str, containing letters that are in the word but in the wrong position
        :return: list of possible remaining words
        """

        if isinstance(unpositioned_letters, list):
            # just take the first one, deal with the position history later
            unpositioned_letters = unpositioned_letters[0]

        initial_words = self.word_list_full.copy()
        words_excludeltr = self.check_excluded_letters(initial_words, excluded_letters)
        words_positionchr = self.check_positioned_letters(words_excludeltr, positioned_letters)
        words_knownltrs = self.check_unpositioned_letters(words_positionchr, unpositioned_letters)
        result = words_knownltrs  # end of the filter pipe

        return result

    def run_iter_cli(self):
        """
        Run a single iteration of a guess
        :return: list of possible words
        """
        initial_words = self.word_list_full

        # get the user input for letters to exclude
        excluded_letters = get_input_escapable("What letters are excluded?")
        if not excluded_letters:
            words_excludeltr = initial_words
        else:
            words_excludeltr = self.check_excluded_letters(initial_words, excluded_letters)
            print(f"Found {len(words_excludeltr)}/{len(initial_words)}")
            if self.is_verbose:
                print(words_excludeltr)

        positioned_letters = get_input_escapable("What letters are known in position? (enter dot as placeholder, eg '.A.ER')")
        if not positioned_letters:
            words_positionchr = words_excludeltr
        elif len(positioned_letters) != 5:
            print(f"Bad length, got '{positioned_letters}'")
            words_positionchr = words_excludeltr
            # continue
        else:
            words_positionchr = self.check_positioned_letters(words_excludeltr, positioned_letters)
            print(f"Found {len(words_positionchr)}/{len(words_excludeltr)}:")
            if self.is_verbose:
                print(words_positionchr)

        # NOTE: listing the word like this will not be able to use prior history of incorrect positions
        # TODO: figure out how to add history
        unpositioned_letters = get_input_escapable("What letters are known and NOT in position? (enter as '.OR..'")
        if not unpositioned_letters:
            words_knownltrs = words_positionchr
        elif len(unpositioned_letters) != 5:
            print(f"Bad length, got '{unpositioned_letters}'")
            words_knownltrs = words_positionchr
            # continue
        else:
            words_knownltrs = self.check_unpositioned_letters(words_positionchr, unpositioned_letters)
            print(f"Found {len(words_knownltrs)}/{len(words_positionchr)}")

        # update the result
        result = words_knownltrs
        print(f"Found {len(result)} word hits")
        if len(result)/len(initial_words) < 0.2 or self.is_verbose:
            result = wordle_filt.sort_by_letter_freq(result)
            print(result)
        else:  # too many words!
            print("Found too many words!")

        return result

    @staticmethod
    def check_excluded_letters(words: List[str], exclude: str) -> List[str]:
        """
        Filter the given `words` list from containing any of the letters in exclude
        :param words: list of words
        :param exclude: string, a list of letters that are not found in the target word
        :return: List with remaining words
        """
        match_str = f"[^{exclude.lower()}]"
        exclude_matcher = re.compile(match_str)
        matches = [exclude_matcher.findall(w) for w in words]
        word_matches = [w for w, match in zip(words, matches) if len(match) == 5]
        return word_matches

    @staticmethod
    def check_positioned_letters(words: List[str], positioned_letters: str) -> List[str]:
        """
        Check the wordlist to see which words have a letter in the target position

        :param words: list of words
        :param positioned_letters: str, regex format using '.' to mark any unknown positions
            eg: "..G.Y"
        :return: list with remaining words
        """
        positioned_matcher = re.compile(positioned_letters.lower())
        matches = [positioned_matcher.findall(w) for w in words]
        word_matches = [m[0] for m in matches if len(m) > 0]
        return word_matches

    @staticmethod
    def check_unpositioned_letters(words: List[str], unpositioned_letters: str) -> List[str]:
        """
        Check the given wordlist to see which words have the given letters, but not in the given position
        :param words: list of words
        :param unpositioned_letters: str, regex format using '.' to mark any unknown positions
            eg: "..G.Y"
            NOTE: this will change once i add a unpositioned history
        :return:  list with remaining words
        """
        # This is a bit harder.
        # Write a regex to exclude the target letters in a given position, AND include them elsewhere
        # first find all words that do not have letters in the given positions
        match_str = re.sub(r"(\w)", r"[^\g<1>]", unpositioned_letters)
        not_there_matcher = re.compile(match_str)
        matches = [not_there_matcher.findall(w) for w in words]
        word_matches = [w for w, match in zip(words, matches) if len(match) != 0]

        # then only keep the words that has ALL the unpositioned letters
        find_letters = unpositioned_letters.replace(".", "").lower()
        matches = [all([ltr in word for ltr in find_letters]) for word in words]
        has_letters_matches = [w for w, match in zip(words, matches) if match]
        # keep via intersection
        final_matches = list(set(word_matches).intersection(set(has_letters_matches)))
        return final_matches

    @staticmethod
    def sort_by_letter_freq(words, common_first=True):
        """
        Sort the given list of words by the summed letter frequencies
        :param words: List[str] word strings
        :param common_first: sort by common first. If False, sort by rare first
        :return: sorted word strings
        """
        return sort_by_letter_freq(words, common_first=common_first)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Display all words always")
    args = parser.parse_args()
    is_verbose = args.verbose

    wordle_filt = WordleFilters()

    print("#########################")
    print("      Wordle Helper      ")
    print("#########################")

    first_guess = find_first_guess()
    first_guess = wordle_filt.sort_by_letter_freq(first_guess)
    print("Possible first word guesses, by unique vowel count:")
    print(first_guess)
    print()

    loop_check = True
    iter_ctr = 1
    result = None
    while loop_check:
        print(f"*** Wordle Helper [iter {iter_ctr}]***")
        iter_ctr += 1
        result = wordle_filt.run_iter_cli()

    if len(result) == 0:
        print("No known solutions, you messed up somewhere in your letter entering. Or bad dictionary.")
    elif len(result) == 1:
        print(f">>> {result.upper()}")
    else:
        print("How'd you get here?")

