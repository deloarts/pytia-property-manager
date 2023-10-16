"""
    Lazy loader for the UI.
"""

import functools
import os
import re
import time
from dataclasses import asdict
from pathlib import Path
from tkinter import StringVar
from tkinter import messagebox as tkmsg
from tkinter import ttk
from typing import List
from typing import Optional

from app.vars import Variables
from app.widgets.notes import NoteWidgets
from app.widgets.processes import ProcessWidgets
from const import ISO_VIEW
from const import LOGON
from const import REVISION_FOLDER
from const import Source
from helper.values import set_perceived_brightness
from pytia.exceptions import PytiaDifferentDocumentError
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.exceptions import PytiaWrongDocumentTypeError
from pytia.log import log
from resources import resource


class LazyDocumentHelper:
    """
    Helper class for late imports of any kind of methods related to handle document operations.

    Important: This class loads the current document only once (on instantiation). If the
    document changes all operations will be made on the original document.

    Use the ensure_doc_not_changed method if you're not sure if the part hasn't changed.
    """

    def __init__(self) -> None:
        # Import the PyPartDocument after the GUI exception handler is initialized.
        # Otherwise the CATIA-not-running-exception will not be caught.
        # Also: The UI will load a little bit faster.

        start_time = time.perf_counter()
        # pylint: disable=C0415
        from pytia.framework import framework

        # pylint: enable=C0415

        self.framework = framework
        self.lazy_document = framework.catia.active_document
        self.is_part = self.lazy_document.is_part
        self.is_document = self.lazy_document.is_product

        # FIXME: Locking CATIA disables the change-detection.
        # self._lock_catia(True)
        # atexit.register(lambda: self._lock_catia(False))

        if not resource.settings.restrictions.allow_unsaved and not os.path.isabs(
            self.lazy_document.full_name
        ):
            raise PytiaDocumentNotSavedError(
                "It is not allowed to edit the parameters of an unsaved document. "
                "Please save the document first."
            )

        if self.lazy_document.is_part:
            # pylint: disable=C0415
            from pytia.wrapper.documents.part_documents import PyPartDocument

            # pylint: enable=C0415

            self.document = PyPartDocument(
                strict_naming=False, material_link=resource.settings.link_material
            )
            log.debug("Current document is a CATPart.")

        elif self.lazy_document.is_product:
            # pylint: disable=C0415
            from pytia.wrapper.documents.product_documents import PyProductDocument

            # pylint: enable=C0415

            self.document = PyProductDocument(
                strict_naming=False, material_link=resource.settings.link_material
            )
            log.debug("Current document is a CATProduct.")

        else:
            raise PytiaWrongDocumentTypeError(
                "The current document is neither a part nor a product."
            )

        end_time = time.perf_counter()
        log.debug(f"Loaded PyPartDocument in {(end_time-start_time):.4f}s")

        self.document.current()
        self.document.product.part_number = self.document.document.name.split(".CATP")[
            0
        ]
        self.name = self.document.document.name

        if REVISION_FOLDER in self.document.document.full_name:
            raise PytiaWrongDocumentTypeError(
                "You opened a document from the revision folder. "
                "It's not allowed to modify documents from this folder."
            )

    @property
    def path(self) -> Path:
        """Returns the documents absolute path with filename and file extension."""
        return Path(self.document.document.full_name)

    @property
    def folder(self) -> Path:
        """Returns the folder as absolute path in which this document is saved."""
        return Path(self.path).parent

    @property
    def partnumber(self) -> str:
        """Returns the part number of the document."""
        return self.document.product.part_number

    @property
    def definition(self) -> str:
        """Returns the definition of the document."""
        return self.document.product.definition

    @definition.setter
    def definition(self, value: str) -> None:
        """Sets the definition value of the document."""
        self.document.product.definition = value

    @property
    def revision(self) -> str:
        """Returns the revision of the document."""
        return self.document.product.revision

    @revision.setter
    def revision(self, value: str) -> None:
        """Sets the revision value of the document."""
        self.document.product.revision = value

    @property
    def nomenclature(self) -> str:
        """Returns the nomenclature of the document"""
        return self.document.product.nomenclature

    @nomenclature.setter
    def nomenclature(self, value: str) -> None:
        """Sets the nomenclature value of the document."""
        self.document.product.nomenclature = value

    @property
    def source(self) -> int:
        """Returns the source of the document."""
        return self.document.product.source

    @source.setter
    def source(self, value: int) -> None:
        """Sets the source value of the document."""
        self.document.product.source = value

    @property
    def description(self) -> str:
        """Returns the description of the document"""
        return self.document.product.description_reference

    @description.setter
    def description(self, value: str) -> None:
        """Returns the description value of the document."""
        self.document.product.description_reference = value

    def _lock_catia(self, value: bool) -> None:
        """
        Sets the lock-state of catia.

        Args:
            value (bool): True: Locks the catia UI, False: Releases the lock.
        """
        log.debug(f"Setting catia lock to {value!r}")
        self.framework.catia.refresh_display = not value
        self.framework.catia.interactive = not value
        self.framework.catia.display_file_alerts = value
        self.framework.catia.undo_redo_lock = value
        if value:
            self.framework.catia.disable_new_undo_redo_transaction()
        else:
            self.framework.catia.enable_new_undo_redo_transaction()

    def _doc_changed(self) -> bool:
        """Returns True if the current part document has changed, False if not."""
        part_document = self.document
        part_document.current()
        log.warning(
            f"The document has changed: {part_document.document.name} -> {self.name}"
        )
        return part_document.document.name != self.name

    def get_all_open_documents(self) -> List[str]:
        """Returns a list of all open documents (document.name)"""
        open_documents: List[str] = []
        for i in range(1, self.framework.catia.documents.count + 1):
            open_documents.append(self.framework.catia.documents.item(i).name)
        return open_documents

    def get_all_open_windows(self) -> List[str]:
        """Returns a list of all open windows"""
        open_windows: List[str] = []
        for i in range(1, self.framework.catia.windows.count + 1):
            open_windows.append(self.framework.catia.windows.item(i).name)
        return open_windows

    def setup_main_body(self, variables: Variables) -> None:
        """
        Sets up the main body of the document (if the document is a part document).
        Sets the main body as "in work object" and sets the name of the main body depending
        on the source.

        Args:
            variables (Variables): The variables of the main app.
        """
        # pylint: disable=C0415
        from pytia.wrapper.documents.part_documents import PyPartDocument

        # pylint: enable=C0415

        if isinstance(self.document, PyPartDocument):
            log.info("Setting the main bodies name...")

            self.document.part.in_work_object = self.document.bodies.main_body

            # The main body name depends on the source of the document.
            match variables.source.get():
                case Source.MADE.value:
                    # Set the main body name
                    if variables.machine.get() != "":
                        main_body_name = (
                            f"{variables.machine.get()}"
                            " - "
                            f"{variables.partnumber.get()}"
                            " - Rev"
                            f"{variables.revision.get()}"
                        )
                    else:
                        main_body_name = variables.partnumber.get()

                    # Set the main body color
                    if resource.appdata.sync_color:
                        try:
                            rgb = set_perceived_brightness(
                                self.document.material.rendering_material.get_ambient_color(),
                                resource.settings.min_brightness or 0,
                            )
                        except AttributeError:
                            rgb = (210, 210, 255)

                        selection = self.document.document.selection
                        selection.clear()
                        selection.add(self.document.bodies.main_body)
                        selection.vis_properties.set_real_color(
                            rgb[0], rgb[1], rgb[2], 1
                        )
                        selection.clear()
                        log.info(f"Set main body color to RGB {rgb}.")

                case Source.BOUGHT.value | _:
                    main_body_name = variables.partnumber.get()

            self.document.bodies.main_body.name = main_body_name

    def set_view(self) -> None:
        """Sets the view for the document and fits it."""
        try:
            viewer = self.framework.catia.active_window.active_viewer
            camera = self.framework.catia.active_document.cameras.item(ISO_VIEW)

            # FIXME: pytia v0.3.5 has no type for Viewpoint3D.
            viewer.viewer.Viewpoint3D = camera.camera.Viewpoint3D

            viewer.update()
            viewer.reframe()
        except Exception as e:
            msg = "Failed to set ISO view."
            tkmsg.showwarning(title=resource.settings.title, message=msg)
            log.error(f"{msg} {e}")

    @staticmethod
    def _ensure_doc_not_changed(func):
        """
        Ensures that the document hasn't changed.
        Raises the PytiaDifferentDocumentError if the document has changed.
        """

        # pylint: disable=W0212
        # pylint: disable=R1710
        @functools.wraps(func)
        def _ensure_part_not_changed_wrapper(self, *args, **kwargs):
            if self._doc_changed():
                document = self.document
                document.current()
                raise PytiaDifferentDocumentError(
                    f"The name of the current document has changed:\n"
                    f" - Original was {self.name}\n"
                    f" - Current is {document.document.name}"
                )
            return func(self, *args, **kwargs)

        return _ensure_part_not_changed_wrapper
        # pylint: enable=W0212
        # pylint: enable=R1710

    # @_ensure_doc_not_changed
    def get_property(self, name: str) -> Optional[str]:
        """
        Retrieves a properties value from the documents properties.

        Args:
            name (str): The name of the property to retrieve the value from.

        Returns:
            Optional[str]: The value of the property as string. Returns None, if the property \
                doesn't exists.
        """
        if self.document.properties.exists(name):
            param = str(self.document.properties.get_by_name(name).value)
            log.info(f"Retrieved property {name} ({param}) from part.")
            return param
        log.info(f"Couldn't retrieve property {name} from part: Doesn't exists.")
        return None

    # @_ensure_doc_not_changed
    def write_property(self, name: str, value: str) -> None:
        """
        Writes the property to the documents properties. Deletes properties with empty values.

        Args:
            name (str): The name of the property.
            value (str): The value of the property.
        """

        if self.document.properties.exists(name):
            if value:
                self.document.properties.set_value(name, value)
                log.info(f"Wrote property {name!r} with value {value!r}.")
            else:
                self.document.properties.delete(name)
        else:
            if value:
                self.document.properties.create(name, value)
            else:
                log.debug(f"Didn't write property {name!r}: Value is empty.")

    # @_ensure_doc_not_changed
    def write_modifier(self, write_creator: bool = True) -> None:
        """
        Saves the modifier to the documents properties.

        Args:
            write_creator (bool, optional): Also write the creator. Defaults to True.
        """
        self.write_property(resource.props.infra.modifier, LOGON)
        if not self.get_property(resource.props.infra.creator) and write_creator:
            self.write_property(resource.props.infra.creator, LOGON)

    def write_notes(self, notes: NoteWidgets) -> None:
        """
        Writes the notes from the notes-widgets to the documents properties.

        Args:
            notes (NoteWidgets): The notes-widgets object.
        """
        for key, value in asdict(resource.props.notes).items():
            note = notes.get(key)
            self.write_property(name=value, value=note.note_var.get())

    def write_processes(self, processes: ProcessWidgets) -> None:
        """
        Writes the processes from the processes-widgets to the documents properties.

        Args:
            processes (ProcessWidgets): The processes-widgets object.
        """
        for i in range(
            resource.settings.processes.first,
            resource.settings.processes.max + resource.settings.processes.first,
        ):
            property_name = resource.props.production.process_n.replace("$", str(i))
            if processes.exists(pid=i):
                self.write_property(
                    property_name, processes.get(pid=i).process_var.get()
                )
            else:
                self.write_property(property_name, "")

    def write_process_notes(self, processes: ProcessWidgets) -> None:
        """
        Writes the process-notes from the processes-widgets to the documents properties.

        Args:
            processes (ProcessWidgets): The processes-widgets object.
        """
        for i in range(
            resource.settings.processes.first,
            resource.settings.processes.max + resource.settings.processes.first,
        ):
            property_name = resource.props.production.note_process_n.replace(
                "$", str(i)
            )
            if processes.exists(pid=i):
                self.write_property(property_name, processes.get(pid=i).note_var.get())
            else:
                self.write_property(property_name, "")

    @staticmethod
    def setvar(
        variable: StringVar,
        value: str | int | None,
        default: Optional[str | int] = None,
    ) -> None:
        """
        Sets the value of a tkinter variable. Omits None values. Omits empty string or
        whitespace-only-strings. All values will be casted to str.

        Args:
            variable (StringVar | IntVar): The tkinter variable.
            value (str | int | None): The value.
            default (Optional[str | int], optional): The default value, if the value is None.
        """
        if re.match(r"^\s+$", str(value)):
            value = None

        if value or isinstance(default, int | str):
            variable.set(str(value or default))
            log.info(f"Set value '{value or default}' for variable '{variable}'")

    def setvar_property(
        self,
        variable: StringVar,
        property_name: str,
        default: Optional[str | int] = None,
    ) -> None:
        """
        Sets the value of a tkinter variable. Fetches the value from the documents property,
        which name matches the given property_name. Omits None values.

        Args:
            variable (StringVar | IntVar): The tkinter variable.
            property_name (str): The name of the property, from which the value will be fetched.
            default (Optional[str | int], optional): The default value, if the value is None.
        """
        self.setvar(
            variable=variable, value=self.get_property(property_name), default=default
        )

    def setvar_combo_property(
        self,
        variable: StringVar,
        property_name: str,
        widget: ttk.Combobox,
        default: Optional[str | int] = None,
        items: Optional[List[str]] = None,
    ) -> None:
        """
        Sets the value of a tkinter variable. Fetches the value from the documents property,
        which name matches the given property_name. Omits None values.

        Args:
            variable (StringVar | IntVar): The tkinter variable.
            property_name (str): The name of the property, from which the value will be fetched.
            widget (Combobox): The widget where the variable will be added.
            default (Optional[str | int], optional): The default value, if the value is None.
            items (Optional[List[str]], optional): A list of items that will be added to the widget.
        """
        self.setvar(
            variable=variable, value=self.get_property(property_name), default=default
        )
        if items:
            widget.configure(values=items)

    def setvar_user(self, variable: StringVar, property_name: str) -> None:
        """
        Sets the value of a tkinter variable. Fetches the value from the documents property,
        which name matches the given property_name. Only use this for User-variables.

        Args:
            variable (StringVar): The tkinter variable.
            property_name (str): The name of the property, from which the value will be fetched.
        """
        value = self.get_property(property_name) or LOGON
        self.setvar(variable=variable, value=value)

    def setvar_mass(self, variable: StringVar, force: bool = False) -> None:
        """
        Sets the value of a tkinter variable. Adds the unit 'kg' to the value. Only use this for
        mass-related variables.

        Args:
            variable (StringVar): The tkinter variable.
            force (bool, optional): Force writing the mass. Defaults to False.
        """
        if self.is_part or force:
            mass = round(self.document.product.analyze.mass, 2)
            variable.set(f"{mass} kg")

    def setvar_material(self, variable: StringVar, metadata: StringVar) -> None:
        """
        Sets the value of a tkinter variable. Only use this for material-related variables.
        Writes the applied material to the UI, overwrites any existing material (retrieved from the
        properties) -> The material applied to the document is always preferred.

        Args:
            variable (StringVar): The material variable.
            metadata (StringVar): The material metadata variable.
        """
        # pylint: disable=C0415
        if self.is_part:
            from pytia.utilities.material import get_material_from_part as get_material
        else:
            from pytia.utilities.material import (
                get_material_from_product as get_material,
            )
        # pylint: enable=C0415
        if applied_material := get_material():
            if resource.settings.separators.metadata in applied_material:
                splitted = applied_material.split(resource.settings.separators.metadata)
                applied_material = splitted[0]
                metadata.set(splitted[1])
            variable.set(applied_material)

    def setvar_notes(self, notes: NoteWidgets) -> None:
        """
        Sets the value of all notes-tkinter variables.

        Args:
            notes (NoteWidgets): The note widgets object.
        """
        for key, value in asdict(resource.props.notes).items():
            note = notes.get(key)
            self.setvar_property(variable=note.note_var, property_name=value)

    def setvar_process(self, processes: ProcessWidgets) -> None:
        """
        Sets the value of all processes-tkinter variables.

        Args:
            notes (NoteWidgets): The process widgets object.
        """
        index = resource.settings.processes.first

        while True:
            process_name = resource.props.production.process_n.replace("$", str(index))

            if self.document.properties.exists(process_name):
                if not processes.exists(pid=index):
                    processes.add()
                process = processes.get(pid=index)

                self.setvar_property(
                    variable=process.process_var, property_name=process_name
                )
                index += 1
            else:
                break

        if not processes.exists(pid=index):
            processes.add()

    def setvar_process_notes(self, processes: ProcessWidgets) -> None:
        """
        Sets the value of all processes-notes-tkinter variables.

        Args:
            notes (NoteWidgets): The process widgets object.
        """
        index = resource.settings.processes.first

        while True:
            process_name = resource.props.production.process_n.replace("$", str(index))
            note_name = resource.props.production.note_process_n.replace(
                "$", str(index)
            )

            # Ignore notes for non-existent processes
            if self.document.properties.exists(process_name) and processes.exists(
                pid=index
            ):
                if self.document.properties.exists(note_name):
                    process = processes.get(pid=index)
                    self.setvar_property(
                        variable=process.note_var, property_name=note_name
                    )
                index += 1
            else:
                break
