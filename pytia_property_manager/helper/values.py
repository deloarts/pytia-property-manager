"""
    Helper functions for value related functions.
"""

from string import ascii_lowercase, ascii_uppercase
from tkinter import StringVar, ttk

from pytia.exceptions import PytiaValueError


def get_new_revision(variable: StringVar) -> str:
    """
    Increases the revision of the given version variable. Does not manipulate the variable itself.

    Args:
        variable (StringVar): The variable that holds the current version, \
            must be a number or a letter.

    Raises:
        NotImplementedError: Raised if the version exceeds the letter Z.
        NotImplementedError: Raised if the version exceeds the letter z.
        PytiaValueError: Raised if the variable is not a number or letter.

    Returns:
        str: The version of the new revision.
    """
    value = variable.get()
    if value.isnumeric():
        return str(int(value) + 1)
    elif value in ascii_uppercase:
        if value == "Z":
            raise NotImplementedError
        return ascii_uppercase[ascii_uppercase.index(value) + 1]
    elif value in ascii_lowercase:
        if value == "z":
            raise NotImplementedError
        return ascii_lowercase[ascii_lowercase.index(value) + 1]
    raise PytiaValueError(f"Cannot increase revision value {value}")
