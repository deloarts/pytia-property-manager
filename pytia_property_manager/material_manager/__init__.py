"""
    The material manager. Handles materials for parts and product.
    TODO: Move this to pytia-ui-tools.
"""

from pathlib import Path
from tkinter import Toplevel, font, ttk

from app.state_setter import UISetter
from decorators import timer
from pytia.exceptions import PytiaMaterialNotFound
from pytia.log import log
from pytia_ui_tools.window_manager import WindowManager
from resources import resource

from material_manager.callbacks import Callbacks
from material_manager.frames import Frames
from material_manager.layout import Layout
from material_manager.traces import Traces
from material_manager.vars import Variables


class MaterialManager(Toplevel):
    """The user interface of the material manager window."""

    WIDTH = 300
    HEIGHT = 150

    @timer
    def __init__(
        self,
        is_part: bool,
        ui_setter: UISetter,
    ) -> None:
        """
        Inits the material manager window.

        Args:
            is_part (bool): The doc type. True for part, False for product.
            ui_setter (UISetter): The main apps state setter.
        """
        Toplevel.__init__(self)

        self.is_part = is_part
        self.window_manager = WindowManager(self)
        self.vars = Variables(root=self)
        self.frames = Frames(root=self)
        self.layout = Layout(root=self, frames=self.frames, variables=self.vars)
        self.set_parent_ui = ui_setter

        self.title("Material Manager")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.configure(cursor="wait")
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=9)
        self.update()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (MaterialManager.WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (MaterialManager.HEIGHT / 2))
        self.geometry(
            f"{MaterialManager.WIDTH}x{MaterialManager.HEIGHT}+{x_coordinate}+{y_coordinate}"
        )

        style = ttk.Style(self)
        style.configure("Footer.TButton", width=14)

        self.set_parent_ui.loading()
        self.update()
        self.grab_set()
        self.window_manager.remove_window_buttons()
        self.after(100, self.run_controller)
        self.mainloop()

    def run_controller(self) -> None:
        """Runs all controllers. Initializes all lazy loaders."""
        self.retrieve_material_data()
        self.callbacks()
        self.traces()

        self.config(cursor="arrow")
        self.update_idletasks()

    @timer
    def retrieve_material_data(self) -> None:
        """Lazy loads the material families for ui loading improvement."""
        # pylint: disable=C0415
        from pytia.utilities.material import get_materials

        # pylint: enable=C0415

        self.vars.material_data = get_materials(
            str(
                Path(
                    resource.settings.paths.material,
                    resource.settings.files.material,
                )
            )
        )
        if self.vars.material_data:
            self.layout.input_family.config(state="readonly")
            self.layout.input_family.config(values=list(self.vars.material_data.keys()))
            log.info(
                f"Retrieved material families from {resource.settings.files.material}."
            )
            return
        raise PytiaMaterialNotFound(
            f"No material families found in {resource.settings.files.material}"
        )

    def callbacks(self) -> None:
        """Inits the callbacks instance."""
        Callbacks(
            root=self,
            variables=self.vars,
            layout=self.layout,
            ui_setter=self.set_parent_ui,
            is_part=self.is_part,
        )

    def traces(self) -> None:
        """Inits the traces instance."""
        Traces(variables=self.vars, layout=self.layout)
