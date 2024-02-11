import pandas as pd
from datetime import date
from smtplib import SMTP_SSL
from email.message import EmailMessage
import json
from pretty_html_table import build_table


# Get the current date
def get_day():
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    return today


# Email the alert
def email(recalls):
    if recalls.shape[0] > 0:
        file = open('config.json')
        data = json.load(file)

        ADDRESS = data['ADDRESS']
        PASSWORD = data['PASSWORD']
        mail_body = """
        New FDA Recalls
        {0}   
        """.format(build_table(recalls,'red_light'))

        msg = EmailMessage()
        msg['From'] = ADDRESS
        msg['To'] = ADDRESS
        msg['Subject'] = "Recall Alert"
        msg.add_alternative(mail_body, subtype='html')
        with SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(ADDRESS, PASSWORD)
            smtp.send_message(msg)
            smtp.close()


# Scrape page
def find_recalls():
    url = 'https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts'

    tables = pd.read_html(url)
    df = tables[0]
    df = df.drop('Excerpt', axis=1)
    today = get_day()

    recalls = df.loc[df['Date'] == today]
    return recalls


def recall_alert():
    recalls = find_recalls()
    email(recalls)


if __name__ == "__main__":
    recall_alert()
