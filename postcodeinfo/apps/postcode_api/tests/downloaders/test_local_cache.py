import datetime
import mock
import time
import unittest

from postcode_api.downloaders.filesystem import LocalCache
from postcode_api.downloaders.http import HttpDownloader


class LocalCacheTest(unittest.TestCase):

    def test_uses_local_file_if_exists_and_up_to_date(self):

        timestamp = 'Sun, 23 Mar 2014 13:05:10 GMT'

        def ts(*args):
            dt = datetime.datetime(*args)
            return time.mktime(dt.timetuple())

        in_date = ts(2014, 3, 24, 12)
        out_of_date = ts(2014, 3, 22, 12)
        cases = [
            (True, in_date, False),
            (True, out_of_date, True),
            (False, in_date, True),
            (False, out_of_date, True)]

        class StubDownloader(LocalCache, HttpDownloader):
            pass

        pkg = lambda x: '%s.%s' % ('postcode_api.downloaders.filesystem', x)
        with mock.patch(pkg('exists')) as exists, \
                mock.patch(pkg('getmtime')) as getmtime, \
                mock.patch('requests.get') as get, \
                mock.patch('requests.head') as head:

            head.return_value.headers = {'last-modified': timestamp}

            for exists_, mtime, use_local in cases:
                getmtime.return_value = mtime
                exists.return_value = exists_

                downloader = StubDownloader('http://example.com/dummy_url')
                downloader.download('/tmp')

                self.assertEqual(use_local, get.called)

    @unittest.skip('foo')
    def test_that_when_the_file_is_in_local_storage_and_up_to_date_it_returns_true(self):
        self.assertEqual( True, subject().local_copy_up_to_date('local/path', 'remote timestamp') )

    @unittest.skip('foo')
    def test_that_when_the_file_is_in_local_storage_and_not_up_to_date_it_returns_false(self):
        self.assertEqual( False, subject().local_copy_up_to_date('local/path', 'remote timestamp') )

    @unittest.skip('foo')
    def test_that_when_the_file_is_not_in_local_storage_it_returns_false(self):
        self.assertEqual( False, subject().local_copy_up_to_date('local/path', 'remote timestamp') )

    @unittest.skip('foo')
    def test_that_when_copy_timestamp_is_greater_than_source_timestamp_it_returns_true(self):
        self.assertEqual( True, subject().up_to_date( datetime.now(), datetime.now() - timedelta(hours=1) ) )

    @unittest.skip('foo')
    def test_that_when_copy_timestamp_is_equal_to_source_timestamp_it_returns_true(self):
        now = datetime.now()
        self.assertEqual( True, subject().up_to_date( now, now ) )

    @unittest.skip('foo')
    def test_that_when_copy_timestamp_is_less_than_source_timestamp_it_returns_false(self):
        self.assertEqual( False, subject().up_to_date( datetime.now() - timedelta(hours=1), datetime.now() ) )
