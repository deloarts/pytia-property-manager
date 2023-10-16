"""
    The layout submodule for the material manager.
"""

import tkinter as tk

from material_manager.frames import Frames
from material_manager.vars import Variables
from ttkbootstrap import Button
from ttkbootstrap import Combobox
from ttkbootstrap import Entry
from ttkbootstrap import Label
from ttkbootstrap import Menu
from ttkbootstrap import Toplevel


class Layout:
    """Layout class for the material manager: The main layout of the app."""

    def __init__(self, root: Toplevel, frames: Frames, variables: Variables) -> None:
        """
        Inits the layout. Adds all widgets.

        Args:
            root (Toplevel): The root of the layout (the material manager window).
            frames (Frames): The material manager frames.
            variables (Variables): The material manager variables.
        """ """"""
        lbl_family = Label(frames.data, text="Family")
        lbl_family.grid(row=0, column=0, padx=(0, 15), pady=(0, 2), sticky="nsew")

        self._combo_family = Combobox(
            frames.data,
            values=[],
            textvariable=variables.sel_family,
            state=tk.DISABLED,
        )
        self._combo_family.grid(
            row=0, column=1, padx=(5, 0), pady=(0, 2), sticky="nsew"
        )

        lbl_material = Label(frames.data, text="Material")
        lbl_material.grid(row=1, column=0, padx=(0, 15), pady=(2, 2), sticky="nsew")

        self._combo_material = Combobox(
            frames.data,
            values=[],
            textvariable=variables.sel_material,
            state=tk.DISABLED,
        )
        self._combo_material.grid(
            row=1, column=1, padx=(5, 0), pady=(2, 2), sticky="nsew"
        )

        lbl_color = Label(frames.data, text="Metadata")
        lbl_color.grid(row=2, column=0, padx=(0, 15), pady=(2, 2), sticky="nsew")

        self._combo_color = Combobox(
            frames.data,
            values=[],
            textvariable=variables.sel_color,
            state=tk.DISABLED,
        )
        self._combo_color.grid(row=2, column=1, padx=(5, 0), pady=(2, 2), sticky="nsew")

        self._btn_save = Button(
            frames.footer,
            text="Apply",
            style="outline",
            width=10,
            state=tk.DISABLED,
        )
        self._btn_save.grid(row=0, column=0, padx=(5, 2), pady=0, sticky="e")

        self._btn_abort = Button(
            frames.footer,
            text="Abort",
            style="outline",
            width=10,
        )
        self._btn_abort.grid(row=0, column=1, padx=(2, 0), pady=0, sticky="e")

    @property
    def input_family(self) -> Combobox:
        """Returns the input widget for the material family."""
        return self._combo_family

    @property
    def input_material(self) -> Combobox:
        """Returns the input widget for the material."""
        return self._combo_material

    @property
    def input_metadata(self) -> Combobox:
        """Returns the input widget for the metadata."""
        return self._combo_color

    @property
    def button_save(self) -> Button:
        """Returns the save button."""
        return self._btn_save

    @property
    def button_abort(self) -> Button:
        """Returns the abort button."""
        return self._btn_abort
