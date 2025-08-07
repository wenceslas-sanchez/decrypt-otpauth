import enum


class Algorithm(enum.Enum):
    Unknown = 0
    SHA1 = 1
    SHA256 = 2
    SHA512 = 3
    MD5 = 4

    @property
    def uri_string(self):
        if self == Algorithm.Unknown:
            return "sha1"
        return self.name.lower()
