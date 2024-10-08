"""
    Loads the content from config files.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import atexit
import importlib.resources
import json
import os
import tkinter.messagebox as tkmsg
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from pathlib import Path
from typing import List
from typing import Literal
from typing import Optional

from const import APP_VERSION
from const import APPDATA
from const import CONFIG_APPDATA
from const import CONFIG_INFOS
from const import CONFIG_INFOS_DEFAULT
from const import CONFIG_PROCESSES
from const import CONFIG_PROCESSES_DEFAULT
from const import CONFIG_PROPS
from const import CONFIG_PROPS_DEFAULT
from const import CONFIG_SETTINGS
from const import CONFIG_USERS
from const import LOGON
from const import STYLES
from resources.utils import expand_env_vars


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsRestrictions:
    """Dataclass for restrictive settings."""

    allow_all_users: bool
    allow_all_editors: bool
    allow_unsaved: bool
    allow_outside_workspace: bool
    strict_project: bool
    strict_product: bool
    enable_information: bool


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsVerificationsBasic:
    """Dataclass for basic property verification settings."""

    project: Literal["critical", "warning"] | None
    product: Literal["critical", "warning"] | None
    revision: Literal["critical", "warning"] | None
    group: Literal["critical", "warning"] | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsVerificationsMade:
    """Dataclass for made property verification settings."""

    order_number: Literal["critical", "warning"] | None
    material: Literal["critical", "warning"] | None
    process_1: Literal["critical", "warning"] | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsVerificationsBought:
    """Dataclass for bought property verification settings."""

    order_number: Literal["critical", "warning"] | None
    manufacturer: Literal["critical", "warning"] | None
    supplier: Literal["critical", "warning"] | None


@dataclass(slots=True, kw_only=True)
class SettingsVerifications:
    """Dataclass for property verification settings."""

    basic: SettingsVerificationsBasic
    made: SettingsVerificationsMade
    bought: SettingsVerificationsBought

    def __post_init__(self) -> None:
        self.basic = SettingsVerificationsBasic(**dict(self.basic))  # type: ignore
        self.made = SettingsVerificationsMade(**dict(self.made))  # type: ignore
        self.bought = SettingsVerificationsBought(**dict(self.bought))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsSeparators:
    """Dataclass for separators."""

    bought: str
    metadata: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsNomenclature:
    """Dataclass for nomenclature."""

    made: str
    bought: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsProcesses:
    """Dataclass for min and max values."""

    first: int
    min: int
    max: int


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsAutoDefinition:
    """Dataclass for auto definition calculation."""

    enable: bool
    prefix: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsAutoGroup:
    """Dataclass for conditional groups."""

    # TODO: Move this to the workspace file.

    made: str | None
    bought: str | None


@dataclass(slots=True, kw_only=True)
class SettingsPaths:
    """Dataclass for paths (settings.json)."""

    catia: Path
    material: Path
    release: Path

    def __post_init__(self) -> None:
        self.catia = Path(expand_env_vars(str(self.catia)))
        self.material = Path(expand_env_vars(str(self.material)))
        self.release = Path(expand_env_vars(str(self.release)))


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsFiles:
    """Dataclass for files (settings.json)."""

    app: str
    launcher: str
    bounding_box_launcher: Optional[str]
    material: str
    workspace: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsUrls:
    """Dataclass for urls (settings.json)."""

    help: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsMails:
    """Dataclass for mails (settings.json)."""

    admin: str


@dataclass(slots=True, kw_only=True)
class Settings:  # pylint: disable=R0902
    """Dataclass for settings (settings.json)."""

    title: str
    debug: bool
    demo: bool
    link_material: bool
    min_brightness: int | None
    revision: int | str
    restrictions: SettingsRestrictions
    verifications: SettingsVerifications
    separators: SettingsSeparators
    nomenclature: SettingsNomenclature
    processes: SettingsProcesses
    auto_definition: SettingsAutoDefinition
    auto_group: SettingsAutoGroup
    tolerances: List[str]
    spare_part_level: List[str]
    files: SettingsFiles
    paths: SettingsPaths
    urls: SettingsUrls
    mails: SettingsMails

    def __post_init__(self) -> None:
        self.restrictions = SettingsRestrictions(**dict(self.restrictions))  # type: ignore
        self.verifications = SettingsVerifications(**dict(self.verifications))  # type: ignore
        self.separators = SettingsSeparators(**dict(self.separators))  # type: ignore
        self.nomenclature = SettingsNomenclature(**dict(self.nomenclature))  # type: ignore
        self.processes = SettingsProcesses(**dict(self.processes))  # type: ignore
        self.auto_definition = SettingsAutoDefinition(**dict(self.auto_definition))  # type: ignore
        self.auto_group = SettingsAutoGroup(**dict(self.auto_group))  # type: ignore
        self.files = SettingsFiles(**dict(self.files))  # type: ignore
        self.paths = SettingsPaths(**dict(self.paths))  # type: ignore
        self.urls = SettingsUrls(**dict(self.urls))  # type: ignore
        self.mails = SettingsMails(**dict(self.mails))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class PropsInfra:
    """Dataclass for infrastructure properties on the document (properties.json)."""

    project: str
    product: str
    material: str
    base_size: str
    base_size_preset: str
    mass: str
    order_number: str
    manufacturer: str
    supplier: str
    weblink: str
    group: str
    tolerance: str
    spare_part_level: str
    creator: str
    modifier: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the PropsInfra dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the PropsInfra dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class PropsNotes:
    """Dataclass for note properties on the document (properties.json)."""

    general: str
    material: str
    base_size: str
    supplier: str
    production: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the PropsNotes dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the PropsNotes dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class PropsProduction:
    """Dataclass for production properties on the document (properties.json)."""

    process_n: str
    note_process_n: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the PropsProduction dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the PropsProduction dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True)
class Props:
    """Dataclass for properties on the document (properties.json)."""

    infra: PropsInfra
    notes: PropsNotes
    production: PropsProduction

    def __post_init__(self) -> None:
        self.infra = PropsInfra(**dict(self.infra))  # type: ignore
        self.notes = PropsNotes(**dict(self.notes))  # type: ignore
        self.production = PropsProduction(**dict(self.production))  # type: ignore

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the Props dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the Props dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class Process:
    """Dataclass for the process to preset conversion (processes.json)."""

    name: str
    note: Optional[str]
    metadata_required: Optional[bool]

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the Process dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the Process dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class User:
    """Dataclass a user (users.json)."""

    logon: str
    id: str
    name: str
    mail: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the User dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the User dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class Info:
    """Dataclass for an info messages (information.json)."""

    counter: int
    msg: str


@dataclass(slots=True, kw_only=True, frozen=True)
class Links:
    """TODO: Dataclass for bought parts-links."""


@dataclass(slots=True, kw_only=True)
class AppData:
    """Dataclass for appdata settings."""

    version: str = field(default=APP_VERSION)
    counter: int = 0
    theme: str = STYLES[0]
    set_view: bool = True
    sync_color: bool = True

    def __post_init__(self) -> None:
        self.version = (
            APP_VERSION  # Always store the latest version in the appdata json
        )
        self.counter += 1


class Resources:  # pylint: disable=R0902
    """Class for handling resource files."""

    __slots__ = (
        "_settings",
        "_props",
        "_processes",
        "_users",
        "_infos",
        "_appdata",
    )

    def __init__(self) -> None:
        self._read_settings()
        self._read_props()
        self._read_users()
        self._read_processes()
        self._read_infos()
        self._read_appdata()

        atexit.register(self._write_appdata)

    @property
    def settings(self) -> Settings:
        """settings.json"""
        return self._settings

    @property
    def props(self) -> Props:
        """properties.json"""
        return self._props

    @property
    def processes(self) -> List[Process]:
        """processes.json"""
        return self._processes

    @property
    def users(self) -> List[User]:
        """users.json"""
        return self._users

    @property
    def infos(self) -> List[Info]:
        """infos.json"""
        return self._infos

    @property
    def appdata(self) -> AppData:
        """Property for the appdata config file."""
        return self._appdata

    def _read_settings(self) -> None:
        """Reads the settings json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_SETTINGS) as f:
            self._settings = Settings(**json.load(f))

    def _read_users(self) -> None:
        """Reads the users json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_USERS) as f:
            self._users = [User(**i) for i in json.load(f)]

    def _read_props(self) -> None:
        """Reads the props json from the resources folder."""
        props_resource = (
            CONFIG_PROPS
            if importlib.resources.is_resource("resources", CONFIG_PROPS)
            else CONFIG_PROPS_DEFAULT
        )
        with importlib.resources.open_binary("resources", props_resource) as f:
            self._props = Props(**json.load(f))

    def _read_processes(self) -> None:
        """Reads the processes json from the resources folder."""
        processes_resource = (
            CONFIG_PROCESSES
            if importlib.resources.is_resource("resources", CONFIG_PROCESSES)
            else CONFIG_PROCESSES_DEFAULT
        )
        with importlib.resources.open_binary("resources", processes_resource) as f:
            self._processes = [Process(**i) for i in json.load(f)]

    def _read_infos(self) -> None:
        """Reads the information json from the resources folder."""
        infos_resource = (
            CONFIG_INFOS
            if importlib.resources.is_resource("resources", CONFIG_INFOS)
            else CONFIG_INFOS_DEFAULT
        )
        with importlib.resources.open_binary("resources", infos_resource) as f:
            self._infos = [Info(**i) for i in json.load(f)]

    def _read_appdata(self) -> None:
        """Reads the json config file from the appdata folder."""
        if os.path.exists(appdata_file := f"{APPDATA}\\{CONFIG_APPDATA}"):
            with open(appdata_file, "r", encoding="utf8") as f:
                try:
                    value = AppData(**json.load(f))
                except Exception:
                    value = AppData()
                    tkmsg.showwarning(
                        title="Configuration warning",
                        message="The AppData config file has been corrupted. \
                            You may need to apply your preferences again.",
                    )
                self._appdata = value
        else:
            self._appdata = AppData()

    def _write_appdata(self) -> None:
        """Saves appdata config to file."""
        os.makedirs(APPDATA, exist_ok=True)
        with open(f"{APPDATA}\\{CONFIG_APPDATA}", "w", encoding="utf8") as f:
            json.dump(asdict(self._appdata), f)

    def get_user_by_logon(self, logon: Optional[str] = None) -> User:
        """
        Returns the user dataclass that matches the logon value. Returns the User of the current
        session if logon is omitted.

        Args:
            logon (Optional[str]): The user to fetch from the dataclass list.

        Raises:
            PytiaValueError: Raised when the user doesn't exist.

        Returns:
            User: The user from the dataclass list that matches the provided logon name.
        """
        if logon is None:
            logon = LOGON

        for index, value in enumerate(self._users):
            if value.logon == logon:
                return self._users[index]
        raise ValueError(f"The user {logon} does not exist.")

    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Returns the user dataclass that matches the name.

        Args:
            name (str): The username to fetch from the dataclass list.

        Returns:
            User: The user from the dataclass list that matches the provided name.
        """
        for index, value in enumerate(self._users):
            if value.name == name:
                return self._users[index]
        return None

    def logon_exists(self, logon: Optional[str] = None) -> bool:
        """
        Returns wether the users logon exists in the dataclass, or not. Uses the logon-value of the
        current session if logon is omitted.

        Args:
            logon (str): The logon name to search for.

        Returns:
            bool: The user from the dataclass list that matches the provided logon name.
        """
        if logon is None:
            logon = LOGON

        for user in self._users:
            if user.logon == logon:
                return True
        return False

    def get_info_msg_by_counter(self) -> List[str]:
        """
        Returns the info message by the app usage counter.

        Returns:
            List[str]: A list of all messages that should be shown at the counter value.
        """
        values = []
        for index, value in enumerate(self._infos):
            if value.counter == self._appdata.counter:
                values.append(self._infos[index].msg)
        return values

    def get_process_by_name(self, name: str) -> Optional[Process]:
        """
        Returns the process dataclass that matches the name.

        Args:
            name (str): The process name to fetch from the dataclass list.

        Returns:
            User: The process from the dataclass list that matches the provided name.
        """
        for index, value in enumerate(self._processes):
            if value.name == name:
                return self._processes[index]
        return None

    def get_process_note(self, name: str) -> str:
        """
        Retrieves the note of the given process name.

        Args:
            name (str): The name of the process.

        Returns:
            str: The note of the process.

        Raises:
            PytiaValueError: Raised if the name is not in the list of processes.
        """
        for item in self._processes:
            if item.name == name:
                return item.note if item.note else ""
        raise ValueError(f"No process found with name {name}.")


resource = Resources()
