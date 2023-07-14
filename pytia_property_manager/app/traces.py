"""
    Traces submodule for the app.
"""

from pathlib import Path
from tkinter import messagebox as tkmsg

from app.callbacks import on_source_bought
from app.layout import Layout
from app.state_setter import UISetter
from app.tooltips import ToolTip
from app.vars import Variables
from const import PROP_DRAWING_PATH, SUFFIX_DRAWING, Source
from helper.lazy_loaders import LazyDocumentHelper
from pytia.log import log
from resources import resource
from resources.utils import expand_env_vars


class Traces:
    """The Traces class. Responsible for all variable traces in the main window."""

    def __init__(
        self,
        variables: Variables,
        layout: Layout,
        state_setter: UISetter,
        doc_helper: LazyDocumentHelper,
    ) -> None:
        """
        Inits the Traces class. Adds the main windows' variable traces.

        Args:
            vars (Variables): The main window's variables.
            state_setter (UISetter): The state setter of the main window.
            doc_helper(LazyDocumentHelper): The lazy doc loader instance.
        """
        self.vars = variables
        self.layout = layout
        self.set_ui = state_setter
        self.doc_helper = doc_helper

        self._add_traces()
        log.info("Traces initialized.")

    def _add_traces(self) -> None:
        """Adds all traces."""
        self.vars.source.trace_add("write", self.trace_source)
        self.vars.mass.trace_add("write", self.trace_mass)
        self.vars.project.trace_add("write", self.trace_project)
        self.vars.base_size.trace_add("write", self.trace_base_size)
        self.vars.creator.trace_add("write", self.trace_creator)
        self.vars.modifier.trace_add("write", self.trace_modifier)
        self.vars.linked_doc.trace_add("write", self.trace_linked_doc)

    def trace_mass(self, *_) -> None:
        """Trace callback for the `mass` StringVar"""
        if (value := self.vars.mass.get()) and not " kg" in value:
            self.vars.mass.set(f"{value} kg")

    def trace_project(self, *_) -> None:
        """Trace callback for the `project` StringVar"""
        ...

    def trace_linked_doc(self, *_) -> None:
        """Trace callback for the `linked_doc` StringVar"""
        linked_doc = Path(
            expand_env_vars(self.vars.linked_doc.get(), ignore_not_found=True)
        )

        if self.vars.linked_doc.get() == "":
            self.vars.linked_doc_display.set("-")
            self.layout.label_linked_doc.configure(cursor="", foreground="black")
            ToolTip(
                widget=self.layout.label_linked_doc,
                text="There's no drawing document linked to this file.",
            )

        elif linked_doc.is_file() and linked_doc.suffix == SUFFIX_DRAWING:
            self.vars.linked_doc_display.set(linked_doc.stem)
            self.layout.label_linked_doc.configure(cursor="hand2", foreground="blue")
            ToolTip(
                widget=self.layout.label_linked_doc,
                text=str(linked_doc),
            )

        elif tkmsg.askyesno(
            title=resource.settings.title,
            message=(
                "This document has a drawing file attached to it, but the drawing "
                "cannot be found.\n\nDo you want to remove the linked drawing file "
                f"from this document?\n\nLast known location: {str(linked_doc)!r}."
            ),
        ):
            self.doc_helper.document.properties.delete(PROP_DRAWING_PATH)
            self.vars.linked_doc_display.set("Link removed")
            self.layout.label_linked_doc.configure(cursor="", foreground="gray")
            ToolTip(
                widget=self.layout.label_linked_doc,
                text=f"{str(linked_doc)} (link removed)",
            )
        else:
            self.vars.linked_doc_display.set("Document not found")
            self.layout.label_linked_doc.configure(cursor="", foreground="gray")
            ToolTip(
                widget=self.layout.label_linked_doc,
                text=f"{str(linked_doc)} (not found)",
            )

    def trace_base_size(self, *_) -> None:
        """Trace callback for the `base_size` StringVar"""
        value = self.vars.base_size.get()
        log.info(f"Trace callback for variable 'base_size': {value}")
        if not value:
            self.vars.base_size_preset.set("")

    def trace_source(self, *_) -> None:
        """Trace callback for the `source` StringVar. Sets the UI depending on the source value."""
        value = self.vars.source.get()
        log.info(f"Trace callback for variable 'source': {value}")

        # Do nothing if the source hasn't changed.
        if self.vars.previous_source.get() == value:
            log.info("Variable 'source' did not change. Skipping.")
            return

        # Ask the user if the source shall be switched, if values may be deleted with this action.
        if (
            self.vars.previous_source.get() == Source.MADE.value
            or self.vars.previous_source.get() == Source.BOUGHT.value
        ):
            change_source = tkmsg.askyesno(
                message=(
                    "Changing the source may clear some values. This can't be undone.\n\nContinue?"
                )
            )
        else:
            change_source = True

        # Actually change the source.
        if change_source:
            self.vars.previous_source.set(value)
            match value:
                case Source.BOUGHT.value:
                    self.set_ui.bought()
                    on_source_bought(
                        partnumber=self.vars.partnumber,
                        definition=self.vars.definition,
                        manufacturer=self.vars.manufacturer,
                    )
                case Source.MADE.value:
                    self.set_ui.made()
                case _:
                    self.set_ui.unknown()
        else:
            self.vars.source.set(self.vars.previous_source.get())

    def trace_creator(self, *_) -> None:
        """Trace callback for the `creator` StringVar"""
        creator = self.vars.creator.get()
        if resource.logon_exists(creator):
            self.vars.creator_display.set(resource.get_user_by_logon(creator).name)
        else:
            self.vars.creator_display.set(f"Unknown user ({creator})")

    def trace_modifier(self, *_) -> None:
        """Trace callback for the `modifier` StringVar"""
        modifier = self.vars.modifier.get()
        if resource.logon_exists(modifier):
            self.vars.modifier_display.set(resource.get_user_by_logon(modifier).name)
        else:
            self.vars.modifier_display.set(f"Unknown user ({modifier})")
