"""
    Variables submodule for the material manager.
"""

from dataclasses import dataclass
from tkinter import StringVar, Toplevel
from typing import Dict, List


@dataclass(slots=True, kw_only=True)
class Variables:
    """Dataclass that holds all material manager variables."""

    material: StringVar
    metadata: StringVar

    sel_family: StringVar
    sel_material: StringVar
    sel_color: StringVar

    material_data: Dict[str, List[str]]

    def __init__(self, root: Toplevel):
        self.material = StringVar(master=root)
        self.metadata = StringVar(master=root)

        self.sel_family = StringVar(master=root)
        self.sel_material = StringVar(master=root)
        self.sel_color = StringVar(master=root)

        self.material_data = {}
