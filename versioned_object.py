import six

import api_version
from versioned_function import VersionedFunction

class VersionedObjectMetaClass(type):
    """Metaclass"""
    
    def __new__(mcs, name, bases, cls_dict):

        for key, value in cls_dict.items():
            # We need to remove the raw method name from the class
            # for versioned methods so __getattr_ will get invoked
            # and we can search for the correct one
            if getattr(value, 'multiversion', None):
                del cls_dict[key]
        
        return super(VersionedObjectMetaClass, mcs).__new__(
            mcs, name, bases, cls_dict)


@six.add_metaclass(VersionedObjectMetaClass)
class VersionedObject(object):
    """Base class for classes that support versioning of their methods."""

    def __getattr__(self, key):
        
        def version_select(*args, **kwargs):
            """
            Look for the method which matches the name supplied and version
            constraints and calls it with the supplied arguments.

            @return: Returns the result of the method called
            @raises: AttributeError if there is no method which matches the
                name and version constraints
            """

            # First arg to the method is the version. In the real API
            # code this is always the request object and we will put
            # the version object as an attribute of the request object
            ver = args[0]

            func_list = self.versioned_functions[key]
#            print "Possible: ", func_list
            for func in func_list:
                if ver.matches(func.start_version, func.end_version):
                    return func.func(self, *args, **kwargs)

            # No version match
            raise AttributeError

        if key in self.versioned_functions:
            return version_select

        # No method name match
        raise AttributeError
        
        
    @classmethod
    def api_version(cls, min_ver, max_ver=None):
        """
        Decorator for versioning methods.

        Add the decorator to any method which takes a version object
        as the first parameter. Note in the Nova API it would be any
        method which takes a request object as the first parameter and
        the version object would be attached to the request object.

        For example:
        @api_version("1.0.0")
        def my_method(ver, param1, param2):
            pass

        @api_version("2.0.0")
        def my_method(ver, param1, param2):
            pass

        An optional maximum version can also be supplied:
            
        @api_version("3.0.0", "3.2.0")
        def my_method(ver, param1, param2):
            pass
        """

        def decorator(f):
            f.multiversion = True
            obj_min_ver = api_version.APIVersion(min_ver)
            if max_ver:
                obj_max_ver = api_version.APIVersion(max_ver)
            else:
                obj_max_ver = api_version.APIVersion()

            # Add to list of versioned functions registered
            func_name = f.__name__
            new_func = VersionedFunction(
                func_name, obj_min_ver, obj_max_ver, f)

            print new_func

            func_dict = getattr(cls, 'versioned_functions', {})
            if not func_dict:
                setattr(cls, 'versioned_functions', func_dict)
                
            func_list = func_dict.get(func_name, [])
            if not func_list:
                func_dict[func_name] = func_list
            func_list.append(new_func)
            # Ensure the list is sorted by minimum version (reversed)
            # so later when we work through the list in order we find
            # the method which has the (latest version which supports
            # the version requested. Won't be an issue if we guarantee
            # no overlapping version definitions though
            func_list.sort(reverse=True)

            # TODO: Check there is no overlap in versions supported
            # which would make the request ambiguous

            return f
        
        return decorator
