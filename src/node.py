"""
Module for Node Class
"""

class Node():
    """
    Class Node
    """
    def __init__(self, letter = None):
        """ Constructor """
        self.letter = letter
        self.paths = {}
        self.is_end = False
        self.frequency = None

    def get_letter(self):
        """ Returns letter that node represents """
        return self.letter

    def get_frequency(self):
        """ Returns frequency value """
        return self.frequency

    def get_all_paths(self):
        """ Returns all paths, eg. children nodes """
        return self.paths

    def has_paths(self):
        """ Returns true if node has paths, else false """
        return bool(self.paths)

    def check_is_end(self):
        """ Returns true if node is marked as end of word """
        return self.is_end

    def set_is_end(self, value, frequency = None):
        """ Set the value of bool 'is_end' """
        if frequency:
            self.frequency = frequency
        self.is_end = value

    def __str__(self):
        """ Override function """
        list_path_keys = ""
        for key in self.paths:
            list_path_keys.join(key)
        return f"letter {self.letter}, paths: {list_path_keys}, is_end: {self.is_end}"

    def __getitem__(self, key):
        """ Override function """
        return self.paths[key]

    def __setitem__(self, key, value):
        """ Override function """
        self.paths[key] = value

    def __contains__(self, key):
        """ Override function """
        return key in self.paths

    # def __iter__(self):  # Är denna rätt???
    #     """ Override function """
    #     iter(self.paths)

    def __delitem__(self, key):
        """ Override function """
        self.paths.pop(key)
