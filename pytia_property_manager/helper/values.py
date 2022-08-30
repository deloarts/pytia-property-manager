"""
    Helper functions for value related functions.
"""

from string import ascii_lowercase, ascii_uppercase
from tkinter import StringVar, ttk

from pytia.exceptions import PytiaValueError


def increase_revision(variable: StringVar) -> None:
    """
    Increases the revision of the given version variable.

    Args:
        variable (StringVar): The variable that holds the version, must be a number or a letter.

    Raises:
        NotImplementedError: Raised if the version exceeds the letter Z.
        NotImplementedError: Raised if the version exceeds the letter z.
        PytiaValueError: Raised if the variable is not a number or letter.
    """
    value = variable.get()
    if value.isnumeric():
        variable.set(str(int(value) + 1))
    elif value in ascii_uppercase:
        if value == "Z":
            raise NotImplementedError
        variable.set(ascii_uppercase[ascii_uppercase.index(value) + 1])
    elif value in ascii_lowercase:
        if value == "z":
            raise NotImplementedError
        variable.set(ascii_lowercase[ascii_lowercase.index(value) + 1])
    else:
        raise PytiaValueError(f"Cannot increase revision value {value}")
