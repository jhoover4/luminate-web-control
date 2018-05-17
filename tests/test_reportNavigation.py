import os
from unittest import TestCase

from reports import ReportNavigation


class TestReportNavigation(TestCase):
    """NOTE: These are largely functional tests and are extremely slow.
    Unit testing will be improved at a later date.
    """

    def setUp(self):
        self.downloads = os.path.expanduser("~") + "\\Downloads"
        self.browse = ReportNavigation()
        self.trx_report_count = len([name for name in os.listdir(self.downloads)
                                     if name.startswith("Donations_By_Transaction")])

    def tearDown(self):
        self.browse.quit_browsing()

    def test_download_online_reports(self):
        self.fail()

    def test_download_trx_report_all(self):
        """Tests that we download all transaction in current month from Luminate to downloads folder."""

        self.browse.download_trx_report(date_rng="mo-curr")

        self.assertEquals(self.trx_report_count + 1,
                          len([name for name in os.listdir(self.downloads)
                               if name.startswith("Donations_By_Transaction")]))

    def test_download_trx_report_campaign(self):
        """Tests that we download all stewards of the wild campaign transactions
         in current month from Luminate to downloads folder.
         """

        self.browse.download_trx_report(["Stewards of the Wild"], "campaign", "mo-curr")

        self.assertEquals(self.trx_report_count + 1,
                          len([name for name in os.listdir(self.downloads)
                               if name.startswith("Donations_By_Transaction")]))

    def test_download_trx_report_form(self):
        """Tests that we download all river and the wall form transactions from Luminate to downloads folder."""

        self.browse.download_trx_report(["The River and the Wall Giving"], "form")

        self.assertEquals(self.trx_report_count + 1,
                          len([name for name in os.listdir(self.downloads)
                               if name.startswith("Donations_By_Transaction")]))

    def test_add_categories(self):
        self.fail()

    def test_set_date_pull(self):
        self.fail()

    def test_is_download_ready(self):
        self.fail()

    def test_download_page_reload(self):
        self.fail()

    def test_check_download_file(self):
        self.fail()
