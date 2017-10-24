# !/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
File: terminalcolor.py
Author: Rafal Marguzewicz
Email: info@pceuropa.net
Github: https://github.com/yourname
Description:  colorize for console
"""


class Colors(object):
    """Docstring for Colors. """

    HEAD = '\033[95m'
    BOLD = '\033[1m'

    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

    BLUE = '\033[94m'
    UNDEERLINE = '\033[4m'
    END = '\033[0m'

    def zero(self, arg, fo=None):
        """
        Return red or gren
        """
        arg = self.fo(arg, fo)
        if float(arg) < 0:
            return self.FAIL + arg + self.END
        else:
            return self.GREEN + arg + self.END

    def head(self, arg, fo=None):
        """ Return red or gren """
        arg = self.fo(arg, fo)
        return self.HEAD + arg + self.END

    def bold(self, arg, fo=None):
        """ Return red or gren """
        arg = self.fo(arg, fo)
        return self.BOLD + arg + self.END

    def green(self, arg, fo=None):
        """ Return red or gren """
        arg = self.fo(arg, fo)
        return self.GREEN + arg + self.END

    def warning(self, arg, fo=None):
        """ Return red or gren """
        arg = self.fo(arg, fo)
        return self.WARNING + arg + self.END

    def fail(self, arg, fo=None):
        """ Return red or gren """
        arg = self.fo(arg, fo)
        return self.FAIL + arg + self.END
    
    def fo(self, arg, fo):
        if fo is None:
            return str(arg)
        else:
            return format(arg, fo)
