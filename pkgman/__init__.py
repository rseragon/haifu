import platform


PLATFORM_ID = platform.freedesktop_os_release().get("ID", "").lower()
PLATFORM_ID_LIKE = platform.freedesktop_os_release().get("ID_LIKE", "").lower()

if PLATFORM_ID_LIKE == "arch" or PLATFORM_ID == "arch":
    import pkgman.pacman as PackageManager
    # Install pyalpm
elif PLATFORM_ID == "debian" or PLATFORM_ID_LIKE == "debian":
    import pkgman.deb_apt as PackageManager
    # Install python-apt
elif PLATFORM_ID == "fedora" or PLATFORM_ID_LIKE == "fedora":
    pass
    # python-dnf?
else:
    Debug.error(1, "Supports only Arch, Debian as of now")

