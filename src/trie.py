"""
Module for Trie class
"""

from src.node import Node
from src.exceptions import SearchMiss

class Trie():
    """
    Class Trie
    """
    def __init__(self, dictionary = None):
        """ Constructor """
        self.root = Node()
        for word, frequency in dictionary.items():
            self.insert_word(word, frequency)

    def insert_word(self, word, frequency):
        """ Insert word in dictionary """
        n = 0
        current_node = self.root
        while True:
            current_letter = word[n]
            if current_letter not in current_node:
                current_node[current_letter] = Node(current_letter)
            current_node = current_node[current_letter]
            n += 1
            if n == len(word):
                current_node.set_is_end(True, frequency)
                break

    def check_word(self, word):
        """ Check if word exists in dictionary """
        current_node = self.root
        n = 0
        while True:
            current_letter = word[n]
            if current_letter in current_node:
                current_node = current_node[current_letter]
                if n == len(word) - 1:
                    if current_node.check_is_end():
                        return True
                    break
                n += 1
            else:
                break
        raise SearchMiss

    def autofill(self, prefix):
        """ Shows suggestions based on prefix """
        try:
            start_node = self.find_end_node(prefix)
        except SearchMiss:
            return {}
        dict_words = {}
        self.req_find_words_to_dict(start_node, prefix, dict_words, False)

        list_tuples = []
        for key, value in dict_words.items():
            list_tuples.append((float(value), key))
        list_tuples.sort(reverse=True)  # tupler sorteras på första elementet

        count = 0
        list_return = []
        while count < 10 and count < len(list_tuples):
            list_return.append((list_tuples[count][1], list_tuples[count][0]))
            count += 1
        return list_return

    def find_end_node(self, word):
        """ Finding end node of word"""
        current_node = self.root
        n = 0
        while True:
            current_letter = word[n]
            if current_letter in current_node:
                current_node = current_node[current_letter]
                if n != len(word) - 1:
                    n += 1
                else:
                    return current_node
            else:
                raise SearchMiss

    def req_find_words_to_dict(self, current_node, prefix_so_far, dict_words, include_letter):
        """ Reqursive method for autofill() and get_all_words() """

        if include_letter:   # excludes first nodes letter
            prefix_so_far += current_node.get_letter()

        if current_node.check_is_end():
            dict_words[prefix_so_far] = current_node.get_frequency()

        # basfall
        if current_node.has_paths() is False:
            return

        # rekursion
        for path in current_node.get_all_paths():
            self.req_find_words_to_dict(current_node[path], prefix_so_far, dict_words, True)


    def get_all_words(self):
        """ Returns all word in dictionary """
        list_words = []
        self.req_find_words_to_list(self.root, "",list_words, False)
        # list_words.sort()     # istället används egengjord merge sort
        self.req_merge_sort(list_words)
        return list_words

    def req_find_words_to_list(self, current_node, prefix_so_far, list_words, include_letter):
        """ Reqursive method for autofill() and get_all_words() """
        if include_letter:   # excludes first nodes letter
            prefix_so_far += current_node.get_letter()

        if current_node.check_is_end():
            list_words.append(prefix_so_far)

        # basfall
        if current_node.has_paths() is False:
            return

        # rekursion
        for path in current_node.get_all_paths():
            self.req_find_words_to_list(current_node[path], prefix_so_far, list_words, True)

    def remove_word(self, word):
        """ Remove word from dictionary """
        self.req_remove(self.root, word, 0)

    def req_remove(self, current_node, word, n):
        """ Reqursive method for remove_word() """
        if n == len(word):
            if current_node.check_is_end():
                current_node.set_is_end(False)
                return
            raise SearchMiss
        current_letter = word[n]
        if current_letter in current_node:
            n += 1
            self.req_remove(current_node[current_letter], word, n)
            if current_node[current_letter].has_paths() is False:
                del current_node[current_letter]
        else:
            raise SearchMiss

    def req_merge_sort(self, list_to_sort):
        """ Reqursive method to merge sort a list """
        if len(list_to_sort) > 1:
            # listorna är beständiga och följer således
            # med och omdefinieras under det rekursiva förloppet
            # (behöver ej därför returnera)
            list_left = list_to_sort[:len(list_to_sort)//2]
            list_right = list_to_sort[len(list_to_sort)//2:]
            # print(f"list_to_sort: {list_to_sort}")
            # print(f"list_left: {list_left}")
            # print(f"list_right: {list_right}")

            # rekursion
            self.req_merge_sort(list_left)
            self.req_merge_sort(list_right)

            # merge
            self.merge(list_to_sort, list_left, list_right)

    @staticmethod
    def merge(list_to_sort, list_left, list_right):
        """ Help method for merging list """
        # print(f"now merge: list_to_sort({list_to_sort}), left({list_left}), right({list_right})" )
        i = 0 # left list index
        j = 0 # right list index
        k = 0 # merge list index
        while i < len(list_left) and j < len(list_right):
            if list_left[i] < list_right[j]:
                list_to_sort[k] = list_left[i]
                i += 1
            else:
                list_to_sort[k] = list_right[j]
                j += 1
            k += 1

        # utifall j >= len(list_right)
        # dvs inga fler kvar i höger
        # men fortfarande kvar i vänster
        while i < len(list_left):
            # återstående är redan sorterade
            # så vi lägger bara till dem en efter en
            list_to_sort[k] = list_left[i]
            i += 1
            k += 1

        # samma som ovan fast om det är
        # i >= len(list_left)
        while j < len(list_right):
            list_to_sort[k] = list_right[j]
            j += 1
            k += 1
