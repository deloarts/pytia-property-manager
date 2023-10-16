"""
    Traces submodule for the app.
"""

import tkinter as tk
from typing import List

from material_manager.layout import Layout
from material_manager.vars import Variables
from resources import resource


class Traces:
    """Traces class: Holds all traces callback functions. Hooks all traces on instantiation."""

    def __init__(self, variables: Variables, layout: Layout) -> None:
        """Inits the traces class.

        Args:
            variables (Variables): The material manager variables.
            layout (Layout): The layout of the material manager UI.
        """
        self.vars = variables
        self.layout = layout

        self._add_traces()

    def _add_traces(self) -> None:
        """Adds variable traces."""
        self.vars.sel_family.trace_add("write", self.trace_material_family)
        self.vars.sel_material.trace_add("write", self.trace_material_selection)

    def trace_material_family(self, *_) -> None:
        """The trace for the material family."""
        self.vars.sel_material.set("")

        if selected_family := self.vars.sel_family.get():
            data = list(self.vars.material_data[selected_family])
            materials: List[str] = []

            for item in data:
                if resource.settings.separators.metadata in item:
                    material = item.split(resource.settings.separators.metadata)[0]
                else:
                    material = item

                if material not in materials:
                    materials.append(material)

            self.layout.input_material.config(
                state="readonly", values=sorted(materials)
            )
        else:
            self.layout.input_material.config(state=tk.DISABLED, values=[])

    def trace_material_selection(self, *_) -> None:
        """The trace for the material selection."""
        self.vars.sel_color.set("")

        if selected_material := self.vars.sel_material.get():
            data = list(self.vars.material_data[self.vars.sel_family.get()])
            metadata: List[str] = [""]
            for item in data:
                if (
                    f"{selected_material}{resource.settings.separators.metadata}"
                    in item
                ):
                    datum = item.split(resource.settings.separators.metadata)[1]
                    if datum not in metadata:
                        metadata.append(datum)
            if len(metadata) > 1:
                # Check if there is a material without metadata (the base material, if you will),
                # if not: Pop the option to select a material without metadata from the metadata
                # list. In other words: Pop the empty option.
                if selected_material not in data:
                    metadata.remove("")

                self.layout.input_metadata.config(
                    state="readonly", values=sorted(metadata)
                )
                self.layout.input_metadata.current(0)
            else:
                self.layout.input_metadata.config(state=tk.DISABLED, values=[])

            self.layout.button_save.configure(state=tk.NORMAL)
        else:
            self.layout.button_save.configure(state=tk.DISABLED)
