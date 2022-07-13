"""
    Frames submodule for the main window.
"""

from tkinter import Tk, ttk


class Frames:
    """Frames class for the main window. Holds all ttk frames."""

    def __init__(self, root: Tk) -> None:
        self._frame_left = ttk.Labelframe(
            master=root, style="Left.TLabelframe", text="Infrastructure"
        )
        self._frame_left.grid(
            row=0, column=0, sticky="nsew", padx=(10, 20), pady=(10, 5)
        )
        self._frame_left.grid_columnconfigure(1, weight=1)
        self._frame_left.grid_rowconfigure(14, weight=1)

        self._frame_middle = ttk.Labelframe(
            master=root, style="Middle.TLabelframe", text="Notes"
        )
        self._frame_middle.grid(
            row=0, column=1, sticky="nsew", padx=(0, 10), pady=(10, 5)
        )

        self._frame_right = ttk.Labelframe(
            master=root, style="Right.TLabelframe", text="Processes"
        )
        self._frame_right.grid(
            row=0, column=2, sticky="nsew", padx=(10, 10), pady=(10, 5)
        )

        self._frame_footer = ttk.Frame(master=root, height=30, style="Footer.TFrame")
        self._frame_footer.grid(
            row=1, column=0, sticky="swe", padx=10, pady=(5, 10), columnspan=3
        )
        self._frame_footer.grid_columnconfigure(1, weight=1)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_rowconfigure(0, weight=1)

    @property
    def infrastructure(self) -> ttk.Labelframe:
        """Returns the infrastructure frame."""
        return self._frame_left

    @property
    def notes(self) -> ttk.Labelframe:
        """Returns the notes frame."""
        return self._frame_middle

    @property
    def processes(self) -> ttk.Labelframe:
        """Returns the processes frame."""
        return self._frame_right

    @property
    def footer(self) -> ttk.Frame:
        """Returns the footer frame."""
        return self._frame_footer
