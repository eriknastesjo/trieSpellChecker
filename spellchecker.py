#!/usr/bin/env python3
"""
Menu for Dictionary
"""

import inspect
import sys
from src.exceptions import SearchMiss
from src.trie import Trie



class SpellChecker():
    """
    Class SpellChecker with Menu
    """

    def __init__(self):
        """ Constructor """
        self._image = r"""
                  _        _        _        __       __       _
        /\       |_)      /        | \      |_       |_       /        |_|
       /--\      |_)      \_       |_/      |__      |        \_?      | |

        """

        with open("frequency.txt", "r", encoding='UTF-8') as file:
            dictionary = {}
            for readline in file:
                line_strip = readline.strip()
                list_line = line_strip.split()
                dictionary[list_line[0]] = list_line[1]

        self.trie = Trie(dictionary)
        self._options = {
            "1": "check_word",
            "2": "autofill",
            "3": "new_dict",
            "4": "print_all",
            "5": "remove_word",
            "6": "quit"
        }


    ### MENU OPTION METHODS ###

    def check_word(self):
        """
        Check a word
        """
        word_to_check = input("Enter a word to look up in dictionary: ")
        word_to_check = word_to_check.lower()
        try:
            self.trie.check_word(word_to_check)
            print("\nword is spelled correctly")
        except SearchMiss:
            print("\nword does not exist")
        self.any_key_to_continue()

    def autofill(self):
        """
        Get word suggestions based on prefix
        """
        prefix = input("\nFirst enter three letter, then one letter at a time: ")
        list_suggestions = self.trie.autofill(prefix)
        self.autofill_print(list_suggestions)
        while True:
            prefix += input("\nEnter another letter or type 'quit': ")
            if "quit" in prefix:
                break
            list_suggestions = self.trie.autofill(prefix)
            self.autofill_print(list_suggestions)
        self.any_key_to_continue()

    @staticmethod
    def autofill_print(list_tuples):
        """
        Help function to print out suggestions in autofill
        """
        for tup in list_tuples:
            print(f"{tup[0]} {tup[1]}")

    def print_all(self):
        """
        Print out all words
        """
        list_print = self.trie.get_all_words()
        for word in list_print:
            print(word)
        self.any_key_to_continue()

    def new_dict(self):
        """
        Choose a new dictionary
        """
        new_dictionary_file_name = input("\nFile name: ")
        with open(new_dictionary_file_name, "r", encoding='UTF-8') as file:
            dictionary = {}
            for readline in file:
                line_strip = readline.strip()
                list_line = line_strip.split()
                dictionary[list_line[0]] = list_line[1]
        self.trie = Trie(dictionary)

    def remove_word(self):
        """
        Remove word from dictionary
        """
        try:
            self.trie.remove_word(input("\nWord to delete: "))
        except SearchMiss:
            print("word is missing")
        self.any_key_to_continue()

    ### MAIN ###

    def main(self):
        """
        Main
        """
        while True:
            print(self._image)
            self._print_menu()
            choice = input("--> ")
            try:
                self._get_method(choice)()
            except KeyError:
                input("Invalid choice! \n[Enter] to try again")

    def _print_menu(self):
        """
        Use docstring from methods to print options for the program
        https://docs.python.org/3/library/inspect.html#inspect.getdoc
        """
        menu = "*** ERIKS DICTIONARY ***\n-------------------------\n"
        # loop over all options in dictionary
        for key in self._options:
            # Use _get_method to dynamically get method
            method = self._get_method(key)
            # Use getdoc to get docstring from method
            docstring = inspect.getdoc(method)

            # format meny choice text
            menu += f"{key}) {docstring}\n"

        print(menu)

    def _get_method(self, method_name):
        """
        Use function getattr() to dynamically get value of an attribute.
        https://docs.python.org/3.7/library/functions.html#getattr
        If attribute is a method, a reference to the method is returned.
        For an example, https://www.journaldev.com/16146/python-getattr
        """
        return getattr(self, self._options[method_name])

    @staticmethod
    def any_key_to_continue():
        """ Waiting for input before continue """
        input("Press [any key] to continue: ")

    def quit(self):
        """
        Quit
        """
        self._image = r"""
   _O/
     \
     /\_
     \  `
     `
        """
        print(self._image)
        sys.exit()


if __name__ == "__main__":
    s = SpellChecker()
    s.main()
