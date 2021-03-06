import csv

from time import gmtime

from postcode_api.models import PostcodeGssCode, Download
from postcode_api.importers.progress_reporter import ImporterProgress, \
    lines_in_file


class PostcodeGssCodeImporter(object):

    def import_postcode_gss_codes(self, filename):

        with open(filename, "rb") as csvfile:
            with ImporterProgress(lines_in_file(filename)) as progress:
                datareader = csv.reader(csvfile)
                # skip the header row!
                datareader.next()
                for row in datareader:
                    self.import_row(row)
                    progress.increment(row[0])

            self.update_download(filename)

    def import_row(self, row):
        postcode = row[0]
        local_authority_gss_code = row[11]
        normalized_postcode = postcode.replace(' ', '').lower()
        mapping = self.find_or_create_lookup(normalized_postcode)
        mapping.local_authority_gss_code = local_authority_gss_code
        mapping.save()

    def find_or_create_lookup(self, postcode_index):
        try:
            a = PostcodeGssCode.objects.get(postcode_index=postcode_index)
        except PostcodeGssCode.DoesNotExist:
            a = PostcodeGssCode(postcode_index=postcode_index)
        return a

    def update_download(self, filename):
        dl = Download.objects.filter(
            local_filepath=filename, state='downloaded').first()
        if dl:
            dl.state = 'imported'
            dl.last_state_change = gmtime()
            dl.save()
