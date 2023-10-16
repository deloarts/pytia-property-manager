"""
    Frames submodule for the material manager interface.
"""


from ttkbootstrap import Frame
from ttkbootstrap import Toplevel


class Frames:
    """Frames class: Holds all frames for the material manager."""

    def __init__(self, root: Toplevel) -> None:
        """
        Inits the frames for the material manager.

        Args:
            root (Toplevel): The material manager interface.
        """ """"""
        self._frame_data = Frame(master=root)
        self._frame_data.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self._frame_data.grid_columnconfigure(1, weight=1)

        self._frame_footer = Frame(master=root, height=30)
        self._frame_footer.grid(row=1, column=0, sticky="swe", padx=10, pady=(5, 10))
        self._frame_footer.grid_columnconfigure(0, weight=1)

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

    @property
    def data(self) -> Frame:
        """Returns the data frame of the material manager."""
        return self._frame_data

    @property
    def footer(self) -> Frame:
        """Returns the footer frame of the material manager."""
        return self._frame_footer
