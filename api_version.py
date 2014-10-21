class APIVersion(object):
    """
    This class represents an API Version with convenience
    methods for manipulation and comparison of version
    numbers that we need to do to implement microversions.
    """

    def __init__(self, version_string=None):
        """
        Create an API version object.

        @param version_string: Semver string representation of a version.
            See http://semver.org. The default is to create a null
            APIVersion object.
        """
        self.ver_major = None
        self.ver_minor = None
        self.ver_patch = None

        # TODO: fix the following to some decent format checking
        if version_string:
            (self.ver_major, self.ver_minor, self.ver_patch) =\
               version_string.split('.')

    def __str__(self):
        """String representation just for debugging purposes"""
        return_str = "Major: %s, Minor: %s, Patch: %s" % (
            self.ver_major, self.ver_minor, self.ver_patch)
        return return_str

    def is_null(self):
        return self.ver_major is None and self.ver_minor is None \
          and self.ver_patch is None

    def __cmp__(self, other):
        if self.ver_major < other.ver_major:
            return -1
        elif self.ver_major == other.ver_major:
            if self.ver_minor < other.ver_minor:
                return -1
            elif self.ver_minor == other.ver_minor:
                if self.ver_patch < other.ver_patch:
                    return -1
                elif self.ver_patch == other.ver_patch:
                    return 0
                else:
                    return 1
            return 1
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
        
#        print  "COMPARING: %s %s %s" % (self, min_version, max_version)
        if max_version.is_null() and min_version.is_null():
            return True
        elif max_version.is_null():
            return min_version <= self
        elif min_version.is_null():
            return self >= max_version
        else:
            return min_version <= self <= max_version

