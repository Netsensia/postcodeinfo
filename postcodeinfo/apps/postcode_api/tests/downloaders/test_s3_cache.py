
    @unittest.skip('foo')
    def test_that_when_the_local_copy_is_not_up_to_date_then_it_gets_from_s3(self):
        s = subject()
        s._local_copy_up_to_date = mock.Mock(False)
        s.retrieve('test.url', '/local/path')
        mock_get_from_s3.assertCalledWith('/local/path', '12345')

    @unittest.skip('foo')
    def test_that_when_the_local_copy_is_up_to_date_then_it_does_not_get_from_s3(self):
        s = subject()
        s.local_copy_up_to_date = mock.Mock(True)
        s.retrieve('test.url', '/local/path')
        assert not mock_get_from_s3.called

    @unittest.skip('foo')
    def test_that_when_the_s3_object_is_up_to_date_it_downloads_the_file_from_s3(self):
        s = subject()
        s.get_from_s3('test.url', '/local/path', '12345')
        self.assertEqual(True, mock_s3_adapter().download.called )

    @unittest.skip('foo')
    def test_that_when_the_s3_object_is_not_up_to_date_it_downloads_the_file_locally(self):
        s = subject()
        s.get_from_s3('test.url', '/local/path', '12345')
        mock_download_to_file.assertCalledWith('test.url', '/local/path')

    @unittest.skip('foo')
    def test_that_when_the_s3_object_is_not_up_to_date_it_uploads_the_local_file_to_s3(self):
        s = subject()
        s.get_from_s3('test.url', '/local/path', '12345')
        mock_s3_adapter.upload.assertCalledWith('test.url', '/local/path')

    @unittest.skip('foo')
    def test_that_when_the_s3_object_exists_and_is_up_to_date_it_returns_true(self):
        s3_object = mock.Mock(last_modified='12345')
        self.assertEqual( True, subject().s3_object_is_up_to_date(s3_object, 'remote timestamp') )

    @unittest.skip('foo')
    def test_that_when_the_s3_object_exists_and_is_not_up_to_date_it_returns_false(self):
        s3_object = mock.Mock(last_modified='12345')
        self.assertEqual( False, subject().s3_object_is_up_to_date(s3_object, 'remote timestamp') )

    @unittest.skip('foo')
    def test_that_when_the_s3_object_does_not_exist_it_returns_true(self):
        self.assertEqual( False, subject().s3_object_is_up_to_date(None, 'remote timestamp') )

