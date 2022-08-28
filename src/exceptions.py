"""
Custom exception module
"""


# Inehrits from built in python class Exception
class Error(Exception):
    """User defined class for custom exceptions"""

# With this I can NAME my own exception handler (otherwise things are the same)
class SearchMiss (Error):
    """Raised when value does not exist"""
