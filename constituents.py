from .basic_web_control import BasicNavigation


class ConstituentNavigation(BasicNavigation):
    def __init__(self):
        super(BasicNavigation, self).__init__()

    def find_constituent(self, constituent):
        self.browser.visit("https://secure2.convio.net/pwft/admin/ConsFind")

        self.browser.fill("FINDUSER_FirstName", constituent["first_name"])
        self.browser.fill("FINDUSER_LastName", constituent["last_name"])
        self.browser.fill("FINDUSER_Email", constituent["email"])
        self.browser.find_by_name("FINDUSER_Find").first.click()

        self.browser.find_by_text("View").first.click()

    def update_member_profile(self, constituent):
        self.find_constituent(constituent)

        # needs to be reworked
        if self.browser.is_text_present("Edit Consituent Info") is True:
            self.browser.find_by_text("Edit Consituent Info").first.click()

        self.browser.select("membership_status", "2")  # current member
        self.browser.fill("membership_id", constituent["membership"]["id"])

        membership_type_select = self.browser.find_by_id("membership_level_id")
        # will need to make sure values are filtered to match luminate text properly
        type_value = membership_type_select.find_by_text(constituent["membership"]["type"]).value
        self.browser.select("membership_level_id", type_value)

        # do date selection here

        self.browser.find_by_id("op.saveCons-top").first.click()  # saves changes
