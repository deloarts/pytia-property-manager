"""
    Helper functions for translations.
"""

from const import Source
from pytia.exceptions import PytiaValueError
from resources import resource


def translate_source(value: int | str) -> str | int:
    """
    Converts the source to the CATIA source integer.

    Args:
        value (int | str): If an integer is given, the name will be returned. If a string is given \
            the corresponding CATIA source number will be returned. If

    Raises:
        PytiaValueError: Raised when the source number is invalid.
        PytiaValueError: Raised when the source name is invalid.

    Returns:
        str | int: The source, string or int, depending on the input.
    """
    if isinstance(value, int):
        match value:
            case 0:
                return Source.UNKNOWN.value
            case 1:
                return Source.MADE.value
            case 2:
                return Source.BOUGHT.value
            case _:
                raise PytiaValueError(
                    f"Source value error: Cannot translate {value} to a CATIA source name."
                )
    else:
        match value:
            case Source.UNKNOWN.value:
                return 0
            case Source.MADE.value:
                return 1
            case Source.BOUGHT.value:
                return 2
            case _:
                raise PytiaValueError(
                    f"Source value error: Cannot translate {value} to a CATIA source number."
                )


def translate_nomenclature(source: int | str) -> str:
    """
    Translates the nomenclature depending on the given source.

    Args:
        source (str): The CATIA source name or number.

    Raises:
        PytiaValueError: Raised when the source is not valid.

    Returns:
        str: The nomenclature depending on the source.
    """
    match source:
        case Source.UNKNOWN.value | 0:
            return ""
        case Source.MADE.value | 1:
            return resource.settings.nomenclature.made
        case Source.BOUGHT.value | 2:
            return resource.settings.nomenclature.bought
        case _:
            raise PytiaValueError(
                f"Source value error: Cannot translate {source} to a valid nomenclature."
            )
