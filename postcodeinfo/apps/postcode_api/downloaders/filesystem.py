# -*- encoding: utf-8 -*-
"""
Local filesystem downloader cache mixin class
"""

import datetime
import logging
import os
from os.path import exists, getmtime
from time import mktime

import pytz


def last_modified(filename):
    """
    Get the last modified datetime of the specified file
    """

    mtime = getmtime(filename)
    if os.stat_float_times():
        return datetime.datetime.fromtimestamp(mtime)
    return pytz.UTC.localize(datetime.fromtimestamp(mktime(mtime)))


class LocalCache(object):
    """
    Download files unless they already exist locally and are newer than the
    files on the server.
    """

    def download_file(self, src, dest):
        """
        Download a single file, unless the file already exists locally and is
        newer than the remote file.
        """

        if exists(dest) and last_modified(dest) >= self.last_modified(src):
            return dest

        return super(LocalCacheMixin, self).download_file(src, dest)
