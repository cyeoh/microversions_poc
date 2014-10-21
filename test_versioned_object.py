#!/usr/bin/python

from test_object import TestObject
from api_version import APIVersion

myobj = TestObject()
ver = APIVersion("1.2.3")
ver2 = APIVersion("2.2.3")
ver3 = APIVersion("1.0.0")

print "Finished init"

print myobj.add(ver, 1, 2) # Expect normal add result
print myobj.add(ver2, 1, 2) # Expect wierd add result

try:
    print myobj.add(ver3, 1, 2) # Expect no match to a method to be made
except AttributeError:
    print "Got attribute error as expected"

print myobj.sub(ver3, 4, 8) # Expect normal sub result
print myobj.sub(ver2, 4, 8) # Expect weird sub result

print myobj.multiply(ver, 8, 4)  # Expect normal multiply
print myobj.multiply(ver2, 8, 4) # Expect divide
print myobj.multiply(ver3, 8, 4) # Expect divide
