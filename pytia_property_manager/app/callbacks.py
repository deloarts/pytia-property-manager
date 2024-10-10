"""
    The callbacks submodule for the main window.
"""

# pylint: disable=E0611

import os
import re
import shutil
import sys
import webbrowser
from pathlib import Path
from stat import S_IREAD
from stat import S_IRGRP
from stat import S_IROTH
from stat import S_IWUSR
from tkinter import StringVar
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox as tkmsg
from tkinter import simpledialog

from app.layout import Layout
from app.state_setter import UISetter
from app.vars import Variables
from const import PROP_DRAWING_PATH
from const import REVISION_FOLDER
from const import SUFFIX_DRAWING
from const import Source
from handler.properties import Properties
from helper.launcher import launch_bounding_box_app
from helper.lazy_loaders import LazyDocumentHelper
from helper.values import calculate_definition
from helper.values import get_new_revision
from material_manager import MaterialManager
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.helper.values import add_current_value_to_combobox_list
from resources import resource
from resources.utils import create_path_symlink
from resources.utils import create_path_workspace_level
from resources.utils import expand_env_vars
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN


def on_source_bought(
    partnumber: StringVar,
    order_number: StringVar,
    manufacturer: StringVar,
    force: bool = False,
) -> None:
    """
    Callback function for the bought option.

    Checks the nomenclature of the partnumber. Writes the order number and the manufacturer if
    the nomenclature is valid. Shows a warning message if the nomenclature is not valid.

    Does not overwrite existing values, except when the `force` flag is set to True.

    Args:
        partnumber (StringVar): The partnumber variable.
        order_number (StringVar): The order_number variable.
        manufacturer (StringVar): The manufacturer variable.
        force (bool, optional): Deletes the current order_number value and replaces it with the \
            result of the nomenclature check. Defaults to False.
    """
    value = partnumber.get()

    if len(values := value.split(resource.settings.separators.bought)) >= 2:
        if not manufacturer.get() or force:
            manufacturer.set(values[-1])
        values.pop(-1)
        values.pop(0)
        if not order_number.get() or force:
            order_number.set(
                resource.settings.separators.bought.join(v for v in values)
            )
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
        """
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
        self._bind_menu_callbacks()
        log.info("Callbacks initialized.")

    def _bind_button_callbacks(self) -> None:
        """Binds all callbacks to the main windows buttons."""
        self.layout.button_revision.configure(command=self.on_btn_revision)
        self.layout.button_source.configure(command=self.on_btn_reload_source)
        self.layout.button_material.configure(command=self.on_btn_material)
        self.layout.button_mass.configure(command=self.on_btn_mass)
        self.layout.button_weblink.configure(command=self.on_btn_weblink)
        self.layout.button_save.configure(command=self.on_btn_save)
        self.layout.button_abort.configure(command=self.on_btn_abort)

    def _bind_menu_callbacks(self) -> None:
        """Binds all callbacks to the menubar."""
        self.layout.tools_menu.entryconfig(0, command=self.on_add_drawing_file)
        self.layout.tools_menu.entryconfig(1, command=self.on_remove_drawing_file)
        self.layout.tools_menu.entryconfig(3, command=self.on_calculate_bounding_box)

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
        self.layout.label_linked_doc.bind(
            "<Button-1>", lambda _: self.on_lbl_linked_doc()
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

            if resource.appdata.set_view:
                self.doc_helper.set_view()

            self.root.withdraw()
            self.root.destroy()
        else:
            self.set_ui.reset()

    def on_btn_abort(self) -> None:
        """Callback function for the abort button. Closes the app."""
        log.info("Callback for button 'Abort'.")
        self.root.withdraw()
        self.root.destroy()

    def on_btn_revision(self) -> None:
        """Callback function for the revision button."""
        log.info("Callback for button 'Revision'.")

        if self.doc_helper.document.properties.exists(PROP_DRAWING_PATH):
            d_path = self.doc_helper.document.properties.get_by_name(
                PROP_DRAWING_PATH
            ).value
            if not tkmsg.askyesno(
                title=resource.settings.title,
                message=(
                    f"This document has a drawing file attached to it at {d_path}.\n\n"
                    "Creating a new revision will remove the link to the attached "
                    "document.\n\nDo you want to continue?"
                ),
            ):
                return

        current_desc = self.vars.description.get()
        line_ending = "\n" if len(current_desc) else ""

        current_revision = self.vars.revision.get()
        new_revision = get_new_revision(self.vars.revision)

        user_input = simpledialog.askstring(
            parent=self.root,
            title=resource.settings.title,
            prompt=(
                "Enter a brief description of the changes you're about to make "
                f"between revision {current_revision} and {new_revision}. "
                f"{'The definition of the document will be changed. ' if resource.settings.auto_definition.enable else ''}"
                "\n\nCreating a new revision must be done before changing anything "
                "in the document."
            ),
        )

        if user_input and not re.match(r"^\s+$", str(user_input)):
            revision_folder = Path(self.doc_helper.folder, REVISION_FOLDER)
            revision_file = Path(
                revision_folder, f"{current_revision}.{self.doc_helper.name}"
            )
            try:
                os.makedirs(name=revision_folder, exist_ok=True)
                SetFileAttributes(str(revision_folder), FILE_ATTRIBUTE_HIDDEN)  # type: ignore

                if os.path.exists(revision_file):
                    os.chmod(revision_file, S_IWUSR | S_IREAD)
                    os.remove(revision_file)
                shutil.copy(self.doc_helper.path, revision_file)
                os.chmod(revision_file, S_IREAD | S_IRGRP | S_IROTH)

                self.vars.revision.set(new_revision)
                self.vars.description.set(
                    f"Revision {new_revision}: {user_input}{line_ending}{current_desc}"
                )
                if resource.settings.auto_definition.enable:
                    self.vars.definition.set(
                        calculate_definition(
                            product_number=self.vars.product_number,
                            partnumber=self.vars.partnumber,
                            revision=self.vars.revision,
                            prefix=self.workspace.elements.definition_prefix
                            or resource.settings.auto_definition.prefix,
                        )
                    )

                log.info(
                    f"Created new revision ({new_revision}) for document "
                    f"{self.doc_helper.name} and saved a copy of the old revision to "
                    f"{revision_folder}."
                )
                if self.doc_helper.document.properties.exists(PROP_DRAWING_PATH):
                    self.doc_helper.document.properties.delete(PROP_DRAWING_PATH)
                    self.vars.linked_doc.set("")
                    log.info(f"Removed property {PROP_DRAWING_PATH!r} from document.")

            except PermissionError as e:
                log.error(f"Failed to create new revision: {e}")
                tkmsg.showerror(
                    title=resource.settings.title,
                    message=(
                        "Failed to create a new revision: Permission error in the file system."
                    ),
                )
        else:
            tkmsg.showwarning(
                title=resource.settings.title,
                message=("Failed to create a new revision: Invalid description."),
            )

    def on_btn_material(self) -> None:
        """Callback function for the material button. Opens the material manager window."""
        log.info("Callback for button 'Material'.")
        MaterialManager(
            doc_helper=self.doc_helper,
            ui_setter=self.set_ui,
        )

    def on_calculate_bounding_box(self) -> None:
        """Callback function for the bounding box tool menu entry.
        Launches the bounding box app."""
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
                order_number=self.vars.order_number,
                manufacturer=self.vars.manufacturer,
                force=True,
            )

    def on_btn_mass(self) -> None:
        """Callback function for the mass button. Loads the mass of the document."""
        log.info("Callback for button 'Mass'.")
        self.set_ui.loading()
        self.doc_helper.setvar_mass(self.vars.mass, force=True)
        self.set_ui.reset()

    def on_btn_weblink(self) -> None:
        """Callback function for the weblink button. Loads the mass of the document."""
        log.info("Callback for button 'Weblink': Opening weblink")
        webbrowser.open(self.vars.weblink.get())

    def on_lbl_linked_doc(self) -> None:
        """Opens the linked document, if there is one and closes the app."""
        drawing_file_value = self.vars.linked_doc.get()
        if drawing_file_value.startswith(".\\") and self.workspace.workspace_folder:
            relative_path = Path(drawing_file_value[2:])
            linked_doc = Path(self.workspace.workspace_folder, relative_path)
        else:
            linked_doc = Path(
                expand_env_vars(drawing_file_value, ignore_not_found=True)
            )
        log.debug(f"Linked doc path: {linked_doc}")

        # We have to check if the document is available in a window, otherwise a
        # prompt with "do you want to open the document again" would appear.
        if linked_doc.name in self.doc_helper.get_all_open_windows():
            self.doc_helper.framework.catia.windows.item(linked_doc.name).activate()
            log.info("User opened linked document (window).")
            sys.exit()
        if linked_doc.is_file() and linked_doc.suffix == SUFFIX_DRAWING:
            self.doc_helper.framework.catia.documents.open(str(linked_doc))
            log.info("User opened linked document (file).")
            sys.exit()

    def on_add_drawing_file(self) -> None:
        """Adds a drawing file to the doc properties"""
        drawing_file = Path(
            filedialog.askopenfilename(
                parent=self.root,
                title=resource.settings.title,
                initialdir=self.workspace.workspace_folder,
                defaultextension="*.CATDrawing",
                filetypes=[("CATDrawing", "*.CATDrawing")],
            )
        )
        if not drawing_file.is_file():
            tkmsg.showwarning(
                title=resource.settings.title,
                message=("The given path is not a valid file."),
            )
            return

        if self.workspace and self.workspace.workspace_folder:
            self.vars.linked_doc.set(
                create_path_workspace_level(
                    path=drawing_file,
                    workspace_folder=self.workspace.workspace_folder,
                    always_apply_relative=False,
                )
            )
        else:
            self.vars.linked_doc.set(
                create_path_symlink(
                    path=drawing_file,
                    alway_apply_symlink=False,
                )
            )

    def on_remove_drawing_file(self) -> None:
        """Removes the drawing file link from the documents properties"""
        self.doc_helper.document.properties.delete(PROP_DRAWING_PATH)
        self.vars.linked_doc_display.set("Link removed")
