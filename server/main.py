# server/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime
import yagmail
from jinja2 import Template
from apscheduler.schedulers.background import BackgroundScheduler
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"
EXCEL_PATH = os.path.join(UPLOAD_FOLDER, "employees.xlsx")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load HTML template
with open("birthday_template.html", "r", encoding="utf-8") as f:
    email_template = Template(f.read())

# Configure Email
yag = yagmail.SMTP(user="vaibhavchauhan658@gmail.com", password="iqxq jpyz qmhx npzz")

# Birthday mail logic
def send_birthday_emails():
    if not os.path.exists(EXCEL_PATH):
        print("❌ Excel file not found.")
        return

    df = pd.read_excel(EXCEL_PATH)
    today = datetime.now().strftime("%m-%d")

    for _, row in df.iterrows():
        try:
            dob = pd.to_datetime(row['DOB'], errors='coerce').strftime("%m-%d")
            if dob == today:
                name = row['Name']
                email = row['Email']
                html = email_template.render(name=name)
                yag.send(to=email, subject=f"Happy Birthday {name}! 🎉", contents=html)
                print(f"✅ Sent to {name} at {email}")
        except Exception as e:
            print(f"⚠️ Error sending mail to {row['Name']} - {e}")

# Scheduler run daily at 9 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_birthday_emails, "cron", hour=9, minute=0)
scheduler.start()

# File upload endpoint
@app.post("/upload")
def upload_excel(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, "employees.xlsx")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return JSONResponse(content={"message": "✅ File uploaded successfully!"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"❌ Error: {str(e)}"})

@app.get("/")
def home():
    return {"message": "🎂 Birthday Mailer Running"}
    