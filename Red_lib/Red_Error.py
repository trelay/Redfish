#!/usr/bin/python3
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class HttpTimeError(Error):
    def __init__(self, time):
        self.time = time 
    def __str__(self):
        msg="Over limit when accessing URL {0:6f}".format(self.time)
        return msg

class DataError(Error):
    def __init__(self, reason):
        self.reason = reason
    def __str__(self):
        msg="Data is not in right format, it"
        return msg

'''
try:
    raise TypeError("not right")
except HttpTimeError as e:
	print(e.__str__())
'''
