import os
import glob
import win32com.client

from luminate_web_control.basic_web_control import BasicNavigation


class DonationFormNavigation(BasicNavigation):
    def __init__(self, campaign, donation_form):
        super().__init__()

        self.campaign = campaign
        self.donation_form = donation_form

        # self.screenshot_folder = self.make_screenshot_folder()

    def get_to_donation_form(self):
        self.browser.visit("https://secure2.convio.net/pwft/admin/Donation2Admin?don.admin=campaign_list_pa&mfc_pref=T")

        self.browser.fill('filter_text', self.campaign)
        self.browser.find_by_id("filter_search").first.click()
        self.browser.find_by_css("a.ListActionLinks[title='Manage']").first.click()

        self.browser.fill('filter_text', self.donation_form)
        self.browser.find_by_css("a.ListActionLinks[title='Edit']").first.click()

    def press_save(self):
        self.browser.find_by_css("#pstep_save-button").first.click()

    def get_to_test(self):
        self.get_to_donation_form()
        self.browser.find_by_text('Test Drive').click()
        self.browser.find_by_css('input#test_buttonbtn').click()
        pop_up_window = self.browser.windows[1]
        self.browser.windows.current = pop_up_window

    def fill_form(self):
        self.browser.find_by_css('.donation-level-amount-container').first.click()

        self.browser.fill('billing_first_namename', 'Bob')
        self.browser.fill('billing_last_namename', 'Rogers')
        self.browser.fill('billing_addr_street1name', '1 Test Street')
        self.browser.fill('billing_addr_cityname', 'Dallas')
        self.browser.select('billing_addr_state', 'TX')
        self.browser.fill('billing_addr_zipname', 75204)
        self.browser.fill('donor_email_addressname', self.un)
        self.browser.fill('responsive_payment_typecc_numbername', '4111-1111-1111-1111')
        self.browser.fill('responsive_payment_typecc_cvvname', 1111)

    def save_email_to_folder(self):
        """Saves email from outlook to created folder."""

        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # "6" refers to the index of a folder - in this case,
        # the inbox. You can change that number to reference
        # any other folder
        messages = inbox.Items
        message = messages.GetLast()

        save_path = os.path.join(self.screenshot_folder, "autoresponder.msg")
        message.SaveAs(save_path)
        print("Autoresponder saved to " + save_path)

    def perform_test(self):
        """Performs test from Luminate Online donation form test button."""

        self.get_to_test()
        self.make_screenshot_folder()

        # landing page
        self.take_screenshot()
        self.rename_file('donation_page')

        self.fill_form()
        self.browser.find_by_id('pstep_next').first.click()
        if "gear up".lower() in self.campaign.lower():
            # gear up campaigns have another step currently
            self.browser.find_by_id('pstep_finish').first.click()

        # thank you page
        self.take_screenshot()
        self.rename_file('thank_you_page')

        # email
        self.save_email_to_folder()

    def make_screenshot_folder(self):
        if not hasattr(self, 'screenshot_folder'):
            screenshot_folder = self.download_folder + self.campaign + "\\" + \
                                self.donation_form + "_form_screenshots"
            if not os.path.exists(screenshot_folder):
                os.makedirs(screenshot_folder)

            self.screenshot_folder = screenshot_folder

    def take_screenshot(self):
        self.make_screenshot_folder()

        self.browser.wait_time = 10
        self.max_window()

        self.browser.screenshot(name=self.screenshot_folder + "\\")

    def rename_file(self, page_type):
        """New file name matches current browser title."""
        files = glob.glob(self.screenshot_folder + "/*")
        newest_file = max(files, key=os.path.getctime)
        try:
            file_rename = self.screenshot_folder + "\\" + page_type + ".png"
            os.rename(newest_file, file_rename)
            print("Screenshot saved to " + file_rename)
        except FileExistsError:
            print("File already exists. Deleting download.")
            os.remove(newest_file)

    def close_new_window(self):
        self.browser.windows.current.close()
        self.browser.windows.current = self.browser.windows[0]

    def get_donation_page_href(self):
        self.get_to_donation_form()
        self.browser.find_by_text('Publish').click()
        return self.browser.find_by_css(".BeanOutputText").last.text

    def donation_page(self):
        self.get_to_donation_form()
        self.browser.find_by_text('Publish').click()
        donation_page_href = self.browser.find_by_css(".BeanOutputText").last.text

        self.browser.execute_script("window.open('');")
        self.browser.windows.current = self.browser.windows[1]
        self.browser.visit(donation_page_href)

        self.take_screenshot()
        self.rename_file('donation_page')

        self.close_new_window()

    def thank_you_page(self):
        self.get_to_donation_form()
        self.browser.find_by_text("Design Donor Screens").click()
        # #this opens a new page
        self.browser.find_by_css(".lc_Row1")[2].find_by_css(".ListActionLinks")[0].click()
        self.browser.windows.current = self.browser.windows[1]

        self.take_screenshot()
        self.rename_file('thank_you_page')

        self.close_new_window()

    def auto_responder(self):
        self.get_to_donation_form()
        self.browser.find_by_text('Configure Autoresponders').click()

        self.browser.find_by_css(
            'a.ListActionLinks[title="Open this Autoresponder in a Preview Window. Opens new window."]').first.click()

        self.browser.windows.current = self.browser.windows[1]

        self.take_screenshot()
        self.rename_file('auto_responder')

        self.close_new_window()

    @staticmethod
    def auto_responder_text(message):
        body_content = message.body
        print(body_content)

    def donation_page_nav(self, selection):
        self.get_to_donation_form()
        self.browser.find_by_text(selection.title()).click()

    def donation_page_edits(self, config_element):

        def save_and_edit():
            save_and_edit_btn = self.browser.find_by_xpath(
                "//*[@id='contentScrollLayer']/div[3]/table/tbody/tr/td/table[1]/tbody/tr[3]/td[3]/input")
            save_and_edit_btn.first.click()

        self.donation_page_nav("design donor screens")
        # donation form edit button
        self.browser.find_by_xpath(
            "/html/body/div[6]/form/table/tbody/tr/td[2]/div[3]/div[2]/table/tbody/tr[3]/td[2]/div/a[2]") \
            .click()

        # holds reference above where LO keeps all <tr>s for selection
        config_elements = self.browser.find_by_css("#selectorSelectedLayer")
        config_elements.find_by_text(" - " + config_element.title())[1].click()

        save_and_edit()
