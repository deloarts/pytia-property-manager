"""
    The layout of the app.
"""
from tkinter import DISABLED, WORD, Tk, ttk

from app.frames import Frames
from app.vars import Variables
from app.widgets.notes import NoteWidgets
from app.widgets.processes import ProcessWidgets
from const import Source
from pytia_ui_tools.widgets.texts import ScrolledText
from resources import resource


class Layout:
    """The layout class of the app, holds all widgets."""

    MARGIN_X = 10
    MARGIN_Y = 10

    def __init__(self, root: Tk, frames: Frames, variables: Variables) -> None:
        """
        Inits the Layout class. Creates and places the widgets of the main window.

        Args:
            root (Tk): The main window.
            frames (Frames): The frames of the main window.
            variables (Variables): The variables of the main window.
        """ """"""
        # region FRAME Infra ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # region partnumber
        lbl_partnumber = ttk.Label(
            frames.infrastructure,
            text="Partnumber",
            width=12,
            font=("Segoe UI", 9, "bold"),
        )
        lbl_partnumber.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )

        self._entry_partnumber = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.partnumber,
            width=30,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_partnumber.grid(
            row=0,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region project
        lbl_project = ttk.Label(frames.infrastructure, text="Project")
        lbl_project.grid(
            row=1, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_project = ttk.Combobox(
            frames.infrastructure,
            values=[],
            textvariable=variables.project,
            width=27,
            state=DISABLED,
        )
        self._combo_project.grid(
            row=1,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(1, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region machine
        lbl_project = ttk.Label(frames.infrastructure, text="Machine")
        lbl_project.grid(
            row=2, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_machine = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.machine,
            state=DISABLED,
        )
        self._entry_machine.grid(
            row=2,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region definition
        lbl_definition = ttk.Label(frames.infrastructure, text="Definition")
        lbl_definition.grid(
            row=3, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_definition = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.definition,
            state=DISABLED,
        )
        self._entry_definition.grid(
            row=3,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region revision
        lbl_revision = ttk.Label(frames.infrastructure, text="Revision")
        lbl_revision.grid(
            row=4, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_revision = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.revision,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_revision.grid(
            row=4, column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_revision = ttk.Button(
            frames.infrastructure,
            text="New Revision",
            width=12,
            state=DISABLED,
        )
        self._btn_revision.grid(
            row=4, column=2, padx=(5, Layout.MARGIN_X), pady=1, sticky="nsew"
        )
        # endregion

        # region source
        lbl_source = ttk.Label(
            frames.infrastructure,
            text="Source",
        )
        lbl_source.grid(
            row=5, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_source = ttk.Combobox(
            frames.infrastructure,
            values=[s.value for s in Source],
            textvariable=variables.source,
            width=15,
            state=DISABLED,
        )
        self._combo_source.grid(
            row=5, column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_reload_source = ttk.Button(
            frames.infrastructure,
            text="Reload",
            state=DISABLED,
            # command=root.on_btn_reload_source,
        )
        self._btn_reload_source.grid(
            row=5, column=2, padx=(5, Layout.MARGIN_X), pady=1, sticky="nsew"
        )
        # endregion

        # region material
        lbl_material = ttk.Label(frames.infrastructure, text="Material")
        lbl_material.grid(
            row=6, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_material = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.material,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_material.grid(
            row=6, column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_material = ttk.Button(
            frames.infrastructure,
            text="Select",
            state=DISABLED,
        )
        self._btn_material.grid(
            row=6, column=2, padx=(5, Layout.MARGIN_X), pady=1, sticky="nsew"
        )
        # endregion

        # region base size
        lbl_base_size = ttk.Label(frames.infrastructure, text="Base Size")
        lbl_base_size.grid(
            row=7, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_base_size = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.base_size,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_base_size.grid(
            row=7, column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_base_size = ttk.Button(
            frames.infrastructure,
            text="Calculate",
            state=DISABLED,
        )
        self._btn_base_size.grid(
            row=7,
            column=2,
            padx=(5, Layout.MARGIN_X),
            pady=1,
            sticky="nsew",
            rowspan=2,
        )

        lbl_base_size_preset = ttk.Label(frames.infrastructure, text="Base Size Preset")
        lbl_base_size_preset.grid(
            row=8, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_base_size_preset = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.base_size_preset,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_base_size_preset.grid(
            row=8, column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="nsew"
        )
        # endregion

        # region mass
        lbl_mass = ttk.Label(frames.infrastructure, text="Mass")
        lbl_mass.grid(row=9, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew")

        self._entry_mass = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.mass,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_mass.grid(
            row=9, column=1, padx=5, pady=2, ipadx=2, ipady=2, sticky="nsew"
        )

        self._btn_mass = ttk.Button(
            frames.infrastructure,
            text="Calculate",
            state=DISABLED,
        )
        self._btn_mass.grid(
            row=9, column=2, padx=(5, Layout.MARGIN_X), pady=1, sticky="nsew"
        )
        # endregion

        # region manufacturer
        lbl_manufacturer = ttk.Label(frames.infrastructure, text="Manufacturer")
        lbl_manufacturer.grid(
            row=10, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_manufacturer = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.manufacturer,
            width=30,
            state=DISABLED,
        )
        self._entry_manufacturer.grid(
            row=10,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region supplier
        lbl_supplier = ttk.Label(frames.infrastructure, text="Supplier")
        lbl_supplier.grid(
            row=11, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_supplier = ttk.Entry(
            frames.infrastructure,
            textvariable=variables.supplier,
            state=DISABLED,
        )
        self._entry_supplier.grid(
            row=11,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region group
        lbl_group = ttk.Label(frames.infrastructure, text="Group")
        lbl_group.grid(
            row=12, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_group = ttk.Combobox(
            frames.infrastructure,
            values=[],
            textvariable=variables.group,
            width=27,
            state=DISABLED,
        )
        self._combo_group.grid(
            row=12,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(1, 2),
            ipadx=2,
            ipady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region tolerance
        lbl_tolerance = ttk.Label(frames.infrastructure, text="Tolerance")
        lbl_tolerance.grid(
            row=13, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_tolerance = ttk.Combobox(
            frames.infrastructure,
            values=resource.settings.tolerances,
            textvariable=variables.tolerance,
            width=27,
            state=DISABLED,
        )
        self._combo_tolerance.grid(
            row=13,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="new",
            columnspan=2,
        )
        # endregion

        # region spare part level
        lbl_spare_part = ttk.Label(
            frames.infrastructure, text="Spare Part Level", state="readonly"
        )
        lbl_spare_part.grid(
            row=14, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_spare_part = ttk.Combobox(
            frames.infrastructure,
            values=resource.settings.spare_part_level,
            textvariable=variables.spare_part_level,
            state=DISABLED,
            width=27,
        )
        self._combo_spare_part.grid(
            row=14,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="new",
            columnspan=2,
        )
        # endregion

        # region description
        lbl_description = ttk.Label(frames.infrastructure, text="Description")
        lbl_description.grid(
            row=15,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=2,
            ipadx=2,
            ipady=2,
            sticky="new",
        )

        self._text_description = ScrolledText(
            parent=frames.infrastructure,
            textvariable=variables.description,
            height=6,
            width=30,
            state=DISABLED,
            wrap=WORD,
            background="#f0f0f0",
            cursor="arrow",
            font=("Segoe UI", 9),
        )
        self._text_description.grid(
            row=15,
            column=1,
            padx=(5, Layout.MARGIN_X + 1),
            pady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region creator
        lbl_creator = ttk.Label(frames.infrastructure, text="Creator")
        lbl_creator.grid(
            row=16,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            ipadx=2,
            ipady=2,
            sticky="new",
        )
        self._lbl_creator_value = ttk.Label(
            frames.infrastructure, textvariable=variables.creator_display
        )
        self._lbl_creator_value.grid(
            row=16,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            ipadx=2,
            ipady=2,
            sticky="nw",
            columnspan=2,
        )
        # endregion

        # region creator
        lbl_modifier = ttk.Label(frames.infrastructure, text="Modifier")
        lbl_modifier.grid(
            row=17,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="new",
        )
        self._lbl_modifier_value = ttk.Label(
            frames.infrastructure, textvariable=variables.modifier_display
        )
        self._lbl_modifier_value.grid(
            row=17,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(2, 2),
            ipadx=2,
            ipady=2,
            sticky="nw",
            columnspan=2,
        )
        # endregion

        # region linked doc
        lbl_linked_doc = ttk.Label(frames.infrastructure, text="Linked Drawing")
        lbl_linked_doc.grid(
            row=18,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, Layout.MARGIN_Y),
            ipadx=2,
            ipady=2,
            sticky="new",
        )
        self._lbl_linked_doc_value = ttk.Label(
            frames.infrastructure, textvariable=variables.linked_doc_display
        )
        self._lbl_linked_doc_value.grid(
            row=18,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(2, Layout.MARGIN_Y),
            ipadx=2,
            ipady=2,
            sticky="nw",
            columnspan=2,
        )
        # endregion
        # endregion

        # region FRAME Notes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._notes = NoteWidgets(root=frames.notes)

        # endregion

        # region FRAME Processes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._processes = ProcessWidgets(
            root=frames.processes, material_metadata=variables.material_meta
        )

        # endregion

        # region FRAME Footer ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # region info
        lbl_info = ttk.Label(
            frames.footer,
            text="",
        )
        lbl_info.grid(
            row=0, column=0, padx=(0, 5), pady=0, ipadx=2, ipady=2, sticky="nsew"
        )
        # endregion

        # region button save
        self._btn_save = ttk.Button(
            frames.footer, text="Save", style="Footer.TButton", state=DISABLED
        )
        self._btn_save.grid(row=0, column=1, padx=(5, 2), pady=0, sticky="e")
        # endregion

        # region button abort
        self._btn_abort = ttk.Button(
            frames.footer, text="Abort", style="Footer.TButton"
        )
        self._btn_abort.grid(row=0, column=2, padx=(2, 0), pady=0, sticky="e")
        # endregion
        # endregion

    @property
    def input_partnumber(self) -> ttk.Entry:
        """Returns the part number entry."""
        return self._entry_partnumber

    @property
    def input_project(self) -> ttk.Combobox:
        """Returns the project combobox."""
        return self._combo_project

    @property
    def input_machine(self) -> ttk.Entry:
        """Returns the machine entry."""
        return self._entry_machine

    @property
    def input_definition(self) -> ttk.Entry:
        """Returns the definition entry."""
        return self._entry_definition

    @property
    def input_revision(self) -> ttk.Entry:
        """Returns the revision entry."""
        return self._entry_revision

    @property
    def button_revision(self) -> ttk.Button:
        """Returns the revision button."""
        return self._btn_revision

    @property
    def input_source(self) -> ttk.Entry:
        """Returns the source entry."""
        return self._combo_source

    @property
    def button_source(self) -> ttk.Button:
        """Returns the source button."""
        return self._btn_reload_source

    @property
    def input_material(self) -> ttk.Entry:
        """Returns the material entry."""
        return self._entry_material

    @property
    def button_material(self) -> ttk.Button:
        """Returns the material button."""
        return self._btn_material

    @property
    def input_base_size(self) -> ttk.Entry:
        """Returns the base size entry."""
        return self._entry_base_size

    @property
    def input_base_size_preset(self) -> ttk.Entry:
        """Returns the base size preset entry."""
        return self._entry_base_size_preset

    @property
    def button_base_size(self) -> ttk.Button:
        """Returns the base size button."""
        return self._btn_base_size

    @property
    def input_mass(self) -> ttk.Entry:
        """Returns the mass entry."""
        return self._entry_mass

    @property
    def button_mass(self) -> ttk.Button:
        """Returns the mass button."""
        return self._btn_mass

    @property
    def input_manufacturer(self) -> ttk.Entry:
        """Returns the manufacturer entry."""
        return self._entry_manufacturer

    @property
    def input_supplier(self) -> ttk.Entry:
        """Returns the supplier entry."""
        return self._entry_supplier

    @property
    def input_group(self) -> ttk.Combobox:
        """Returns the group combobox."""
        return self._combo_group

    @property
    def input_tolerance(self) -> ttk.Combobox:
        """Returns the tolerance combobox."""
        return self._combo_tolerance

    @property
    def input_spare_part(self) -> ttk.Combobox:
        """Returns the spare part combobox."""
        return self._combo_spare_part

    @property
    def input_description(self) -> ScrolledText:
        """Returns the description text widget."""
        return self._text_description

    @property
    def label_creator(self) -> ttk.Label:
        """Returns the creator label."""
        return self._lbl_creator_value

    @property
    def label_modifier(self) -> ttk.Label:
        """Returns the modifier label."""
        return self._lbl_modifier_value

    @property
    def label_linked_doc(self) -> ttk.Label:
        """Returns the linked document label."""
        return self._lbl_linked_doc_value

    @property
    def notes(self) -> NoteWidgets:
        """Returns the notes widget."""
        return self._notes

    @property
    def processes(self) -> ProcessWidgets:
        """Returns the processes widget."""
        return self._processes

    @property
    def button_save(self) -> ttk.Button:
        """Returns the save button."""
        return self._btn_save

    @property
    def button_abort(self) -> ttk.Button:
        """Returns the abort button."""
        return self._btn_abort
