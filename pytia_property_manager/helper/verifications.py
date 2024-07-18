"""
    Helper functions for verifying functions.
"""

from tkinter import StringVar
from typing import Literal
from urllib.parse import urlparse

from app.layout import Layout
from app.widgets.processes import ProcessWidgets
from const import VERIFY_CRITICAL
from const import VERIFY_WARNING


def verify_variable(
    critical: list,
    warning: list,
    variable: StringVar,
    settings_verification: Literal["critical", "warning"] | None,
    msg: str,
) -> None:
    if settings_verification is not None and not variable.get():
        if settings_verification == VERIFY_CRITICAL:
            critical.append(msg)
        elif settings_verification == VERIFY_WARNING:
            warning.append(msg)


def verify_process(
    critical: list,
    warning: list,
    process_id: int,
    settings_verification: Literal["critical", "warning"] | None,
    layout: Layout,
    msg: str,
) -> None:
    if (
        settings_verification is not None
        and not layout.processes.get(process_id).process_var.get()
    ):
        if settings_verification == VERIFY_CRITICAL:
            critical.append(msg)
        elif settings_verification == VERIFY_WARNING:
            warning.append(msg)


def verify_url(url: str) -> bool:
    try:
        result = urlparse(url=url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
