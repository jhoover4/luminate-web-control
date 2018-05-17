# Luminate Web Control

Created to test forms and download reports and queries from convio's Luminate Online 
due to Luminate's very limited API capabilities in regards to pulling a real amount of data from database.

This module uses an actual browser with selenium and beautifulsoup to pull reports 
and hence is relatively unstable and slow. If a better version of Luminate API become available 
consider this module irrelevant of soon to be updated.

For now, however, this was a  real help to me in automating Luminate reporting, 
especially when paired with my 
[send-reports module](https://github.com/jhoover4/send-reports).

Find an example use below.

## Reports

```
from luminate_web_control import reports


# initialize object
session = reports.ReportNavigation()

# download_trx_report takes the name of a form or campaign, a pull type, and a date.
# date_rng must match the types offered by Luminate.
# To grab all donations call the method with no parameters: session.download_trx_report()

session.download_trx_report(donation_categories=["The River and the Wall Giving"], pull_type="form")

# closes browser
session.quit_browsing()

```

## Queries

```
from luminate_web_control import queries


# initialize object
session = queries.QueryNavigation()

# simply use the exact query name. File goes to set download folder.
session.download_query_results("Planned Giving Opt-Ins")

# closes browser
session.quit_browsing()

```

## Donation Forms

This can be used for testing and making changes to LO donation forms automatically.
For example, to take a screenshot of every form and save the in an array:

```
from luminate_web_control import donation_forms


for key, value in forms.items():
        print("Taking shots of " + key, form)
        form = donation_forms.DonationFormNavigation(key, form)
        
        # takes screenshot of first page in donation form and thank you page
        form.perform_test()
        
        # saves email to downloads folder using email address in settings.py
        form.save_email_to_folder()
        
# closes browser
form.quit_browsing()
```