"""
    Submodule for the material manager callbacks.
"""

from pathlib import Path
from tkinter import Toplevel

from app.state_setter import UISetter
from material_manager.layout import Layout
from material_manager.vars import Variables
from resources import resource


class Callbacks:
    """
    The material manager callbacks class. Holds all callback functions and adds them to widgets, etc
    on instantiation.
    """

    def __init__(
        self,
        root: Toplevel,
        variables: Variables,
        layout: Layout,
        ui_setter: UISetter,
        is_part: bool,
    ) -> None:
        """
        Inits the material manager callbacks object.

        Args:
            root (Toplevel): The root object (the material manager window).
            variables (Variables): The material manager variables.
            layout (Layout): The material manager layout.
            ui_setter (UISetter): The main window's ui setter.
            is_part (bool): True if the doc is a part, False otherwise.
        """
        self.root = root
        self.vars = variables
        self.layout = layout
        self.set_parent_ui = ui_setter
        self.is_part = is_part

        self._bind_button_callbacks()

    def _bind_button_callbacks(self) -> None:
        """Binds all callbacks."""
        self.layout.button_save.configure(command=self.on_btn_save)
        self.layout.button_abort.configure(command=self.on_btn_abort)
        # TODO: Bind callbacks for the combobox widgets for logging.

    def on_btn_save(self) -> None:
        """
        Callback for the save button.
        Applies the material to the document.
        """
        if selected_material := self.layout.input_material.get():
            # pylint: disable=C0415
            if self.is_part:
                from pytia.utilities.material import (
                    apply_material_on_part as apply_material,
                )
            else:
                from pytia.utilities.material import (
                    apply_material_on_product as apply_material,
                )
            # pylint: enable=C0415

            self.vars.material.set(selected_material)
            if selected_metadata := self.layout.input_metadata.get():
                self.vars.metadata.set(selected_metadata)
                selected_material = f"{selected_material}{resource.settings.separators.metadata}{selected_metadata}"
            else:
                self.vars.metadata.set("")

            apply_material(
                material=selected_material,
                catalog_path=Path(
                    resource.settings.paths.material,
                    resource.settings.files.material,
                ),
            )

        self.set_parent_ui.reset()
        # FIXME: This also writes the material to the main UI.
        # This is a bit messy and nor easy to follow. Should be done with the variables from the
        # main UI object.

        self.root.grab_release()
        self.root.destroy()

    def on_btn_abort(self) -> None:
        """Callback for the abort button. Closes the material manager interface."""
        self.set_parent_ui.reset()
        self.root.grab_release()
        self.root.destroy()
