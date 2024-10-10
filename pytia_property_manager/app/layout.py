"""
    The layout of the app.
"""

from tkinter import DISABLED
from tkinter import WORD
from tkinter import Tk

from app.frames import Frames
from app.vars import Variables
from app.widgets.notes import NoteWidgets
from app.widgets.processes import ProcessWidgets
from const import STYLES
from const import Source
from helper.appearance import set_appearance_menu
from helper.messages import show_help
from pytia_ui_tools.widgets.texts import ScrolledText
from resources import resource
from ttkbootstrap import Button
from ttkbootstrap import Checkbutton
from ttkbootstrap import Combobox
from ttkbootstrap import Entry
from ttkbootstrap import Label
from ttkbootstrap import Menu


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
        """
        # region MENU
        menubar = Menu(root)

        self._appearance_menu = Menu(menubar, tearoff=False)
        for style in STYLES:
            self._appearance_menu.add_command(label=style)

        self._tools_menu = Menu(menubar, tearoff=False)
        self._tools_menu.add_command(label="Calculate Bounding Box")

        menubar.add_cascade(label="Help", command=show_help)
        menubar.add_cascade(label="Appearance", menu=self._appearance_menu)
        menubar.add_cascade(label="Tools", menu=self._tools_menu)

        set_appearance_menu(self._appearance_menu)
        root.configure(menu=menubar)
        # endregion

        # region FRAME Infra ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # region partnumber
        lbl_partnumber = Label(
            frames.infrastructure,
            text="Part Number",
            width=15,
        )
        lbl_partnumber.grid(
            row=0,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )

        self._entry_partnumber = Entry(
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
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region product number
        lbl_product_number = Label(frames.infrastructure, text="Product Number")
        lbl_product_number.grid(
            row=1, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_product_number = Entry(
            frames.infrastructure,
            textvariable=variables.product_number,
            state=DISABLED,
        )
        self._entry_product_number.grid(
            row=1,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region project number
        lbl_project = Label(frames.infrastructure, text="Project Number")
        lbl_project.grid(
            row=2, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_project = Combobox(
            frames.infrastructure,
            values=[],
            textvariable=variables.project,
            width=27,
            state=DISABLED,
        )
        self._combo_project.grid(
            row=2,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(1, 2),
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region definition
        # lbl_definition = Label(frames.infrastructure, text="Definition")
        # lbl_definition.grid(
        #     row=3, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        # )

        # self._entry_definition = Entry(
        #     frames.infrastructure,
        #     textvariable=variables.definition,
        #     state=DISABLED,
        # )
        # self._entry_definition.grid(
        #     row=3,
        #     column=1,
        #     padx=(5, Layout.MARGIN_X),
        #     pady=2,
        #     sticky="nsew",
        #     columnspan=2,
        # )
        # endregion

        # region revision
        lbl_revision = Label(frames.infrastructure, text="Revision")
        lbl_revision.grid(
            row=3, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_revision = Entry(
            frames.infrastructure,
            textvariable=variables.revision,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_revision.grid(row=3, column=1, padx=5, pady=2, sticky="nsew")

        self._btn_revision = Button(
            frames.infrastructure,
            text="New Revision",
            style="outline",
            width=12,
            state=DISABLED,
        )
        self._btn_revision.grid(
            row=3, column=2, padx=(0, Layout.MARGIN_X), pady=2, sticky="nsew"
        )
        # endregion

        # region source
        lbl_source = Label(
            frames.infrastructure,
            text="Source",
        )
        lbl_source.grid(
            row=4, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_source = Combobox(
            frames.infrastructure,
            values=[s.value for s in Source],
            textvariable=variables.source,
            width=15,
            state=DISABLED,
        )
        self._combo_source.grid(row=4, column=1, padx=5, pady=2, sticky="nsew")

        self._btn_reload_source = Button(
            frames.infrastructure,
            text="Reload",
            style="outline",
            width=12,
            state=DISABLED,
        )
        self._btn_reload_source.grid(
            row=4, column=2, padx=(0, Layout.MARGIN_X), pady=2, sticky="nsew"
        )
        # endregion

        # region material
        lbl_material = Label(frames.infrastructure, text="Material")
        lbl_material.grid(
            row=5,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )

        self._entry_material = Entry(
            frames.infrastructure,
            textvariable=variables.material,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_material.grid(
            row=5, column=1, padx=5, pady=(Layout.MARGIN_Y, 2), sticky="nsew"
        )

        self._btn_material = Button(
            frames.infrastructure,
            text="Select",
            style="outline",
            width=12,
            state=DISABLED,
        )
        self._btn_material.grid(
            row=5,
            column=2,
            padx=(0, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )
        # endregion

        # region base size
        lbl_base_size = Label(frames.infrastructure, text="Base Size")
        lbl_base_size.grid(
            row=6, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_base_size = Entry(
            frames.infrastructure,
            textvariable=variables.base_size,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_base_size.grid(row=6, column=1, padx=(5, 5), pady=2, sticky="nsew")

        self._entry_base_size_preset = Entry(
            frames.infrastructure,
            textvariable=variables.base_size_preset,
            state=DISABLED,
            width=12,
            cursor="arrow",
        )
        self._entry_base_size_preset.grid(
            row=6, column=2, padx=(0, Layout.MARGIN_X), pady=2, sticky="nsew"
        )
        # endregion

        # region tolerance
        lbl_tolerance = Label(frames.infrastructure, text="Tolerance")
        lbl_tolerance.grid(
            row=7, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_tolerance = Combobox(
            frames.infrastructure,
            values=resource.settings.tolerances,
            textvariable=variables.tolerance,
            width=27,
            state=DISABLED,
        )
        self._combo_tolerance.grid(
            row=7,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            sticky="new",
            columnspan=2,
        )
        # endregion

        # region mass
        lbl_mass = Label(frames.infrastructure, text="Mass")
        lbl_mass.grid(row=8, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew")

        self._entry_mass = Entry(
            frames.infrastructure,
            textvariable=variables.mass,
            width=18,
            state=DISABLED,
            cursor="arrow",
        )
        self._entry_mass.grid(row=8, column=1, padx=5, pady=2, sticky="nsew")

        self._btn_mass = Button(
            frames.infrastructure,
            text="Calculate",
            style="outline",
            width=12,
            state=DISABLED,
        )
        self._btn_mass.grid(
            row=8, column=2, padx=(0, Layout.MARGIN_X), pady=2, sticky="nsew"
        )
        # endregion

        # region order number
        lbl_order_number = Label(frames.infrastructure, text="Order Number")
        lbl_order_number.grid(
            row=9,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
        )

        self._entry_order_number = Entry(
            frames.infrastructure,
            textvariable=variables.order_number,
            state=DISABLED,
        )
        self._entry_order_number.grid(
            row=9,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region manufacturer
        lbl_manufacturer = Label(frames.infrastructure, text="Manufacturer")
        lbl_manufacturer.grid(
            row=10, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_manufacturer = Entry(
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
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region supplier
        lbl_supplier = Label(frames.infrastructure, text="Supplier")
        lbl_supplier.grid(
            row=11, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_supplier = Entry(
            frames.infrastructure,
            textvariable=variables.supplier,
            state=DISABLED,
        )
        self._entry_supplier.grid(
            row=11,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region weblink
        lbl_weblink = Label(frames.infrastructure, text="Weblink")
        lbl_weblink.grid(
            row=12, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._entry_weblink = Entry(
            frames.infrastructure,
            textvariable=variables.weblink,
            state=DISABLED,
        )
        self._entry_weblink.grid(row=12, column=1, padx=5, pady=2, sticky="nsew")

        self._btn_weblink = Button(
            frames.infrastructure,
            text="Open",
            style="outline",
            width=12,
            state=DISABLED,
        )
        self._btn_weblink.grid(
            row=12, column=2, padx=(0, Layout.MARGIN_X), pady=2, sticky="nsew"
        )
        # endregion

        # region group
        lbl_group = Label(frames.infrastructure, text="Group")
        lbl_group.grid(
            row=13, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_group = Combobox(
            frames.infrastructure,
            values=[],
            textvariable=variables.group,
            width=27,
            state=DISABLED,
        )
        self._combo_group.grid(
            row=13,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(1, 2),
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region spare part level
        lbl_spare_part = Label(frames.infrastructure, text="Spare Part Level")
        lbl_spare_part.grid(
            row=14, column=0, padx=(Layout.MARGIN_X, 5), pady=2, sticky="nsew"
        )

        self._combo_spare_part = Combobox(
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
            sticky="new",
            columnspan=2,
        )
        # endregion

        # region description
        lbl_description = Label(frames.infrastructure, text="Description")
        lbl_description.grid(
            row=15,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=2,
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
            padx=(3, Layout.MARGIN_X - 1),
            pady=2,
            sticky="nsew",
            columnspan=2,
        )
        # endregion

        # region creator
        lbl_creator = Label(frames.infrastructure, text="Creator")
        lbl_creator.grid(
            row=16,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(Layout.MARGIN_Y, 2),
            sticky="new",
        )
        self._lbl_creator_value = Label(
            frames.infrastructure, textvariable=variables.creator_display
        )
        self._lbl_creator_value.grid(
            row=16,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(Layout.MARGIN_Y, 2),
            sticky="nw",
            columnspan=2,
        )
        # endregion

        # region creator
        lbl_modifier = Label(frames.infrastructure, text="Modifier")
        lbl_modifier.grid(
            row=17,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, 2),
            sticky="new",
        )
        self._lbl_modifier_value = Label(
            frames.infrastructure, textvariable=variables.modifier_display
        )
        self._lbl_modifier_value.grid(
            row=17,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(2, 2),
            sticky="nw",
            columnspan=2,
        )
        # endregion

        # region linked doc
        lbl_linked_doc = Label(frames.infrastructure, text="Linked Drawing")
        lbl_linked_doc.grid(
            row=18,
            column=0,
            padx=(Layout.MARGIN_X, 5),
            pady=(2, Layout.MARGIN_Y),
            sticky="new",
        )
        self._lbl_linked_doc_value = Label(
            frames.infrastructure, textvariable=variables.linked_doc_display
        )
        self._lbl_linked_doc_value.grid(
            row=18,
            column=1,
            padx=(5, Layout.MARGIN_X),
            pady=(2, Layout.MARGIN_Y),
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
        self._iso_view_toggle = Checkbutton(
            master=frames.footer,
            bootstyle="round-toggle",  # type:ignore
            text="Set ISO view",
            variable=variables.set_view,
            onvalue=True,
            offvalue=False,
        )
        self._iso_view_toggle.grid(row=0, column=0, padx=(8, 2), pady=0, sticky="w")

        self._sync_color_toggle = Checkbutton(
            master=frames.footer,
            bootstyle="round-toggle",  # type:ignore
            text="Synchronize color",
            variable=variables.sync_color,
            onvalue=True,
            offvalue=False,
        )
        self._sync_color_toggle.grid(row=0, column=1, padx=(8, 2), pady=0, sticky="w")

        # region button save
        self._btn_save = Button(
            frames.footer, text="Save", style="outline", width=10, state=DISABLED
        )
        self._btn_save.grid(row=0, column=2, padx=(5, 2), pady=0, sticky="e")
        # endregion

        # region button abort
        self._btn_abort = Button(
            frames.footer,
            text="Abort",
            style="outline",
            width=10,
        )
        self._btn_abort.grid(row=0, column=3, padx=(2, 0), pady=0, sticky="e")
        # endregion
        # endregion

    @property
    def tools_menu(self) -> Menu:
        """Returns the tools menu bar entry"""
        return self._tools_menu

    @property
    def input_partnumber(self) -> Entry:
        """Returns the part number entry."""
        return self._entry_partnumber

    @property
    def input_project(self) -> Combobox:
        """Returns the project combobox."""
        return self._combo_project

    @property
    def input_product_number(self) -> Entry:
        """Returns the product number entry."""
        return self._entry_product_number

    @property
    def input_revision(self) -> Entry:
        """Returns the revision entry."""
        return self._entry_revision

    @property
    def button_revision(self) -> Button:
        """Returns the revision button."""
        return self._btn_revision

    @property
    def input_source(self) -> Entry:
        """Returns the source entry."""
        return self._combo_source

    @property
    def button_source(self) -> Button:
        """Returns the source button."""
        return self._btn_reload_source

    @property
    def input_material(self) -> Entry:
        """Returns the material entry."""
        return self._entry_material

    @property
    def button_material(self) -> Button:
        """Returns the material button."""
        return self._btn_material

    @property
    def input_base_size(self) -> Entry:
        """Returns the base size entry."""
        return self._entry_base_size

    @property
    def input_base_size_preset(self) -> Entry:
        """Returns the base size preset entry."""
        return self._entry_base_size_preset

    @property
    def input_mass(self) -> Entry:
        """Returns the mass entry."""
        return self._entry_mass

    @property
    def button_mass(self) -> Button:
        """Returns the mass button."""
        return self._btn_mass

    @property
    def input_order_number(self) -> Entry:
        """Returns the order number entry."""
        return self._entry_order_number

    @property
    def input_manufacturer(self) -> Entry:
        """Returns the manufacturer entry."""
        return self._entry_manufacturer

    @property
    def input_supplier(self) -> Entry:
        """Returns the supplier entry."""
        return self._entry_supplier

    @property
    def input_weblink(self) -> Entry:
        """Returns the supplier weblink."""
        return self._entry_weblink

    @property
    def button_weblink(self) -> Button:
        """Returns the weblink button."""
        return self._btn_weblink

    @property
    def input_group(self) -> Combobox:
        """Returns the group combobox."""
        return self._combo_group

    @property
    def input_tolerance(self) -> Combobox:
        """Returns the tolerance combobox."""
        return self._combo_tolerance

    @property
    def input_spare_part(self) -> Combobox:
        """Returns the spare part combobox."""
        return self._combo_spare_part

    @property
    def input_description(self) -> ScrolledText:
        """Returns the description text widget."""
        return self._text_description

    @property
    def label_creator(self) -> Label:
        """Returns the creator label."""
        return self._lbl_creator_value

    @property
    def label_modifier(self) -> Label:
        """Returns the modifier label."""
        return self._lbl_modifier_value

    @property
    def label_linked_doc(self) -> Label:
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
    def button_save(self) -> Button:
        """Returns the save button."""
        return self._btn_save

    @property
    def button_abort(self) -> Button:
        """Returns the abort button."""
        return self._btn_abort

    @property
    def toggle_iso_view(self) -> Checkbutton:
        """Returns the iso view checkbutton."""
        return self._iso_view_toggle

    @property
    def toggle_sync_color(self) -> Checkbutton:
        """Returns the color sync checkbutton."""
        return self._sync_color_toggle
