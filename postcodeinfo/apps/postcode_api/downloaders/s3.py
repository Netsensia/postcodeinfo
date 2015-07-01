# -*- encoding: utf-8 -*-
"""
Downloader mixin class that caches downloads on Amazon S3
"""

import logging

import boto
from boto.s3.key import Key
from dateutil import parser as dateparser
from django.conf import settings


class S3Cache(object):
    """
    Download files unless they already exist in S3 and are newer than the files
    on the server.
    """

    def __init__(self, region=None, bucket=None):
        self._bucket = None
        self.region_name = region
        if region is None:
            self.region_name = settings.AWS['region_name']
        self.bucket_name = bucket
        if bucket is None:
            self.bucket_name = settings.AWS['s3_bucket_name']

    @property
    def bucket(self):
        if self._bucket is None:
            conn = boto.s3.connect_to_region(self.region_name)
            self._bucket = conn.get_bucket(self.bucket_name)
        return self._bucket

    def download_file(self, src, dest):
        """
        Download a single file, unless the file already exists in S3 and is
        newer than the remote file - in which case, download from S3.
        """

        key = self.bucket.lookup(src)
        last_modified = lambda k: dateparser.parse(k.last_modified)

        if key and last_modified(key) >= self.last_modified(src):

            logging.debug('downloading from s3 to {dest}'.format(dest=dest))

            return key.get_contents_to_filename(dest)

        result = super(S3CacheMixin, self).download_file(src, dest)

        logging.debug('uploading {dest} to s3 key {src}'.format(
            src=src, dest=dest))

        key = Key(self.bucket, src)
        key.set_contents_from_filename(dest)

        return result
