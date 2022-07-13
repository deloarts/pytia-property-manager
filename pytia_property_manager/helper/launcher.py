"""
    Helper functions and classes for the UI.
"""

import os
import subprocess
import time
from tkinter import messagebox as tkmsg

from const import CNEXT, PID_FILE_BOUNDING_BOX, PYTIA_BOUNDING_BOX
from pytia.log import log
from resources import resource


def launch_bounding_box_app() -> None:
    """Starts the pytia bounding box application."""
    log.info(f"Running {PYTIA_BOUNDING_BOX} app.")
    path = f"{resource.settings.paths.release}\\{resource.settings.files.bounding_box_launcher}"

    if resource.settings.files.bounding_box_launcher and os.path.exists(path):
        subprocess.Popen(
            [
                f"{resource.settings.paths.catia}\\{CNEXT}",
                "-batch",
                "-macro",
                path,
            ]
        )
        log.info("Waiting for the bounding box app to open...")
        while not os.path.exists(PID_FILE_BOUNDING_BOX):
            time.sleep(1)
        log.info("Waiting for the bounding box app to close...")
        while os.path.exists(PID_FILE_BOUNDING_BOX):
            time.sleep(1)
        log.info(f"The {PYTIA_BOUNDING_BOX} app has been closed.")
    else:
        tkmsg.showinfo(
            title="Launcher",
            message="Cannot launch the bounding box app: The app is not available.",
        )
