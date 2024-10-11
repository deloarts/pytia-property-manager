"""
    Submodule for managing the state of the widgets.
    The UI is mainly managed by the 'source' of the document.

    Four states are available:

    - Unknown
    - Loading
    - Made
    - Bought
"""

import tkinter as tk

from app.layout import Layout
from app.vars import Variables
from const import Source
from helper.lazy_loaders import LazyDocumentHelper
from helper.verifications import verify_url
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource


class UISetter:
    """UI Setter class for the main window."""

    def __init__(
        self,
        root: tk.Tk,
        layout: Layout,
        variables: Variables,
        lazy_document_helper: LazyDocumentHelper,
        workspace: Workspace,
    ) -> None:
        """Inits the UI Setter class for the main window.

        Args:
            root (tk.Tk): The main window object.
            layout (Layout): The layout of the main window.
            variables (Variables): The variables of the main window.
            lazy_document_helper (LazyDocumentHelper): The lazy document helper instance.
            workspace (Workspace): The workspace instance.
        """ """"""
        self.root = root
        self.layout = layout
        self.doc_helper = lazy_document_helper
        self.vars = variables
        self.workspace = workspace

    def reset(self) -> None:
        """Resets the UI depending on the current chosen source."""
        log.info("Resetting main UI state...")
        match self.vars.source.get():
            case Source.MADE.value:
                self.made()
            case Source.BOUGHT.value:
                self.bought()
            case Source.UNKNOWN.value:
                self.unknown()
            case _:
                self.disabled()

    def loading(self) -> None:
        """Sets the UI to state 'loading'. Disables all widgets."""
        self.root.config(cursor="wait")
        self.root.update()
        self.root.update_idletasks()
        self.disabled()

    def unknown(self) -> None:
        """Sets the UI to state 'unknown'. Disabled almost all widgets and clears their content."""
        log.debug("Setting main UI to state 'unknown'.")

        self.layout.input_partnumber.config(state="readonly")

        self.layout.input_project.config(
            state=(
                "readonly"
                if resource.settings.restrictions.strict_project
                and self.workspace.elements.projects
                else tk.NORMAL
            )
        )

        self.layout.input_product_number.config(
            state=(
                "readonly"
                if resource.settings.restrictions.strict_product
                and self.workspace.elements.product
                else tk.NORMAL
            )
        )

        self.layout.input_revision.config(state="readonly")
        self.layout.button_revision.configure(state=tk.NORMAL)

        self.layout.input_source.config(state="readonly")
        self.layout.button_source.configure(state=tk.DISABLED)

        self.vars.material.set("")
        self.vars.material_meta.set("")
        self.layout.input_material.config(state=tk.DISABLED)
        self.layout.button_material.configure(state=tk.DISABLED)

        self.vars.base_size.set("")
        self.vars.base_size_preset.set("")
        self.layout.input_base_size.config(state=tk.DISABLED)
        self.layout.input_base_size_preset.config(state=tk.DISABLED)

        self.vars.mass.set("")
        self.layout.input_mass.config(state=tk.DISABLED)
        self.layout.button_mass.configure(state=tk.DISABLED)

        self.vars.order_number.set("")
        self.layout.input_order_number.config(state=tk.DISABLED)

        self.vars.manufacturer.set("")
        self.layout.input_manufacturer.config(state=tk.DISABLED)

        self.vars.supplier.set("")
        self.layout.input_supplier.config(state=tk.DISABLED)

        self.vars.weblink.set("")
        self.layout.input_weblink.config(state=tk.DISABLED)

        self.vars.group.set("")
        self.layout.input_group.config(state=tk.DISABLED)

        self.vars.tolerance.set("")
        self.layout.input_tolerance.config(state=tk.DISABLED)

        self.vars.spare_part_level.set("")
        self.layout.input_spare_part.config(state=tk.DISABLED)

        self.layout.input_description.state = tk.NORMAL

        self.layout.notes.clear()
        self.layout.notes.state(tk.DISABLED)

        self.layout.processes.clear()
        self.layout.processes.state(tk.DISABLED)

        self.layout.button_abort.configure(state=tk.NORMAL)

        self.root.config(cursor="arrow")
        self.root.update()
        log.info("Main UI state is now 'unknown'.")

    def made(self) -> None:
        """Sets the UI to state 'made'. Enables all made-related widgets."""
        log.debug("Setting main UI to state 'made'.")
        self.layout.input_partnumber.config(state="readonly")

        self.layout.input_project.config(
            state=(
                "readonly"
                if resource.settings.restrictions.strict_project
                and self.workspace.elements.projects
                else tk.NORMAL
            )
        )

        self.layout.input_product_number.config(
            state=(
                "readonly"
                if resource.settings.restrictions.strict_product
                and self.workspace.elements.product
                else tk.NORMAL
            ),
            cursor=(
                "arrow"
                if resource.settings.restrictions.strict_product
                and self.workspace.elements.product
                else "xterm"
            ),
        )

        self.layout.input_revision.config(state="readonly")
        self.layout.button_revision.configure(state=tk.NORMAL)

        self.layout.input_source.config(state="readonly")
        self.layout.button_source.configure(state=tk.NORMAL)

        self.layout.input_material.configure(state="readonly")
        self.doc_helper.setvar_material(self.vars.material, self.vars.material_meta)
        self.layout.button_material.configure(state=tk.NORMAL)

        self.layout.input_base_size.config(state="readonly")
        self.layout.input_base_size_preset.config(state="readonly")

        self.layout.input_mass.config(state="readonly")
        self.layout.button_mass.configure(state=tk.NORMAL)

        self.layout.input_order_number.config(state=tk.NORMAL)

        self.layout.input_manufacturer.config(state=tk.NORMAL)

        self.layout.input_supplier.config(state=tk.NORMAL)

        self.layout.input_weblink.config(state=tk.NORMAL)
        self.layout.button_weblink.configure(
            state=tk.NORMAL if verify_url(self.vars.weblink.get()) else tk.DISABLED
        )

        self.layout.input_group.config(state=tk.NORMAL)

        self.layout.input_tolerance.config(state=tk.NORMAL)
        if not self.vars.tolerance.get():
            self.layout.input_tolerance.current(0)

        self.layout.input_spare_part.config(state="readonly")
        if not self.vars.spare_part_level.get():
            self.layout.input_spare_part.current(0)

        self.layout.input_description.state = tk.NORMAL

        self.layout.notes.state(tk.NORMAL)

        self.layout.processes.state(tk.NORMAL)

        self.layout.button_save.configure(state=tk.NORMAL)

        self.root.config(cursor="arrow")
        self.root.update()
        log.info("Main UI state is now 'made'.")

    def bought(self) -> None:
        """
        Sets the UI to state 'bought'. Enables all bought-related widgets, disables all others.
        """
        log.debug("Setting main UI to state 'bought'.")
        self.layout.input_partnumber.config(state="readonly")

        self.layout.input_project.config(
            state=(
                "readonly"
                if resource.settings.restrictions.strict_project
                and self.workspace.elements.projects
                else tk.NORMAL
            )
        )

        self.layout.input_product_number.config(
            state=(
                "readonly"
                if resource.settings.restrictions.strict_product
                and self.workspace.elements.product
                else tk.NORMAL
            )
        )

        self.layout.input_revision.config(state="readonly")
        self.layout.button_revision.configure(state=tk.NORMAL)

        self.layout.input_source.config(state="readonly")
        self.layout.button_source.configure(state=tk.NORMAL)

        self.layout.input_material.config(state="readonly")
        self.doc_helper.setvar_material(self.vars.material, self.vars.material_meta)
        self.layout.button_material.configure(state=tk.NORMAL)

        self.vars.base_size.set("")
        self.layout.input_base_size.config(state=tk.DISABLED)
        self.layout.input_base_size_preset.config(state=tk.DISABLED)

        self.layout.input_mass.config(state="readonly")
        self.layout.button_mass.configure(state=tk.NORMAL)

        self.layout.input_order_number.config(state=tk.NORMAL)

        self.layout.input_manufacturer.config(state=tk.NORMAL)

        self.layout.input_supplier.config(state=tk.NORMAL)

        self.layout.input_weblink.config(state=tk.NORMAL)
        self.layout.button_weblink.configure(
            state=tk.NORMAL if verify_url(self.vars.weblink.get()) else tk.DISABLED
        )

        self.layout.input_group.config(state=tk.NORMAL)

        self.vars.tolerance.set("")
        self.layout.input_tolerance.config(state=tk.DISABLED)

        self.layout.input_spare_part.config(state=tk.NORMAL)
        self.layout.input_spare_part.current(0)

        self.layout.input_description.state = tk.NORMAL

        self.layout.notes.get("general").state = tk.NORMAL

        self.layout.notes.get("material").note_var = ""
        self.layout.notes.get("material").state = tk.DISABLED

        self.layout.notes.get("base_size").note_var = ""
        self.layout.notes.get("base_size").state = tk.DISABLED

        self.layout.notes.get("supplier").state = tk.NORMAL

        self.layout.notes.get("production").note_var = ""
        self.layout.notes.get("production").state = tk.DISABLED

        self.layout.processes.clear()
        self.layout.processes.state(tk.DISABLED)

        self.layout.button_save.configure(state=tk.NORMAL)

        self.root.config(cursor="arrow")
        self.root.update()
        log.info("Main UI state is now 'bought'.")

    def disabled(self) -> None:
        """
        Sets the UI to state 'disabled'.
        """
        log.debug("Setting main UI to state 'disabled'.")
        self.layout.input_partnumber.config(state=tk.DISABLED)

        self.layout.input_project.config(state=tk.DISABLED)

        self.layout.input_product_number.config(state=tk.DISABLED)

        self.layout.input_revision.config(state=tk.DISABLED)
        self.layout.button_revision.configure(state=tk.DISABLED)

        self.layout.input_source.config(state=tk.DISABLED)
        self.layout.button_source.configure(state=tk.DISABLED)

        self.layout.input_material.config(state=tk.DISABLED)
        self.layout.button_material.configure(state=tk.DISABLED)

        self.layout.input_base_size.config(state=tk.DISABLED)
        self.layout.input_base_size_preset.config(state=tk.DISABLED)

        self.layout.input_mass.config(state=tk.DISABLED)
        self.layout.button_mass.configure(state=tk.DISABLED)

        self.layout.input_order_number.config(state=tk.DISABLED)

        self.layout.input_manufacturer.config(state=tk.DISABLED)

        self.layout.input_supplier.config(state=tk.DISABLED)

        self.layout.input_weblink.config(state=tk.DISABLED)
        self.layout.button_weblink.configure(state=tk.DISABLED)

        self.layout.input_group.config(state=tk.DISABLED)

        self.layout.input_tolerance.config(state=tk.DISABLED)

        self.layout.input_spare_part.config(state=tk.DISABLED)

        self.layout.input_description.state = tk.DISABLED

        self.layout.notes.state(tk.DISABLED)

        self.layout.processes.state(tk.DISABLED)

        self.layout.button_save.configure(state=tk.DISABLED)

        self.root.update()
        log.info("Main UI state is now 'disabled'.")
