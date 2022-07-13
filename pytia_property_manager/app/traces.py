"""
    Traces submodule for the app.
"""

from tkinter import messagebox as tkmsg

from const import LOGON, Source
from pytia.log import log
from resources import resource

from app.callbacks import on_source_bought
from app.state_setter import UISetter
from app.vars import Variables


class Traces:
    """The Traces class. Responsible for all variable traces in the main window."""

    def __init__(self, variables: Variables, state_setter: UISetter) -> None:
        """
        Inits the Traces class. Adds the main windows' variable traces.

        Args:
            vars (Variables): The main window's variables.
            state_setter (UISetter): The state setter of the main window.
        """
        self.vars = variables
        self.set_ui = state_setter

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

    def trace_mass(self, *_) -> None:
        """Trace callback for the `mass` StringVar"""
        if (value := self.vars.mass.get()) and not " kg" in value:
            self.vars.mass.set(f"{value} kg")

    def trace_project(self, *_) -> None:
        """Trace callback for the `project` StringVar"""
        ...

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
