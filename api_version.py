class InvalidVersionString(Exception):
    pass

class APIVersion(object):
    """
    This class represents an API Version with convenience
    methods for manipulation and comparison of version
    numbers that we need to do to implement microversions.
    """

    def __init__(self, version_string=None):
        """
        Create an API version object.
        """
        self.ver_major = None
        self.ver_minor = None

        if version_string:
            ver_array = version_string.split('.')
            if len(ver_array) != 2:
                raise InvalidVersionString()
            try:
                self.ver_major = int(ver_array[0])
                self.ver_minor = int(ver_array[1])
            except ValueError:
                raise InvalidVersionString()

    def __str__(self):
        """String representation just for debugging purposes"""
        return "Major: %s, Minor: %s" % (self.ver_major, self.ver_minor)

    def is_null(self):
        return self.ver_major is None and self.ver_minor is None

    def __cmp__(self, other):
        if self.ver_major < other.ver_major:
            return -1
        elif self.ver_major == other.ver_major:
            if self.ver_minor < other.ver_minor:
                return -1
            elif self.ver_minor == other.ver_minor:
                return 0
        return 1
        
    def matches(self, min_version, max_version):
        """
        Returns whether the version object represents a version
        greater than or equal to the minimum version and less than
        the maximum version.

        @param min_version: Minimum acceptable version.
        @param max_version: Maximum acceptable version.
        @returns: boolean

        If min_version is null then there is no minimum limit.
        If max_version is null then there is no maximum limit.
        """
        
        if max_version.is_null() and min_version.is_null():
            return True
        elif max_version.is_null():
            return min_version <= self
        elif min_version.is_null():
            return self >= max_version
        else:
            return min_version <= self <= max_version

