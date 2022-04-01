class Package:
    '''
    The bare bones package info
    '''

    # TODO: Convert into dict?
    def __init__(self, name="", md5="", sha="", deps=[], ver="", arch=""):
        self.name = name
        self.md5  = md5
        self.sha  = sha
        self.deps = deps
        self.ver  = ver
        self.arch = arch

        # Only for Arch
        self.file_name = f"{self.name}-{self.ver}-{self.arch}.pkg.tar.zst"

    def print(self):
        print(f"Package Name: {self.name}\n\
                File   : {self.file_name}\n\
                Arch   : {self.arch}\n\
                Version: {self.ver}\n\
                MD5Hash: {self.md5}\n\
                SHA256 : {self.sha}\n\
                Depends: {str(self.deps)}")

    def filename(self):
        return self.file_name
