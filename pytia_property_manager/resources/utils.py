"""
    Resource utilities.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import os
import re
import sys
from pathlib import Path
from tkinter import messagebox as tkmsg


def expand_env_vars(value: str, ignore_not_found: bool = False) -> str:
    """
    Expands windows environment variables.
    E.g.: Expands %ONEDRIVE%/foo/bar to "C:/Users/.../OneDrive/foo/bar

    The variable to replace must be between two percentage symbols.

    Terminates the app if the given value has a variable, that
    cannot be found in the system variables (and ignore_not_found is False),
    return the original value otherwise.
    """
    output = value
    filter_result = re.findall(r"\%(.*?)\%", value)
    for key in filter_result:
        if key in os.environ:
            output = value.replace(f"%{key}%", os.environ[key])  # type: ignore
        elif ignore_not_found:
            return value
        else:
            tkmsg.showerror(
                title="Environment Variables",
                message=(
                    f"The environment variable {key!r} is not set on your machine. "
                    "Depending on your system it may be required to setup the "
                    "environment variable in capitals only.\n\n"
                    "Please contact your system administrator."
                ),
            )
            sys.exit()
    return output


def create_path_symlink(path: Path, alway_apply_symlink: bool) -> str:
    """
    Replaces paths of the given path with the environment variable, if exists
    and the users agrees. Starts with the deepest folder and runs upwards.

    E.g.: Replaces `C:/Users/.../OneDrive/foo/bar` with `%ONEDRIVE%/foo/bar`

    The environment variable will be encapsuled within two percentage symbols.

    Return the original path if no symlink is found.
    """
    path_str = str(path)

    for parent in path.parents:
        for key, value in os.environ.items():
            if str(parent) == value:
                symlinked = path_str.replace(str(parent), f"%{key}%")
                if alway_apply_symlink or tkmsg.askyesno(
                    title="Symlink has been found.",
                    message=(
                        "A symlink has been found for the drawing documents path:\n"
                        f" - Path: {str(parent)!r}.\n"
                        f" - Symlink: {key!r}\n\n"
                        "Do you want to save the symlink to the linked documents path?\n\n"
                        "Depending on your choice, the following path will be written "
                        "to the linked document:\n"
                        f" - Yes: {symlinked!r}\n"
                        f" - No:  {path_str!r}"
                    ),
                ):
                    return symlinked
                else:
                    return path_str
    return path_str


def create_path_workspace_level(
    path: Path, workspace_folder: Path, always_apply_relative: bool
) -> str:
    path_str = str(path)
    workspace_folder_str = str(workspace_folder)

    if workspace_folder_str in path_str:
        relative_path = "." + path_str.split(workspace_folder_str)[-1]
        if always_apply_relative or tkmsg.askyesno(
            title="Workspace has been found.",
            message=(
                "A workspace file has been found for the drawing documents path:\n"
                f" - Workspace: {workspace_folder_str!r}.\n"
                f" - Relative path: {relative_path!r}.\n\n"
                "Do you want to save the relative path to the linked documents path?\n\n"
                "Depending on your choice, the following path will be written "
                "to the linked document:\n"
                f" - Yes: {relative_path!r}\n"
                f" - No:  {path_str!r}"
            ),
        ):
            return relative_path
        else:
            return path_str

    return path_str
