import os
from unittest import TestCase

from queries import QueryNavigation


class TestQueryNavigation(TestCase):
    """NOTE: These are largely functional tests and are extremely slow.
    Unit testing will be improved at a later date.
    """

    def setUp(self):
        self.downloads = os.path.expanduser("~") + "\\Downloads"
        self.browse = QueryNavigation()

    def tearDown(self):
        self.browse.quit_browsing()

    def test_download_mail_merge(self):
        csv_count = len([name for name in os.listdir(self.downloads) if name.endswith(".csv")])

        self.browse.download_mail_merge()

        self.assertEquals(csv_count + 1, len([name for name in os.listdir(self.downloads) if name.endswith(".csv")]))

    def test_download_query_results(self):
        self.browse.download_query_results('All Austin Emails')
        file_name = 'All_Austin_Emails'

        downloads_files = [f for f in os.listdir(self.downloads) if file_name in f]

        self.assertIn(file_name, downloads_files[0])
