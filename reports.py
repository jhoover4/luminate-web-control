import datetime
import glob
import time

import bs4
from luminate_web_control.basic_web_control import BasicNavigation


class ReportNavigation(BasicNavigation):
    def __init__(self):
        super().__init__()

    def download_online_reports(self, report_id):
        """Online reporting refers to 'CCAH Transaction Report 2017' and 'CCAH Message Variant Report 2017'.
        Dates for online reporting is always the whole year.
        """

        self.browser.visit(
            "https://secure2.convio.net/pwft/admin/ReportWriterManager?rptwrt.manager=result_list&mfc_pref=T&report_schedule_id=")
        self.browser.find_by_text("Report Writer").click()

        report_run_link = "https://secure2.convio.net/pwft/admin/ReportWriterManager?rptwrt.manager=run_report&report_definition_id=" \
                          + report_id + "&mfc_pref=T&rid=0&action=run"
        self.browser.click_link_by_href(report_run_link)

        if report_id == "43806":  # trx id
            edit_button = self.browser.find_by_css("#report_filtersrow2 a")[0]
        elif report_id == "42322":  # email id
            edit_button = self.browser.find_by_css("#report_filtersrow2 a")[1]
        else:
            raise ValueError("report_id does not have a valid id.")

        edit_button.click()
        self.browser.select("report_filterdate_part_select_listname", "yr")
        self.browser.find_by_id("pstep_finish-button").click()

        # cycle through all the sidebar shit
        num_of_levels = len(self.browser.find_by_css(".tier-2")) - 1
        while num_of_levels > 0:
            time.sleep(3)
            self.next_button()
            num_of_levels -= 1

        self.browser.find_by_id("run_buttonbtn").first.click()

        # need to wait here until report is loaded
        self.browser.is_element_present_by_css("#dld_prtview_results a", wait_time=10)
        self.browser.find_by_css("#dld_prtview_results a").first.click()

        print("Waiting for download to be ready...")
        time.sleep(80)  # need to wait here until report is loaded

        pop_up_window = self.browser.windows[1]
        self.browser.windows.current = pop_up_window  # changes to popup window. Should probably use name for more specificity
        self.browser.find_by_css("#download_csvrow2 a").first.click()
        # Need to add error catching here in case we need to keep waiting!!
        pop_up_window.close()
        self.browser.windows.current = self.browser.windows[0]
        self.browser.find_by_id("HeaderLogo").click()

        print("Download finished! Find in downloads folder.")

    def download_trx_report(self, donation_categories = "", pull_type="all", date_rng="all"):
        self.browser.visit("https://secure2.convio.net/pwft/admin/Donation2Admin?don.admin=campaign_list_pa&mfc_pref=T")

        self.browser.find_by_id("don_report_list").first.click()
        self.browser.find_by_text("Donations By Transaction").first.click()
        self.browser.find_by_id("ProcessRunReport").first.click()

        valid_pull_types = ["form", "campaign", "all"]
        if pull_type.lower() not in valid_pull_types:
            raise ValueError("Improper pull type set. Must be one of ".format(", ".join(valid_pull_types)))

        # downloads all transactions if all
        if pull_type != "all":
            self.add_categories(donation_categories, pull_type)

        if date_rng != "all":
            self.set_date_pull(date_rng)

        self.browser.find_by_text("Configuration Summary").first.click()
        self.browser.find_by_id("submit_reportbtn").first.click()

        # reloads browser until download ready
        creation_time = self.download_page_reload()

        self.browser.find_by_text("Download").first.click()

        print(
            "Luminate transactions downloaded, creation time took {} seconds. Find in downloads folder.".format(creation_time)
        )

    def add_categories(self, donation_categories, form_grouping):
        form_grouping.strip()
        self.browser.find_by_text(form_grouping.capitalize() + " Filtering").first.click()
        self.browser.find_by_id(form_grouping.lower() + "_option_selected").first.click()

        for item in donation_categories:
            self.browser.find_by_text(item).first.click()
            self.browser.find_by_id(form_grouping.lower() + "s_Add_Selected").first.click()

        self.next_button()

    def set_date_pull(self, date_rng):

        self.browser.find_by_id("ProcessLink_don_report_configure_date_filter").first.click()
        self.browser.select("predefined_date_rangename", date_rng)
        self.next_button()

    @staticmethod
    def is_download_ready(page_html):
        """Using scraping for this because Luminates html setup is so difficult to manage."""

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        new_query_row_text = soup.select("tr.lc_Row1")[1].text.strip()

        return "download" not in new_query_row_text.lower()

    def download_page_reload(self):
        """Checks if the query is ready. If it isn't run the method until it is and inform the user."""

        self.browser.reload()
        query_page_html = self.browser.html
        total_creation_time = 0

        if not self.is_download_ready(query_page_html):
            print("Waiting for download to be ready...")
            time.sleep(30)  # need to wait here until report is loaded
            self.browser.reload()
            total_creation_time += 30
            total_creation_time += self.download_page_reload()

        return total_creation_time

    def check_download_file(self):
        today = datetime.datetime.today()
        month = today.strftime("%b")

        try:
            download_file = \
                glob.glob(self.download_folder + "Donations_By_Transaction_" +
                          month + "_" +
                          str(today.day) + "_" +
                          str(today.hour) + "_" +
                          str(today.minute) + "*.csv")[0]
            print("File saved as " + download_file)
            return True
        except IndexError:
            return False
