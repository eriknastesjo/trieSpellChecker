#!/usr/bin/env python3
""" Module for testing Spellchecker"""

import unittest
import random
from src.trie import Trie
from src.exceptions import SearchMiss

class TestTrie(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """

    def setUp(self):
        """ Performed before every test """
        self.filename = "frequency.txt"
        with open(self.filename, "r", encoding='UTF-8') as file:
            dictionary = {}
            for readline in file:
                line_strip = readline.strip()
                list_line = line_strip.split()
                dictionary[list_line[0]] = list_line[1]

        self.my_trie = Trie(dictionary)
        random.seed("seed")

    def test_check_word_exists(self):
        """check_word() returns True using correct words"""
        self.assertEqual(self.my_trie.check_word("them"), True)
        self.assertEqual(self.my_trie.check_word("part"), True)
        self.assertEqual(self.my_trie.check_word("money"), True)
        self.assertEqual(self.my_trie.check_word("free"), True)

    def test_check_word_raise_error(self):
        """check_word() returns error 'SearchMiss' using uncorrect words"""
        with self.assertRaises(SearchMiss):
            self.assertEqual(self.my_trie.check_word("themm"), True)
            self.assertEqual(self.my_trie.check_word("partt"), True)
            self.assertEqual(self.my_trie.check_word("moneyy"), True)
            self.assertEqual(self.my_trie.check_word("freee"), True)

    def test_autofill_does_contain(self):
        """autofill() contains correct suggestions"""
        self.assertIn("hard", self.get_tup_first(self.my_trie.autofill("har")))
        self.assertIn("hardly", self.get_tup_first(self.my_trie.autofill("har")))
        self.assertIn("harder", self.get_tup_first(self.my_trie.autofill("har")))
        self.assertIn("service", self.get_tup_first(self.my_trie.autofill("ser")))
        self.assertIn("mercy", self.get_tup_first(self.my_trie.autofill("mer")))
        self.assertIn("during", self.get_tup_first(self.my_trie.autofill("dur")))

    def test_autofill_does_not_contain(self):
        """autofill() does not contain incorrect suggestions"""
        self.assertNotIn("have", self.my_trie.autofill("hard"))
        self.assertNotIn("soft", self.my_trie.autofill("soften"))
        self.assertNotIn("harq", self.my_trie.autofill("har"))
        self.assertNotIn("ser", self.my_trie.autofill("ser"))
        self.assertNotIn("me", self.my_trie.autofill("mer"))
        self.assertNotIn("you", self.my_trie.autofill("your"))

    def test_get_all_words(self):
        """get_all_words() returns list of words"""
        with open(self.filename, "r", encoding='UTF-8') as file:
            list_compare = []
            for readline in file:
                line_strip = readline.strip()
                list_line = line_strip.split()
                list_compare.append(list_line[0])
            list_compare.sort()
            list_trie_words = self.my_trie.get_all_words()
            check = all(item in list_compare for item in list_trie_words)
            self.assertTrue(check)

    def test_remove_word_exists(self):
        """remove() removes word that exists"""
        self.assertIn("earth", self.my_trie.get_all_words())
        self.assertIn("spoke", self.my_trie.get_all_words())
        self.assertIn("important", self.my_trie.get_all_words())
        self.my_trie.remove_word("earth")
        self.my_trie.remove_word("spoke")
        self.my_trie.remove_word("important")
        self.assertNotIn("earth", self.my_trie.get_all_words())
        self.assertNotIn("spoke", self.my_trie.get_all_words())
        self.assertNotIn("important", self.my_trie.get_all_words())

    def test_remove_word_not_exist(self):
        """remove() raises error when word does not exist"""
        with self.assertRaises(SearchMiss):
            self.my_trie.remove_word("earthh")
            self.my_trie.remove_word("marvin")
            self.my_trie.remove_word("worf")

    @staticmethod
    def get_tup_first(list_tup):
        """returns list with only the first element in each tuple"""
        tup_first = []
        for tup in list_tup:
            tup_first.append(tup[0])
        return tup_first
