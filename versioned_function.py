

class VersionedFunction(object):

    def __init__(self, name, start_version, end_version, func):
        """
        Versioning information for a single function

        @name: Name of the method
        @start_version: Minimum acceptable version
        @end_version: Maximum acceptable_version
        @func: Method to call

        Minimum and maximums are inclusive
        """
        self.name = name
        self.start_version = start_version
        self.end_version = end_version
        self.func = func

    def __str__(self):
        return "%s: %s %s" % (self.name, self.start_version, self.end_version)
