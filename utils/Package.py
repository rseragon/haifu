import json
import platform
import utils.Debug as Debug


PLATFORM_ID = platform.freedesktop_os_release().get("ID", "").lower()
PLATFORM_ID_LIKE = platform.freedesktop_os_release().get("ID_LIKE", "").lower()





class Package(dict):
    """
    The bare bones package info
    Inherited from dict to make it json serializable
    """

    # TODO: Convert into dict?
    def __init__(self, name="", md5="", sha="", deps=None, ver="", arch=""):
        dict.__init__(self, name=name, md5=md5, sha=sha, deps=deps, ver=ver, arch=arch)
        self.name = name
        self.md5 = md5
        self.sha = sha
        self.deps = deps
        self.ver = ver
        self.arch = arch

        # Only for Arch
        self.file_name = f"{self.name}-{self.ver}-{self.arch}.pkg.tar.zst"

    def print(self):
        print(self)

    def filename(self):
        """
        Returns the location of the cached packag
        """
        from pkgman import PackageManager  # Fix circular import
        return PackageManager.pkg_file_name(self)

    def get_pkg_location(self) -> str:
        """
        Returns the package location
        """
        from pkgman import PackageManager # Fix cirular import
        return PackageManager.get_file_location(self)


    def __repr__(self) -> str:
        return f"Package Name: {self.name}\n\
                File   : {self.file_name}\n\
                Arch   : {self.arch}\n\
                Version: {self.ver}\n\
                MD5Hash: {self.md5}\n\
                SHA256 : {self.sha}\n\
                Depends: {str(self.deps)}"

    """
    def toJson(self):
        return {
            "Package Name": self.name,
            "File": self.file_name,
            "Arch": self.arch,
            "Version": self.ver,
            "MD5Hash": self.md5,
            "SHA256": self.sha,
            "Depends": str(self.deps),
        }
    """

    def toJson(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)
