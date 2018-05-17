import os
import time

import bs4
from luminate_web_control.basic_web_control import BasicNavigation


class QueryNavigation(BasicNavigation):
    def __init__(self):
        super().__init__()
        self.mail_merge_url = "https://secure2.convio.net/pwft/admin/Mailmerge"

    def download_query_results(self, query_name):
        """Runs a query from LO's Data Management > Query tab and returns results."""

        self.browser.visit("https://secure2.convio.net/pwft/admin/QueryAdmin")
        self.browser.fill('filter_text', query_name)
        self.browser.find_by_id("filter_search").first.click()
        self.browser.find_by_css("a[title='Run this query']").first.click()

        self.browser.find_by_css("#QueryResults a").first.click()
        pop_up_window = self.browser.windows[1]
        # changes to popup window. Should probably use name for more specificity
        self.browser.windows.current = pop_up_window
        self.browser.find_by_text("Create a Mail-Merge list").first.click()
        self.browser.find_by_id("ian_go").first.click()
        # popup window should close on its own.
        self.browser.windows.current = self.browser.windows[0]

        self.browser.fill('Message_Name', query_name)
        self.browser.fill('Message_Description', query_name)

        self.browser.find_by_id("Mailmerge_Field_Selector_Add_All").first.click()
        self.browser.find_by_css("input[title='Next Step']").first.click()
        self.browser.find_by_id("create_mr_ph").first.click()

        # Luminate is extremely buggy. To actually get the query to download,
        # you must go backwards in the browser and the confirm to create the query again.
        # We do that here.
        self.browser.back()
        time.sleep(5)
        self.browser.find_by_id("create_mr_ph").first.click()
        self.browser.find_by_text("Mail Merges List").first.click()

        self.download_mail_merge()

    def download_mail_merge(self):
        """Downloads mail merges from LO Data Management > Mail Merges tab.
        Will only download the most recent merge.
        """

        self.browser.visit(self.mail_merge_url)

        creation_time = self.query_page_reload()

        self.browser.find_by_text("Mail Merges List").first.click()
        img_list = self.browser.find_by_tag("img")
        img_list[11].click()  # first 'save' image on page

        print(
            "Luminate query downloaded, creation time took {} seconds. Find in downloads folder.".format(creation_time))

    @staticmethod
    def is_query_ready(page_html):
        """Using scraping for this because Luminates html setup is so difficult to manage."""

        soup = bs4.BeautifulSoup(page_html, 'html.parser')
        new_donation_row = soup.find_all("tr", "lc_Row1")[1]

        return bool(new_donation_row.find_all(string="Download"))

    def query_page_reload(self):
        """Checks if the query is ready. If it isn't run the method until it is and inform the user."""

        self.browser.reload()
        query_page_html = self.browser.html
        total_creation_time = 0

        if not self.is_query_ready(query_page_html):
            os.system('cls')
            print("Luminate has not finished creating the mailmerge, will refresh in 30 seconds...")
            time.sleep(30)
            total_creation_time += 30
            total_creation_time += self.query_page_reload()

        return total_creation_time
