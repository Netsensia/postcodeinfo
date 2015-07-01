# -*- encoding: utf-8 -*-
"""
AddressBase Basic downloader class
"""

import os

from .filesystem import LocalCache
from .ftp import FTPDownloader
from .s3 import S3Cache


class AddressBaseBasicDownloader(LocalCache, S3Cache, FtpDownloader):
    """
    Ordnance Survey remove the files from the download directory after 21 days,
    so we cache the files on Amazon S3 in case we need them after that time.
    """

    def __init__(self):
        super(AddressBaseBasicDownloader, self).__init__(
            'osmmftp.os.uk',
            os.environ.get('OS_FTP_USERNAME'),
            os.environ.get('OS_FTP_PASSWORD'),
            path=os.environ.get(
                'OS_FTP_ORDER_DIR', '../from-os/DCS0001654526/'))

    def download(self, dest_dir=None):
        """
        Execute the download.
        Returns a list of downloaded files.
        """

        return super(AddressBaseBasicDownloader, self).download(
            '*_csv.zip', dest_dir)