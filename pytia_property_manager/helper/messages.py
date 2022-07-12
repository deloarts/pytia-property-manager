"""
    Helper functions for messages.
"""

import webbrowser
from tkinter import messagebox as tkmsg
from typing import List, Optional

from resources import resource


def show_help() -> None:
    """Opens the help docs."""
    if url := resource.settings.urls.help:
        webbrowser.open_new(url)
    else:
        tkmsg.showinfo(
            title=resource.settings.title,
            message="Your administrator did not provide a help page for this app.",
        )


def datafield_message(messages: List[str], critical: bool) -> Optional[str]:
    """
    Message helper for datafield warnings. Use for the ok button.
    Shows a question-warning for the user to interact with.

    Args:
        messages (List[str]): The list of warnings or errors.
        critical (bool): Show the message as critical, doesn't ask a question.

    Returns:
        Optional[str]: True if the question was answered with yes, False otherwise.
    """
    if len(messages) == 1:
        msg = messages[0]
    else:
        output = "\n - ".join(messages)
        msg = f"Some data fields are not set properly:\n\n - {output}"

    if critical:
        tkmsg.showerror(message=msg)
        return None

    return tkmsg.askquestion(message=f"{msg}\n\nProceed anyway?", icon="warning")
