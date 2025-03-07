"""
    Constants for the pytia property manager app.
"""

import os
from enum import Enum
from pathlib import Path

__version__ = "0.7.3"

PYTIA = "pytia"
PYTIA_PROPERTY_MANAGER = "pytia_property_manager"
PYTIA_BOUNDING_BOX = "pytia_bounding_box"

APP_NAME = "PYTIA Property Manager"
APP_VERSION = __version__

LOGON = str(os.environ.get("USERNAME")).lower()
CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
APPDATA = f"{str(os.environ.get('APPDATA'))}\\{PYTIA}\\{PYTIA_PROPERTY_MANAGER}"
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
PID = os.getpid()
PID_FILE = f"{TEMP}\\{PYTIA_PROPERTY_MANAGER}.pid"
PID_FILE_BOUNDING_BOX = f"{TEMP}\\{PYTIA_BOUNDING_BOX}.pid"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = Path(VENV, "Scripts\\python.exe")
VENV_PYTHONW = Path(VENV, "Scripts\\pythonw.exe")
PY_VERSION = APPDATA + "\\pyversion.txt"
REVISION_FOLDER = ".rev"

PROP_DRAWING_PATH = "pytia.drawing_path"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_PROPS = "properties.json"
CONFIG_PROPS_DEFAULT = "properties.default.json"
CONFIG_PROCESSES = "processes.json"
CONFIG_PROCESSES_DEFAULT = "processes.default.json"
CONFIG_INFOS = "information.json"
CONFIG_INFOS_DEFAULT = "information.default.json"
CONFIG_USERS = "users.json"

VERIFY_CRITICAL = "critical"
VERIFY_WARNING = "warning"

WEB_PIP = "https://www.pypi.org"

SUFFIX_DRAWING = ".CATDrawing"

ISO_VIEW = "* iso"

STYLES = [
    "cosmo",
    "litera",
    "flatly",
    "journal",
    "lumen",
    "minty",
    "pulse",
    "sandstone",
    "united",
    "yeti",
    "morph",
    "simplex",
    "cerculean",
    "solar",
    "superhero",
    "darkly",
    "cyborg",
    "vapor",
]


class Source(Enum):
    UNKNOWN = "Unknown"
    MADE = "Made"
    BOUGHT = "Bought"
