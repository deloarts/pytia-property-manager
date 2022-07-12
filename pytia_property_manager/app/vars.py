"""
    The variables submodule for the app.
"""

from dataclasses import dataclass
from tkinter import StringVar, Tk


@dataclass(slots=True, kw_only=True)
class Variables:
    """Dataclass for the main windows variables."""

    partnumber: StringVar
    definition: StringVar
    revision: StringVar
    source: StringVar
    previous_source: StringVar
    description: StringVar

    project: StringVar
    machine: StringVar
    material: StringVar
    material_meta: StringVar
    base_size: StringVar
    base_size_preset: StringVar
    mass: StringVar
    manufacturer: StringVar
    supplier: StringVar
    tolerance: StringVar
    spare_part_level: StringVar

    creator: StringVar
    modifier: StringVar

    def __init__(self, root: Tk) -> None:
        """
        Inits the variables.

        Args:
            root (Tk): The main window.
        """
        self.partnumber = StringVar(master=root, name="partnumber")
        self.definition = StringVar(master=root, name="definition")
        self.source = StringVar(master=root, name="source")
        self.previous_source = StringVar(master=root, name="previous_source")
        self.description = StringVar(master=root, name="description")

        self.project = StringVar(master=root, name="project")
        self.machine = StringVar(master=root, name="machine")
        self.revision = StringVar(master=root, name="revision")
        self.material = StringVar(master=root, name="material")
        self.material_meta = StringVar(master=root, name="material_meta")
        self.base_size = StringVar(master=root, name="base_size")
        self.base_size_preset = StringVar(master=root, name="base_size_preset")
        self.mass = StringVar(master=root, name="mass")
        self.manufacturer = StringVar(master=root, name="manufacturer")
        self.supplier = StringVar(master=root, name="supplier")
        self.tolerance = StringVar(master=root, name="tolerance")
        self.spare_part_level = StringVar(master=root, name="spare_part_level")

        self.creator = StringVar(master=root, name="creator")
        self.modifier = StringVar(master=root, name="modifier")
