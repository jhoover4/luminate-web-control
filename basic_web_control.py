import glob
import os
import win32gui

import splinter
import win32con

from .local_settings import *


class BasicNavigation:
    """
    TODO: Errorhandling.
    TODO: Improve browser knowing when download is ready.
    """

    luminate_online = "https://secure2.convio.net/pwft/admin/AdminHomePage"
    un = LUMINATE_USERNAME
    pw = LUMINATE_PASSWORD

    user_dir = os.path.expanduser("~")
    download_folder = os.path.join(user_dir, DOWNLOAD_FOLDER)
    firefox_profile = os.path.join(user_dir, FIREFOX_PROFILE)

    def __init__(self, browser_type="firefox", **kwargs):
        self.browser_type = browser_type

        # firefox works best with splinter/selenium.
        # Params below give ability to download file on click without prompts
        if self.browser_type == "firefox":
            self.browser = splinter.Browser(
                browser_type,
                headless=HEADLESS,
                profile=self.firefox_profile,
                capabilities={
                    'showWhenStarting': False,
                    'saveToDisk': "application/octet-stream",
                }
            )
        else:
            self.browser = splinter.Browser(browser_type, **kwargs)

        self.luminate_log_in()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def luminate_log_in(self):
        self.browser.visit(self.luminate_online)
        login_form = self.browser.find_by_css("#lmainLogonForm")
        un_field = login_form.find_by_tag("input")[0]
        pw_field = login_form.find_by_tag("input")[1]

        self.browser.fill(un_field["name"], self.un)
        self.browser.fill(pw_field["name"], self.pw)
        self.browser.find_by_name("login").first.click()

    @staticmethod
    def max_window():
        toplist, winlist = [], []

        def enum_cb(hwnd):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, toplist)
        chrome = [(hwnd, title) for hwnd, title in winlist if 'chrome' in title.lower()]

        hwnd = chrome[0][0]
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    def quit_browsing(self):
        self.browser.quit()

    def go_to_lo_home(self):
        self.browser.visit("https://secure2.convio.net/pwft/admin/AdminHomePage")

    def next_button(self):
        """Easy use of next button."""
        self.browser.find_by_id("pstep_next-button").first.click()

    def check_if_downloaded(self, partial_file_name):
        """Checks to see if we already have the file before trying to download from Luminate."""

        file = glob.glob(self.download_folder + partial_file_name)

        return bool(file)
