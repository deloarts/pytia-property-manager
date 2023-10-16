"""
    Widget set for processes. Creates the processes in the process frame and provides
    variables for all child widgets.

    This submodule has two classes:

    - ProcessWidget: Holds all widgets related to one process. Currently a label, a combobox and \
        a note text widget.
    - ProcessWidgets: Manages multiple instances of ProcessWidget. Has managing methods like add \
        or delete.
"""

import tkinter as tk
from tkinter import StringVar
from tkinter import messagebox as tkmsg
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from pytia.log import log
from pytia_ui_tools.widgets.texts import ScrolledText
from resources import resource
from ttkbootstrap import Combobox
from ttkbootstrap import Frame
from ttkbootstrap import Label
from ttkbootstrap import Labelframe


class ProcessWidget:
    """The process widget class. Holds all widgets related to one process."""

    MARGIN_X = 10
    MARGIN_Y = 10

    def __init__(
        self,
        root: Frame | Labelframe,
        pid: int,
        callback_combo: Callable,
        callback_process: Callable,
    ) -> None:
        """
        Inits the ProcessWidget class. Holds all widgets for one process (label, combobox and note).

        Args:
            root (tk.Tk | tk.Frame | ttk.Frame | ttk.Labelframe): The parent of all widgets (the \
                tkinter parent frame).
            pid (int): The id of this instance.
            callback_combo (Callable): The callback method for combobox selections.
            callback_process (Callable): The callback for the process variable trace.
        """
        self._root = root
        self._pid = pid
        self._func_combo = callback_combo
        self._func_process = callback_process

        self._process_var = StringVar()
        self._process_var.trace_add("write", self._callback_process_var)
        self._note_var = StringVar()

        self._state = tk.NORMAL
        self._bottom_space = False

        self.lbl_process = Label(
            self._root,
            text=f"Process {self._pid}",
            width=15,
        )
        self.lbl_process.grid(
            row=(self._pid - resource.settings.processes.first) * 2,
            column=0,
            padx=(ProcessWidget.MARGIN_X, 5),
            pady=(
                ProcessWidget.MARGIN_Y
                if self._pid == resource.settings.processes.first
                else 2,
                2,
            ),
            sticky="nsew",
        )

        combo_process_values = [""]
        combo_process_values.extend([p.name for p in resource.processes])
        self.combo_process = Combobox(
            self._root,
            values=combo_process_values,
            textvariable=self._process_var,
            state="readonly",
        )
        self.combo_process.grid(
            row=(self._pid - resource.settings.processes.first) * 2,
            column=1,
            padx=(5, ProcessWidget.MARGIN_X),
            pady=(
                ProcessWidget.MARGIN_Y + 1
                if self._pid == resource.settings.processes.first
                else 2,
                2,
            ),
            sticky="new",
        )
        self.combo_process.bind("<<ComboboxSelected>>", self._callback_combo)

        self.text_note_process = ScrolledText(
            parent=self._root,
            textvariable=self._note_var,
            height=4,
            width=30,
            state=tk.DISABLED,
            wrap=tk.WORD,
        )
        self.text_note_process.grid(
            row=(self._pid - resource.settings.processes.first) * 2 + 1,
            column=1,
            padx=(3, ProcessWidget.MARGIN_X - 1),
            pady=2,
            sticky="nsew",
        )

        self._root.grid_rowconfigure(
            (self._pid - resource.settings.processes.first) * 2 + 1, weight=1
        )

    @property
    def parent(self) -> Frame | Labelframe:
        """Returns the parent of this instance."""
        return self._root

    @property
    def pid(self) -> int:
        """Returns the process id of this instance."""
        return self._pid

    @property
    def process_var(self) -> StringVar:
        """Returns the variable of the combobox selection."""
        return self._process_var

    @process_var.setter
    def process_var(self, value: str) -> None:
        """Sets the value of the combobox variable."""
        self._process_var.set(value)

    @property
    def note_var(self) -> StringVar:
        """Returns the variable of the note widget."""
        return self._note_var

    @note_var.setter
    def note_var(self, value: str) -> None:
        """Sets the value of the note widgets variable."""
        self._note_var.set(value)

    @property
    def state(self) -> str:
        """Returns the state of the widgets. Combobox and note are combined."""
        return self._state

    @state.setter
    def state(self, value: Literal["normal", "disabled"]) -> None:
        """
        Sets the state of the widgets. Combobox and note are combined.
        The state of the note widget only `NORMAL`if the state of the combobox is not `DISABLED`
        and the StringVar value of the process is not empty.
        """
        self.combo_process.configure(
            state="readonly" if value == tk.NORMAL else tk.DISABLED
        )
        self.text_note_process.state = (
            tk.NORMAL if self._process_var.get() and value == tk.NORMAL else tk.DISABLED
        )
        self._state = value

    @property
    def bottom_space(self) -> bool:
        """
        Returns the current bottom space state of the widget. The last widget needs a higher margin
        value on the bottom, all other widgets not. This is for a nice look.
        """
        return self._bottom_space

    @bottom_space.setter
    def bottom_space(self, value: bool) -> None:
        """Switches the bottom space value."""
        self.text_note_process.grid_configure(
            pady=(2, ProcessWidget.MARGIN_Y if value else 2)
        )
        self._bottom_space = value

    def _callback_combo(self, event: tk.Event) -> None:
        """
        The combobox-selection callback.
        Calls the `_callback_combo` method of the `ProcessWidgets` class.
        """
        self._func_combo(self._pid, event.widget.get())

    def _callback_process_var(self, *_) -> None:
        """
        The process variable trace callback.
        Calls the `_callback_process` method of the `ProcessWidgets` class.
        """
        self._func_process(self._pid, self._process_var.get())


class ProcessWidgets:
    """The process widgets class. Holds all process widgets."""

    def __init__(
        self,
        root: Frame | Labelframe,
        material_metadata: StringVar,
    ) -> None:
        """
        Inits the ProcessWidgets class. This class handles the ProcessWidget instances.

        Args:
            root (tk.Tk | tk.Frame | ttk.Frame | ttk.Labelframe): The parent of the widgets.
            material_meta (StringVar): The metadata from a selected material.
        """
        self._root = root
        self._material_meta = material_metadata
        self._init_amount = int(resource.settings.processes.min)
        self._process_widgets: Dict[int, ProcessWidget] = {}
        self._current_pid = resource.settings.processes.first - 1

        self._root.grid_columnconfigure(1, weight=1)

        # On instantiation the minimum amount of widgets is created.
        for _ in range(self._init_amount):
            self.add()
        self.state(tk.DISABLED)

    @property
    def process_vars(self) -> List[StringVar]:
        """Returns a list of all StringVar variables of the process combobox-selections."""
        return [p.process_var for p in self._process_widgets.values()]

    @property
    def note_vars(self) -> List[StringVar]:
        """Returns a list of all StringVar variables for the process notes."""
        return [p.note_var for p in self._process_widgets.values()]

    def add(
        self, process_value: Optional[str] = None, note_value: Optional[str] = None
    ) -> Optional[ProcessWidget]:
        """Adds the process combobox and the process note widgets."""
        new_pid = self._current_pid + 1
        if len(self._process_widgets) <= resource.settings.processes.max - 1:
            widget = ProcessWidget(
                root=self._root,
                pid=new_pid,
                callback_combo=self._callback_combo,
                callback_process=self._callback_process,
            )
            widget.bottom_space = True
            if new_pid > resource.settings.processes.first:
                prev = self.get(pid=new_pid - 1)
                prev.bottom_space = False
                # Only allow the selection of the process if the previous
                # process has been selected. This way we don't have to sort
                # processes later, because there are no 'blank' processes.
                if prev.process_var.get():
                    widget.state = tk.NORMAL
                else:
                    widget.state = tk.DISABLED

            # self._process_widgets.append(w)
            self._process_widgets[new_pid] = widget
            self._current_pid = new_pid

            if process_value:
                widget.process_var.set(process_value)
            if process_value and note_value:
                widget.note_var.set(note_value)

            log.debug(f"Added new process {new_pid}")
            return widget
        return None

    def clear(self, pid: Optional[int] = None) -> None:
        """
        Clears the content of the widgets with the given pid (process id).
        Clears all processes if no pid is provided.

        Args:
        pid (Optional[int], optional): The process id, which widgets have \
            to be cleared. Defaults to None.
        """
        if pid:
            process = self.get(pid)
            process.process_var.set("")
            process.note_var.set("")
        else:
            for widget in self._process_widgets.values():
                widget.process_var.set("")
                widget.note_var.set("")

    def remove(self, pid: int) -> None:
        """
        Removes the process combobox and the process note from the frame.
        All widgets (all processes) are going to be deleted, and re-added,
        except the one with the given pid (process-id). This ensures that
        the tkinter grid will always work.

        Args:
            pid (int): The id of the process which will be deleted.
        """
        process_store: List[str] = []
        note_store: List[str] = []

        # First: Destroy all widgets from the all processes.
        # Store all processes temporarily.
        for i, widget in enumerate(self._process_widgets.values()):
            process_store.append(widget.process_var.get())
            note_store.append(widget.note_var.get())

            widget.lbl_process.grid_forget()
            widget.combo_process.grid_forget()
            widget.text_note_process.grid_forget()

            widget.lbl_process.destroy()
            widget.combo_process.destroy()
            widget.text_note_process.destroy()
            widget.parent.grid_rowconfigure(i * 2 + 1, weight=0)

        # Remove the process which shall be removed from
        # the list from the temporary store.
        process_store.pop(pid - resource.settings.processes.first)
        note_store.pop(pid - resource.settings.processes.first)

        # Clear the process list that holds all widgets.
        self._process_widgets.clear()

        # Reset the pid counter
        self._current_pid = resource.settings.processes.first - 1

        # Add all widgets from the process store.
        # Remember: The process from the given pid isn't in the temp
        # store anymore.
        for i, _ in enumerate(process_store):
            self.add(process_value=process_store[i], note_value=note_store[i])

        # Add all processes from the init_amount, if the amount
        # of remaining processes is less than the init amount.
        for i in range(len(process_store), self._init_amount):
            self.add()

        # Add another widget set, if the current one has a value.
        if process_store[-1]:
            self.add()

        log.debug(f"Removed process {pid}")

    def get(self, pid: int) -> ProcessWidget:
        """
        Returns a process widget by its pid.

        Args:
            pid (int): The pid of the desired ProcessWidget.

        Returns:
            ProcessWidget: The desired ProcessWidget.
        """
        return self._process_widgets[pid]

    def exists(self, pid: int) -> bool:
        """
        Returns wether a pid exists or not.

        Args:
            pid (int): The pid to look for.

        Returns:
            bool: True, if the process exists, False otherwise.
        """
        # return True if len(self._process_widgets) > pid else False
        return bool(pid in self._process_widgets)

    def state(
        self, state: Literal["normal", "disabled"], pid: Optional[int] = None
    ) -> None:
        """
        Sets the state of process widgets. A process widget is only set to state `NORMAL` if the
        previous widget has a value. The state of the process note widgets is set via the
        trace callback of the process widgets StringVar, see method `_callback_process`.

        Args:
            state (Literal[&quot;normal&quot;, &quot;disabled&quot;]): The tkinter-state.
            pid (Optional[int], optional): The pid from which to set the process. \
                If None, all processes will be set to the given state. Defaults to None.
        """
        if pid:
            self.get(pid).state = state
        else:
            for _, widget in enumerate(self._process_widgets.values()):
                if (
                    state == tk.DISABLED
                    or widget.pid == resource.settings.processes.first
                    or (
                        widget.pid > resource.settings.processes.first
                        and self._process_widgets[widget.pid - 1].process_var.get()
                    )
                ):
                    widget.state = state

    def _callback_combo(self, pid: int, value: str) -> None:
        """
        Callback for the process combobox.

         - Removes the widget if the value is None.
         - Adds a following widget if the value is set and no following widget exists yet.
         - Clears the note text widget if the callback value is empty.
         - Adds the process note to the note widget.

        Args:
            pid (int): The pid from which the callback is triggered.
            value (str): The value of the combobox.
        """
        log.debug(f"Callback combobox process: pid={pid}, value={value}")
        process = self._process_widgets[pid]

        if value:
            c = len(self._process_widgets) + resource.settings.processes.first

            # Set the state of the following widget to NORMAL
            if pid + 1 < c:
                self.get(pid + 1).state = tk.NORMAL

            # Adds another widget set
            if pid == c - 1:
                self.add()

            # Ask the user if the note value shall be replaced
            if process.note_var.get():
                use_preset_note = tkmsg.askyesno(
                    title=resource.settings.title,
                    message=(
                        f"There is already a note set for process {pid}.\n\n"
                        "Do you want to replace the current note with a preset?"
                    ),
                )
            else:
                use_preset_note = True

            # Write the preset note value
            if use_preset_note:
                note_value = resource.get_process_note(value)
                meta_value = self._material_meta.get()

                resource_process = resource.get_process_by_name(
                    process.process_var.get()
                )
                metadata_required = (
                    True
                    if resource_process and resource_process.metadata_required
                    else False
                )

                if "$" in note_value and meta_value:
                    note_value = note_value.replace("$", meta_value)
                elif "$" in note_value and metadata_required and not meta_value:
                    tkmsg.showwarning(
                        message=(
                            f"The process {process.process_var.get()} requires metadata.\n\n"
                            "Please select the correct metadata with the material manager. "
                            "To do so, click the 'select' button besides the material input field."
                        )
                    )
                else:
                    note_value = note_value.replace("$", "-")
                process.note_var.set(note_value)
        else:
            # Remove the widget set if the process has no value
            self.remove(pid)

    def _callback_process(self, pid: int, value: str) -> None:
        """
        Callback for the process StringVar trace.

         - Sets the note widget as disabled or normal depending of the value.
         - Sets the state of the following process widgets dependent of the value.

        Args:
            pid (int): The pid from which the trace callback is triggered.
            value (str): The value of the variable.
        """
        log.debug(f"Callback trace process: pid={pid}, value={value}")

        process = self._process_widgets[pid]

        if bool(value):
            process.text_note_process.state = tk.NORMAL
        else:
            process.note_var.set("")
            process.text_note_process.state = tk.DISABLED

        if self.exists(pid=pid + 1):
            self.get(pid + 1).state = tk.NORMAL
