"""
    The callbacks submodule for the main window.
"""

from tkinter import StringVar, Tk
from tkinter import messagebox as tkmsg

from const import Source
from handler.properties import Properties
from helper.launcher import launch_bounding_box_app
from helper.lazy_loaders import LazyDocumentHelper
from material_manager import MaterialManager
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.helper.values import add_current_value_to_combobox_list
from resources import resource

from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables


def on_source_bought(
    partnumber: StringVar,
    definition: StringVar,
    manufacturer: StringVar,
    force: bool = False,
) -> None:
    """
    Callback function for the bought option.

    Checks the nomenclature of the partnumber. Writes the definition and the manufacturer if
    the nomenclature is valid. Shows a warning message if the nomenclature is not valid.

    Does not overwrite existing values, except when the `force` flag is set to True.

    Args:
        partnumber (StringVar): The partnumber variable.
        definition (StringVar): The definition variable.
        manufacturer (StringVar): The manufacturer variable.
        force (bool, optional): Deletes the current definition value and replaces it with the \
            result of the nomenclature check. Defaults to False.
    """
    value = partnumber.get()

    if len(values := value.split(resource.settings.separators.bought)) >= 2:
        if not manufacturer.get() or force:
            manufacturer.set(values[-1])
        values.pop(-1)
        values.pop(0)
        if not definition.get() or force:
            definition.set(resource.settings.separators.bought.join(v for v in values))
    else:
        log.info(
            "Source option 'bought' is selected, but the nomenclature is not valid. "
            "Informing user."
        )
        tkmsg.showwarning(
            message=(
                "The partnumber doesn't match the nomenclature for bought items. "
                "Please consider changing the filename to the convention.\n\n"
                f"The nomenclature is:\n{resource.settings.nomenclature.bought}, "
                f"where the separator is {resource.settings.separators.bought!r}"
            )
        )


class Callbacks:
    """The callbacks class for the main window."""

    def __init__(
        self,
        root: Tk,
        variables: Variables,
        lazy_document_helper: LazyDocumentHelper,
        layout: Layout,
        properties: Properties,
        workspace: Workspace,
        ui_setter: UISetter,
    ) -> None:
        """
        Initializes the callbacks class.

        Args:
            root (Tk): The main window of the app.
            variables (Variables): The variables of the main window.
            lazy_document_helper (LazyDocumentHelper): The lazy document helper object.
            layout (Layout): The layout of the main window.
            properties (Properties): The properties of the main window.
            workspace (Workspace): The workspace instance.
            ui_setter (UISetter): The ui setter instance of the main window.
        """ """"""
        self.root = root
        self.vars = variables
        self.doc_helper = lazy_document_helper
        self.layout = layout
        self.properties = properties
        self.workspace = workspace
        self.set_ui = ui_setter
        self.readonly = bool(
            not resource.logon_exists()
            and not resource.settings.restrictions.allow_all_users
        )

        self._bind_button_callbacks()
        self._bind_widget_callbacks()
        log.info("Callbacks initialized.")

    def _bind_button_callbacks(self) -> None:
        """Binds all callbacks to the main windows buttons."""
        self.layout.button_source.configure(command=self.on_btn_reload_source)
        self.layout.button_material.configure(command=self.on_btn_material)
        self.layout.button_base_size.configure(command=self.on_btn_bounding_box)
        self.layout.button_mass.configure(command=self.on_btn_mass)
        self.layout.button_save.configure(command=self.on_btn_save)
        self.layout.button_abort.configure(command=self.on_btn_abort)

    def _bind_widget_callbacks(self) -> None:
        """Binds all callbacks to the main windows widgets."""
        if not (
            resource.settings.restrictions.strict_project
            and self.workspace.elements.projects
        ):
            self.layout.input_project.bind(
                "<FocusOut>",
                lambda _: add_current_value_to_combobox_list(self.layout.input_project),
            )
        self.layout.input_tolerance.bind(
            "<FocusOut>",
            lambda _: add_current_value_to_combobox_list(self.layout.input_tolerance),
        )

    def on_btn_save(self) -> None:
        """
        Event handler for the OK button. Verifies the user input and saves the changes to the
        documents properties.
        """
        log.info("Callback for button 'Save'.")
        self.set_ui.loading()

        if resource.settings.restrictions.enable_information:
            for msg in resource.get_info_msg_by_counter():
                tkmsg.showinfo(
                    title=resource.settings.title, message=f"Did you know:\n\n{msg}"
                )

        if self.properties.verify():
            self.properties.checkout()
            self.doc_helper.setup_main_body(variables=self.vars)

            self.root.withdraw()
            self.root.destroy()
        else:
            self.set_ui.reset()

    def on_btn_abort(self) -> None:
        """Callback function for the abort button. Closes the app."""
        log.info("Callback for button 'Abort'.")
        self.root.withdraw()
        self.root.destroy()

    def on_btn_material(self) -> None:
        """Callback function for the material button. Opens the material manager window."""
        log.info("Callback for button 'Material'.")
        MaterialManager(
            is_part=self.doc_helper.is_part,  # type: ignore
            ui_setter=self.set_ui,
        )

    def on_btn_bounding_box(self) -> None:
        """Callback function for the bounding box button. Launches the bounding box app."""
        log.info("Callback for button 'Bounding Box'.")
        self.set_ui.loading()

        launch_bounding_box_app()
        self.doc_helper.document.current()
        self.doc_helper.setvar_property(
            self.vars.base_size, resource.props.infra.base_size
        )
        self.doc_helper.setvar_property(
            self.vars.base_size_preset, resource.props.infra.base_size_preset
        )

        self.set_ui.reset()

    def on_btn_reload_source(self) -> None:
        """Callback function for the reload source button. Runs the on_source_bought function."""
        log.info("Callback for button 'Source'.")
        if self.vars.source.get() == Source.BOUGHT.value:
            on_source_bought(
                partnumber=self.vars.partnumber,
                definition=self.vars.definition,
                manufacturer=self.vars.manufacturer,
                force=True,
            )

    def on_btn_mass(self) -> None:
        """Callback function for the mass button. Loads the mass of the document."""
        log.info("Callback for button 'Mass'.")
        self.set_ui.loading()
        self.doc_helper.setvar_mass(self.vars.mass, force=True)
        self.set_ui.reset()
