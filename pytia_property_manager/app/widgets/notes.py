"""
    Widget set for notes. Creates the notes in the note frame and provides variables for all
    child widgets.

    This submodule has two classes:

    - NoteWidget: Holds all widgets related to one note. Currently a label and a note text widget.
    - NoteWidgets: Manages multiple instances of ProcessWidget. Has managing methods like add \
        or delete.
"""

import tkinter as tk
from tkinter import StringVar
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from pytia.exceptions import PytiaValueError
from pytia_ui_tools.widgets.texts import ScrolledText
from resources import resource
from ttkbootstrap import Frame
from ttkbootstrap import Label
from ttkbootstrap import Labelframe


class NoteWidget:
    """Note widget class. Holds all elements related to one note set."""

    MARGIN_X = 10
    MARGIN_Y = 10

    def __init__(
        self,
        root: Frame | Labelframe,
        title: str,
        row: int,
    ) -> None:
        """
        Inits the NoteWidget class. Holds all widgets for one note (label, text input).

        Args:
            root ttk.Frame | ttk.Labelframe): The parent of all widgets (the \
                tkinter parent frame).
            title (str): The name of the note element.
            row (int): The place of the note element.
        """
        self._root = root
        self._textvariable = StringVar(name=f"textvariable_{title}")
        self._state = tk.NORMAL
        self._bottom_space = False

        self.lbl_note = Label(
            self._root,
            text=f"{title} Note",
            width=15,
        )
        self.lbl_note.grid(
            row=row,
            column=0,
            padx=(NoteWidget.MARGIN_X, 5),
            pady=(NoteWidget.MARGIN_Y if row == 0 else 2, 2),
            sticky="new",
        )

        self.text_note = ScrolledText(
            parent=self._root,
            textvariable=self._textvariable,
            height=4,
            width=30,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self.text_note.grid(
            row=row,
            column=1,
            padx=(5, NoteWidget.MARGIN_X + 1),
            pady=(
                NoteWidget.MARGIN_Y if row == 0 else 2,
                NoteWidget.MARGIN_Y if row == len(resource.props.notes.keys) - 1 else 2,
            ),
            sticky="nsew",
        )

        self._root.grid_rowconfigure(row, weight=1)

    @property
    def parent(self) -> Frame | Labelframe:
        """Returns the parent of this instance."""
        return self._root

    @property
    def note_var(self) -> StringVar:
        """Returns the variable of the note widget."""
        return self._textvariable

    @note_var.setter
    def note_var(self, value: str) -> None:
        """Sets the value of the note widgets variable."""
        self._textvariable.set(value)

    @property
    def state(self) -> str:
        """Returns the state of the widgets."""
        return self._state

    @state.setter
    def state(self, value: Literal["normal", "disabled"]) -> None:
        """Sets the state of the widgets."""
        self.text_note.state = value
        self._state = value


class NoteWidgets:
    """Note widgets class. Holds all note widgets."""

    def __init__(self, root: Frame | Labelframe) -> None:
        """
        Inits the NoteWidgets class. This class manages the NoteWidget instances.

        Args:
            root (Labelframe): The parent of the widgets.
        """
        self._root = root
        self._note_widgets: Dict[str, NoteWidget] = {}

        self._root.grid_columnconfigure(1, weight=1)

        for item in resource.props.notes.keys:
            self.add(name=item)

    @property
    def note_vars(self) -> List[StringVar]:
        """Returns a list of all StringVar variables of all notes."""
        return [p.note_var for p in self._note_widgets.values()]

    def add(self, name: str) -> NoteWidget:
        """
        Adds a note widget to the parent frame.

        Args:
            name (str): The name of the note.

        Returns:
            NoteWidget: The newly created note widget.
        """
        widget = NoteWidget(
            root=self._root,
            title=name.replace("_", " ").title(),
            row=len(self._note_widgets),
        )
        self._note_widgets[name] = widget
        return widget

    def get(self, name: str) -> NoteWidget:
        """
        Returns a note widget by its name. Fetches

        Args:
            name (str): The name of the widget to retrieve.

        Returns:
            NoteWidget: The retrieved widget.
        """
        if name in self._note_widgets:
            return self._note_widgets[name]
        raise PytiaValueError(f"{name!r} is not a valid NoteWidget.")

    def clear(self, name: Optional[str] = None) -> None:
        """
        Clears the content of the note widget which name matches the given name.

        Args:
            name (Optional[str], optional): The name of the widget to clear. If omitted, all \
                widgets will be cleared. Defaults to None.
        """
        if name:
            note = self.get(name)
            note.note_var.set("")
        else:
            for widget in self._note_widgets.values():
                widget.note_var.set("")

    def state(
        self, state: Literal["normal", "disabled"], name: Optional[str] = None
    ) -> None:
        """
        Sets the state of note widgets.

        Args:
            state (Literal[&quot;normal&quot;, &quot;disabled&quot;]): The tkinter-state.
            name (Optional[int], optional): The name from which to set the state. \
                If None, all notes will be set to the given state. Defaults to None.
        """
        if name:
            self.get(name).state = state
        else:
            for item in self._note_widgets.values():
                item.state = state
