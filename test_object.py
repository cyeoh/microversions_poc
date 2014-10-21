import versioned_object
from api_version import APIVersion

class TestObject(versioned_object.VersionedObject):

    @versioned_object.VersionedObject.api_version("1.2.3")
    def add(self, ver, first, second):
        "add"

        first = int(first)
        second = int(second)
        return first + second


    # Example of versioning on a method that will be called
    # externally
    @versioned_object.VersionedObject.api_version("2.0.0")
    def add(self, ver, first, second):
        first = int(first)
        second = int(second)
        # Do something weird so we can tell the difference
        # between the two add methods
        return first + second + 100

    @versioned_object.VersionedObject.api_version("1.0.0")
    def _real_sub(self, ver, first, second):
        return first - second

    
    # Example of versioning on a method that will be called
    # from within the class but still passed the version
    # information
    @versioned_object.VersionedObject.api_version("2.0.0")
    def real_sub(self, ver, first, second):
        return second - first

    def sub(self, ver, first, second):
        first = int(first)
        second = int(second)
        return self._real_sub(ver, first, second)

    def multiply(self, ver, first, second):
        first = int(first)
        second = int(second)

        # Example of inline version matching
        if ver.matches(APIVersion("1.1.0"),
                       APIVersion("2.1.0")):
            return first * second
        else:
            return first / second
