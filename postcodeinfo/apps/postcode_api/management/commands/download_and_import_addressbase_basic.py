import os
from django.core.management.base import BaseCommand

from index_suppressor import IndexSuppressor

from postcode_api.downloaders.addressbase_basic_downloader \
    import AddressBaseBasicDownloader
from postcode_api.importers.addressbase_basic_importer \
    import AddressBaseBasicImporter
from postcode_api.utils import ZipExtractor


def exit_code(key):
    return {'OK': 0, 'GENERIC_ERROR': 1}[key]


class Command(BaseCommand):
    args = '<destination_dir (default /tmp/)>'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--destination_dir',
                            action='store_true',
                            dest='destination_dir',
                            default='/tmp/addressbase_basic/')

        # Named (optional) arguments
        parser.add_argument('--force',
                            action='store_true',
                            dest='force',
                            default=False,
                            help='Force download '
                            'even if previous download exists')

    def handle(self, *args, **options):

        if not os.path.exists(options['destination_dir']):
            os.makedirs(options['destination_dir'])

        downloaded_file = self._download(
            options['destination_dir'], options.get('force', False))
        if downloaded_file:
            self._process_all(downloaded_file)
            return exit_code('OK')
        else:
            print 'nothing downloaded - nothing to import'
            return exit_code('OK')

    def _download(self, destination_dir, force=False):
        print 'downloading'
        downloader = AddressBaseBasicDownloader()
        return downloader.download(destination_dir, force)

    def _process_all(self, files):
        with IndexSuppressor('postcode_api_address'):
            if isinstance(files, list):
                for filepath in files:
                    self._process(filepath)
            else:
                self._process(files)

    def _process(self, filepath):
        files = ZipExtractor(filepath).unzip_if_needed(
            '.*AddressBase_.*\.csv')

        for path in files:
            print 'importing ' + path
            self._import(path)

        return True

    def _import(self, downloaded_file):
        importer = AddressBaseBasicImporter()
        importer.import_csv(downloaded_file)
