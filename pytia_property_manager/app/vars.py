"""
    The variables submodule for the app.
"""

from dataclasses import dataclass
from tkinter import BooleanVar
from tkinter import StringVar
from tkinter import Tk

from resources import resource


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
    product_number: StringVar
    material: StringVar
    material_meta: StringVar
    base_size: StringVar
    base_size_preset: StringVar
    mass: StringVar

    order_number: StringVar
    manufacturer: StringVar
    supplier: StringVar
    weblink: StringVar
    group: StringVar
    tolerance: StringVar
    spare_part_level: StringVar

    creator: StringVar
    creator_display: StringVar
    modifier: StringVar
    modifier_display: StringVar

    linked_doc: StringVar
    linked_doc_display: StringVar

    set_view: BooleanVar
    sync_color: BooleanVar

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
        self.product_number = StringVar(master=root, name="product_number")
        self.revision = StringVar(master=root, name="revision")
        self.material = StringVar(master=root, name="material")
        self.material_meta = StringVar(master=root, name="material_meta")
        self.base_size = StringVar(master=root, name="base_size")
        self.base_size_preset = StringVar(master=root, name="base_size_preset")
        self.mass = StringVar(master=root, name="mass")
        self.order_number = StringVar(master=root, name="order_number")
        self.manufacturer = StringVar(master=root, name="manufacturer")
        self.supplier = StringVar(master=root, name="supplier")
        self.weblink = StringVar(master=root, name="weblink")
        self.group = StringVar(master=root, name="group")
        self.tolerance = StringVar(master=root, name="tolerance")
        self.spare_part_level = StringVar(master=root, name="spare_part_level")

        self.creator = StringVar(master=root, name="creator")
        self.creator_display = StringVar(master=root, name="creator_display", value="-")
        self.modifier = StringVar(master=root, name="modifier")
        self.modifier_display = StringVar(
            master=root, name="modifier_display", value="-"
        )

        self.linked_doc = StringVar(master=root, name="linked_doc")
        self.linked_doc_display = StringVar(
            master=root, name="linked_doc_display", value="-"
        )

        self.set_view = BooleanVar(
            master=root, name="set_view", value=resource.appdata.set_view
        )
        self.sync_color = BooleanVar(
            master=root, name="sync_color", value=resource.appdata.sync_color
        )
