"""
Sets up haifu for different OSes
"""

import platform
import os
from utils.Debug import Debug

PLATFORM_ID = platform.freedesktop_os_release().get("ID", "").lower()
PLATFORM_ID_LIKE = platform.freedesktop_os_release().get("ID_LIKE", "").lower()
Debug.debug(f"[OS] ID: {PLATFORM_ID}")

if PLATFORM_ID_LIKE == "arch" or PLATFORM_ID == "arch":
    os.system("poetry add pyalpm")
    # Install pyalpm
elif PLATFORM_ID == "debian" or PLATFORM_ID_LIKE == "debian":
    pass
    # Install python-apt
elif PLATFORM_ID == "fedora" or PLATFORM_ID_LIKE == "fedora":
    pass
    # python-dnf?
else:
    Debug.error(1, "Supports only Arch as of now")

