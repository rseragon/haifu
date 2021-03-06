"""
Sets up haifu for different OSes
"""

import platform
import os

PLATFORM_ID = platform.freedesktop_os_release().get("ID", "").lower()
PLATFORM_ID_LIKE = platform.freedesktop_os_release().get("ID_LIKE", "").lower()
print(f"[OS] ID: {PLATFORM_ID}")


if PLATFORM_ID_LIKE == "arch" or PLATFORM_ID == "arch":
    os.system("poetry add pyalpm")
    # Install pyalpm
elif PLATFORM_ID == "debian" or PLATFORM_ID_LIKE == "debian":
    os.system("sudo apt install build-essential intltool python-apt python3-dev python3-distutils python3.10-dev python3.10-distutils libapt-pkg-dev") # Install python stubs for debian
    os.system("pip install -r requirements.txt")
elif PLATFORM_ID == "fedora" or PLATFORM_ID_LIKE == "fedora":
    pass
    # python-dnf?
else:
    print("Supports only Arch, debian as of now")

os.system('poetry install')
