# -*- encoding: utf-8 -*-
import mock
import os
import unittest

from postcode_api.downloaders import AddressBaseBasicDownloader


class AddressBaseBasicDownloaderTest(unittest.TestCase):

    def setUp(self):
        ftpuser = 'ftpuser'
        ftppass = 'ftppass'
        ftpdir = 'my/dir'
        self.env = {
            'OS_FTP_USERNAME': ftpuser,
            'OS_FTP_PASSWORD': ftppass,
            'OS_FTP_ORDER_DIR': ftpdir}

        self.env_patch = mock.patch.dict('os.environ', self.env)
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()

    def test_passes_ftp_credentials(self):

        with mock.patch('ftplib.FTP') as ftp_class:
            ftp = ftp_class.return_value
            AddressBaseBasicDownloader().download()
            ftp_class.assertCalledWith('osmmftp.os.uk')
            ftp.login.assertCalledWith(
                self.env['OS_FTP_USERNAME'], self.env['OS_FTP_PASSWORD'])
            ftp.cwd.assertCalledWith(self.env['OS_FTP_ORDER_DIR'])

    def test_downloads_files_matching_pattern(self):
        pattern = '*_csv.zip'

        with mock.patch('ftplib.FTP') as ftp_class:
            ftp = ftp_class.return_value
            AddressBaseBasicDownloader().download()
            self.assertTrue(ftp.dir.called)
            self.assertEqual(pattern, ftp.dir.call_args[0][0])
