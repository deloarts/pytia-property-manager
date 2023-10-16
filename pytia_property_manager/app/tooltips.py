"""
    Tooltips submodule for the app.
"""

from app.layout import Layout
from app.vars import Variables
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.widgets.tooltips import ToolTip
from resources import resource


class ToolTips:
    """
    The ToolTips class. Responsible for initializing all tooltips for the main windows widgets.
    """

    def __init__(
        self, layout: Layout, workspace: Workspace, variables: Variables
    ) -> None:
        """
        Inits the ToolTips class.

        Args:
            layout (Layout): The layout of the main window.
            workspace (Workspace): The workspace instance.
            variables (Variables): The variables of the main window.
        """
        # region PARTNUMBER
        ToolTip(
            widget=layout.input_partnumber,
            text=(
                "To change the part number you have to rename the file and execute this app again."
                "\n\nNote: By executing this app the partnumber is always set to the filename."
            ),
        )
        # endregion

        # region PROJECT NUMBER
        if (
            resource.settings.restrictions.strict_project
            and workspace.elements.projects
        ):
            ToolTip(
                widget=layout.input_project,
                text=(
                    "The rule for project numbers is set to 'strict'.\n\n"
                    "You can only use project numbers that are set in the workspace file."
                ),
            )
        elif (
            resource.settings.restrictions.strict_project
            and workspace.available
            and not workspace.elements.projects
        ):
            ToolTip(
                widget=layout.input_project,
                text=(
                    "The rule for project numbers is set to 'strict'.\n\n"
                    "Warning: There are no project numbers set in the workspace file, you are "
                    "allowed to use any project number of your choice. But it is recommended to "
                    "setup the workspace file correctly."
                ),
            )
        elif resource.settings.restrictions.strict_project and not workspace.available:
            ToolTip(
                widget=layout.input_project,
                text=(
                    "The rule for project numbers is set to 'strict'.\n\n"
                    "Warning: No workspace file found. You are allowed to use any project number "
                    "but you should consider setting up the workspace file correctly."
                ),
            )
        # endregion

        # region MACHINE NUMBER
        if resource.settings.restrictions.strict_machine and workspace.elements.machine:
            ToolTip(
                widget=layout.input_machine,
                text=(
                    "The rule for the machine number is set to 'strict'.\n\n"
                    "The machine number is given by the workspace configuration. "
                    "To change the machine number you need to edit the workspace file.\n\n"
                    "Note: An existing machine number in this document will be overwritten with "
                    "the value provided in the workspace file."
                ),
            )
        elif (
            resource.settings.restrictions.strict_machine
            and workspace.available
            and not workspace.elements.machine
        ):
            ToolTip(
                widget=layout.input_machine,
                text=(
                    "The rule for the machine number is set to 'strict'.\n\n"
                    "Warning: No machine number is set in the workspace, you are allowed to use "
                    "any machine number of your choice. But it is recommended to setup the "
                    "workspace file correctly."
                ),
            )
        elif resource.settings.restrictions.strict_machine and not workspace.available:
            ToolTip(
                widget=layout.input_machine,
                text=(
                    "The rule for the machine numbers is set to 'strict'.\n\n"
                    "Warning: No workspace file found. You are allowed to use any machine number "
                    "but you should consider setting up the workspace file correctly."
                ),
            )
        # endregion

        # region SOURCE
        ToolTip(
            layout.button_source,
            (
                "Reloads the partnumber, the definition and the manufacturer from the documents "
                "filename if the source is set to 'bought'.\n\n"
                "Overwrites any existing text of these items."
            ),
        )
        # endregion

        # region CREATOR
        if resource.logon_exists((logon := variables.creator.get())) and (
            creator := resource.get_user_by_logon(logon=logon)
        ):
            ToolTip(
                layout.label_creator,
                (
                    f"Logon: {creator.logon}\n"
                    f"ID: {creator.id}\n"
                    f"Name: {creator.name}\n"
                    f"Mail: {creator.mail}"
                ),
            )
        # endregion

        # region MODIFIER
        if resource.logon_exists((logon := variables.modifier.get())) and (
            modifier := resource.get_user_by_logon(logon=logon)
        ):
            ToolTip(
                layout.label_modifier,
                (
                    f"Logon: {modifier.logon}\n"
                    f"ID: {modifier.id}\n"
                    f"Name: {modifier.name}\n"
                    f"Mail: {modifier.mail}"
                ),
            )
        # endregion

        # region ISO VIEW
        ToolTip(
            layout.toggle_iso_view,
            "Sets the view to ISO and fits in the visible item on save.",
        )
        # endregion

        # region SYNC COLOR
        ToolTip(
            layout.toggle_sync_color,
            (
                "Synchronizes the ambient color from the applied material with the "
                "main body.\n\nIf the main body doesn't have a material applied, the "
                "color will be set to CATIAs default."
                f"{' If the color is too dark it will be brightened up, to prevent visual hurdles.' if resource.settings.min_brightness else ''}"
            ),
        )
        # endregion
