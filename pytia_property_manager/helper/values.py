"""
    Helper functions for value related functions.
"""

from copy import deepcopy
from string import ascii_lowercase
from string import ascii_uppercase
from tkinter import StringVar

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


def interpolate_colors(
    source_color: tuple, target_color: tuple, factor: float
) -> tuple:
    """Interpolates two colors (naive interpolation).

    Args:
        source_color (tuple): The source color.
        target_color (tuple): The interpolation target.
        factor (float): The interpolation factor.

    Returns:
        tuple: The interpolated color.
    """
    # source: a, target: b
    return tuple(int(a + (b - a) * factor) for a, b in zip(source_color, target_color))


def get_perceived_brightness(rgb: tuple) -> float:
    """Returns the perceived brightness of a given RGB value using ITU BT.709.

    Args:
        rgb (tuple): The RGB value from which to get the perceived brightness.

    Returns:
        float: The perceived brightness.
    """
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def set_perceived_brightness(rgb: tuple, brightness: float) -> tuple:
    """Set the perceived brightness from the given RGB value to at least the given value.
    If the perceived brightness from the RGB value is equal or brighter that the given
    brightness value, no changes will be made.

    Args:
        rgb (tuple): The rgb value to brighten up.
        brightness (float): The minium brightness level.

    Returns:
        tuple: The brightened up rgb value.
    """

    color = deepcopy(rgb)
    y = get_perceived_brightness(rgb)
    t = 0

    while y < brightness and t <= 255:
        color = interpolate_colors(
            source_color=rgb, target_color=(255, 255, 255), factor=t / 255
        )
        y = get_perceived_brightness(color)
        t += 1

    return color
