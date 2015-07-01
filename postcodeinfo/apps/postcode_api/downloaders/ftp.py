# -*- encoding: utf-8 -*-
"""
FTP downloader class
"""

import ftplib
import logging
import re

from postcode_api.downloaders import Downloader


class FTPDownloader(Downloader):
    """
    Downloads files from a FTP server
    """

    def __init__(self, host, username, password, path=None):
        self.host = host
        self.path = path
        self.username = username
        self.password = password
        self._ftp = None
        self._headers = {}

    def download(self, pattern, dest_dir):
        """
        Execute the download.
        Returns a list of downloaded files.
        """

        files = self._list(pattern)
        logging.debug('%i files matching %s' % (len(files), pattern))

        def dest(filename):
            return os.path.join(dest_dir, filename.split('/')[-1])

        return map(lambda src: self.download_file(src, dest(src)), files)

    def download_file(self, src, dest):
        """
        Download a single file.
        """

        content_length = self._headers[src]['content-length']

        def write_and_log_progress(f):

            counts = {
                'bytes': 0,
                'chunks': 0}

            def callback(data):
                f.write(data)

                counts['bytes'] += len(data)
                counts['chunks'] += 1

                if counts['chunks'] % 100 == 0:
                    logging.debug('{bytes} bytes of {total}'.format(
                        total=content_length,
                        bytes=counts['bytes']))

            return callback

        logging.debug('downloading {src} to {dest}'.format(
            src=src, dest=dest))

        with open(dest, 'wb') as f:
            self.ftp.retrbinary('RETR %s' % src, write_and_log_progress(f))

        logging.info('downloaded {dest}'.format(dest=dest))

    def last_modified(self, src):
        """
        Get the last modified datetime of the remote file
        """

        return parse_time(self._headers[src]['last-modified'])

    @property
    def ftp(self):
        if self._ftp is None:
            self._ftp = ftplib.FTP(self.host)
            self._ftp.login(self.username, self.password)
            if self.path is not None:
                self._ftp.cwd(self.path)
        return self._ftp

    def _list(self, pattern):
        files = {}

        def parse_ls_line(line):
            # NOTE: this is VERY brittle, but the OS FTP server doesn't support
            # the MSLD command (which is intended to produce machine-readable
            # output) so we don't have many other options.  Here we're trying
            # to emulate as closely as possible the headers that we would get
            # back from a HTTP HEAD request
            cols = re.split(' +', line)
            return {
                'permissions': cols[0],
                'content-length': int(cols[4]),
                'last-modified': ' '.join(cols[5:8]),
                'url': cols[-1],
                'etag': None
            }
            files[details['url']] = details

        self.ftp.dir(pattern, parse_ls_line)
        self._headers.update(files)
        return files.keys()
