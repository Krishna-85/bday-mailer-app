import pandas as pd
from datetime import datetime
import yagmail
from jinja2 import Template
import os

EXCEL_PATH = "server/uploads/employees.xlsx"
TEMPLATE_PATH = "server/templates/birthday_template.html"

def send_birthday_mails():
    today = datetime.now().strftime("%m-%d")

    try:
        df = pd.read_excel(EXCEL_PATH)
    except Exception as e:
        print("Excel read failed:", e)
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = Template(f.read())

    yag = yagmail.SMTP(user=os.environ["EMAIL_USER"], password=os.environ["EMAIL_PASS"])

    for _, row in df.iterrows():
        dob = pd.to_datetime(row['DOB']).strftime("%m-%d")
        if dob == today:
            html_content = template.render(name=row['Name'])
            yag.send(
                to=row['Email'],
                subject=f"Happy Birthday {row['Name']}! 🎂",
                contents=html_content
            )
            print(f"Sent to {row['Name']} - {row['Email']}")

if __name__ == "__main__":
    send_birthday_mails()
