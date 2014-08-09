# -*- coding: utf-8 -*-

import uno
from com.sun.star.connection import NoConnectException
from com.sun.star.lang import IllegalArgumentException
from com.sun.star.task import ErrorCodeIOException
from com.sun.star.beans import PropertyValue
import string


class ODTFileError(Exception):
    pass


class ODTFile():
    def __init__(self, filename):
        self.errors = []
        self.local = uno.getComponentContext()
        self.document = None
        self.resolver = self.local.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver",
            self.local
        )
        try:
            self.context = self.resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            self.desktop = self.context.ServiceManager.createInstanceWithContext(
                "com.sun.star.frame.Desktop",
                self.context
            )
            try:
                self.document = self.desktop.loadComponentFromURL(uno.systemPathToFileUrl(filename), "_blank", 0, ())
            except IllegalArgumentException, e:
                self.errors.append('Error in file %s: %s' % (filename, e.message))
                raise ODTFileError
        except NoConnectException:
            self.errors.append('Connect to server error!')
            raise ODTFileError

    def save(self, path, file_format='MS Word 97'):
        properties = (
            PropertyValue("FilterName", 0, file_format, 0),
            PropertyValue("Overwrite", 0, True, 0))

        if self.document:
            try:
                self.document.storeToURL(uno.systemPathToFileUrl(path), properties)
            except ErrorCodeIOException:
                self.errors.append("Save file error (may be already open): %s" % path)
                raise ODTFileError

    def __del__(self):
        if self.document:
            self.document.dispose()

    def replace(self, find, replace):
        if self.document:
            search = self.document.createSearchDescriptor()
            search.SearchString = find
            found = self.document.findFirst(search)
            while found:
                found.String = string.replace(found.String, find, replace)
                found = self.document.findNext(found.End, search)

    def fill_template(self, data):
        for find, replace in data.items():
            if len(replace) > 65500:
                start = replace[0:65500] + "$pekfjgyt"
                end = replace[65500:]
                self.replace("$%s" % find, start)
                self.replace("$pekfjgyt", end)
            else:
                self.replace("$%s" % find, replace)