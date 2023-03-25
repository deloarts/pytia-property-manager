"""
    Properties submodule for the app.
    Handles the documents properties: Loading, writing, and verifying.
"""

from pathlib import Path

from app.layout import Layout
from app.vars import Variables
from const import PROP_DRAWING_PATH, Source
from helper.lazy_loaders import LazyDocumentHelper
from helper.messages import datafield_message
from helper.translators import translate_nomenclature, translate_source
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource


class Properties:
    """Properties class for handling reading and writing between UI and document."""

    def __init__(
        self,
        layout: Layout,
        lazy_document_helper: LazyDocumentHelper,
        variables: Variables,
        workspace: Workspace,
    ):
        """
        Inits the Properties class.

        Args:
            layout (Layout): The layout of the main app.
            lazy_document_helper (LazyDocumentHelper): The lazy document helper instance.
            variables (Variables): The variables of the main app.
            workspace (Workspace): The workspace instance.
        """
        self.layout = layout
        self.doc_helper = lazy_document_helper
        self.vars = variables
        self.workspace = workspace

    def checkout(self) -> None:
        """Checks out the properties: Writes the values from the UI to the document."""

        log.info("Checking out default properties...")
        # Catia properties
        self.doc_helper.definition = self.vars.definition.get()
        self.doc_helper.revision = self.vars.revision.get()
        self.doc_helper.nomenclature = translate_nomenclature(self.vars.source.get())
        self.doc_helper.source = int(translate_source(self.vars.source.get()))
        self.doc_helper.description = self.vars.description.get()
        log.info("Checked out default properties.")

        log.info("Checking out custom properties...")
        # Custom properties
        self.doc_helper.write_property(
            resource.props.infra.project, self.vars.project.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.machine, self.vars.machine.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.material, self.vars.material.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.base_size, self.vars.base_size.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.base_size_preset,
            self.vars.base_size_preset.get(),
        )
        self.doc_helper.write_property(resource.props.infra.mass, self.vars.mass.get())
        self.doc_helper.write_property(
            resource.props.infra.manufacturer, self.vars.manufacturer.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.supplier, self.vars.supplier.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.tolerance, self.vars.tolerance.get()
        )
        self.doc_helper.write_property(
            resource.props.infra.spare_part_level,
            self.vars.spare_part_level.get(),
        )

        self.doc_helper.write_notes(self.layout.notes)

        self.doc_helper.write_processes(self.layout.processes)
        self.doc_helper.write_process_notes(self.layout.processes)

        self.doc_helper.write_modifier()
        log.info("Checked out custom properties.")

    def verify(self) -> bool:
        """Verifies all properties that need verification. Returns True if everything is ok."""
        critical = []
        warning = []

        log.info("Verifying properties...")

        if (
            self.workspace.elements.projects
            and resource.settings.restrictions.strict_project
            and self.vars.project.get() not in self.workspace.elements.projects
        ):
            critical.append(
                "The selected project number is not in the workspace configuration. "
                "Please select a project number from the dropdown menu."
            )

        if not self.vars.project.get():
            msg = "The project number is not set."
            if resource.settings.verifications.require_project:
                critical.append(msg)
            else:
                warning.append(msg)

        if not self.vars.machine.get():
            msg = "The machine number is not set."
            if resource.settings.verifications.require_machine:
                critical.append(msg)
            else:
                warning.append(msg)

        if not self.vars.revision.get():
            msg = "The revision number is not set."
            if resource.settings.verifications.require_revision:
                critical.append(msg)
            else:
                warning.append(msg)

        match self.vars.source.get():
            case Source.MADE.value:
                if not self.vars.material.get() and self.doc_helper.is_part:
                    warning.append("No material was applied to the part.")
                if not self.layout.processes.get(
                    resource.settings.processes.first
                ).process_var.get():
                    warning.append("No process is selected.")
            case Source.BOUGHT.value:
                if not self.vars.definition.get():
                    critical.append("The definition is not set.")
                if not self.vars.manufacturer.get():
                    critical.append("The manufacturer is not set.")

        if any(critical):
            datafield_message(critical, critical=True)
            log.warning(f"Failed verifying properties: {', '.join(critical)}")
            return False

        if any(warning):
            if datafield_message(warning, critical=False) != "yes":
                log.warning(f"Failed verifying properties: {', '.join(warning)}")
                return False

        log.info("Successfully verified properties.")
        return True

    def retrieve(self) -> None:
        """Loads the properties from the document into the UI via the main apps variables."""
        log.info("Retrieving properties from the document...")
        self.doc_helper.setvar_combo_property(
            variable=self.vars.project,
            property_name=resource.props.infra.project,
            widget=self.layout.input_project,
            default=self.workspace.elements.projects[0]
            if self.workspace.elements.projects
            else None,
            items=self.workspace.elements.projects,
        )

        if (
            resource.settings.restrictions.strict_machine
            and self.workspace.elements.machine
        ):
            self.doc_helper.setvar(
                variable=self.vars.machine,
                value=self.workspace.elements.machine,
            )
        else:
            self.doc_helper.setvar_property(
                self.vars.machine,
                resource.props.infra.machine,
                default=self.workspace.elements.machine,
            )

        self.doc_helper.setvar_material(self.vars.material, self.vars.material_meta)
        self.doc_helper.setvar_property(
            self.vars.base_size, resource.props.infra.base_size
        )
        self.doc_helper.setvar_property(
            self.vars.base_size_preset, resource.props.infra.base_size_preset
        )
        self.doc_helper.setvar_mass(self.vars.mass)
        self.doc_helper.setvar_property(
            self.vars.manufacturer, resource.props.infra.manufacturer
        )
        self.doc_helper.setvar_property(
            self.vars.supplier, resource.props.infra.supplier
        )
        self.doc_helper.setvar_combo_property(
            variable=self.vars.tolerance,
            property_name=resource.props.infra.tolerance,
            widget=self.layout.input_tolerance,
        )
        self.doc_helper.setvar_property(
            self.vars.spare_part_level, resource.props.infra.spare_part_level
        )
        self.doc_helper.setvar_user(self.vars.creator, resource.props.infra.creator)
        self.doc_helper.setvar_user(self.vars.modifier, resource.props.infra.modifier)

        self.doc_helper.setvar_property(self.vars.linked_doc, PROP_DRAWING_PATH)

        self.doc_helper.setvar_notes(self.layout.notes)

        self.doc_helper.setvar_process(self.layout.processes)
        self.doc_helper.setvar_process_notes(self.layout.processes)

        # Default properties
        # We retrieve the default catia properties after the user properties, because the source
        # property has a trace, which set the state of the UI.
        self.doc_helper.setvar(self.vars.partnumber, self.doc_helper.partnumber)
        self.doc_helper.setvar(self.vars.definition, self.doc_helper.definition)
        self.doc_helper.setvar(
            self.vars.revision,
            self.doc_helper.revision,
            default=resource.settings.revision,
        )
        self.doc_helper.setvar(
            self.vars.source, translate_source(self.doc_helper.source)
        )
        self.doc_helper.setvar(self.vars.description, self.doc_helper.description)

        log.info("Retrieved all properties.")
