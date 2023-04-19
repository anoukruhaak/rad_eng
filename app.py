from flask import Flask, jsonify, request, abort
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

app = Flask(__name__)
app.secret_key = "FLASK_KEY"
Bootstrap(app)

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",                                                        "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credentials)
gsheet = client.open("Developers and Projects Overview").sheet1

@app.route("/")
def home():
    return render_template("home.html", active="home")

@app.route("/volunteer")
def volunteer():
    vacancies = gsheet.get_all_records()
    open = [v for v in vacancies if v["Status"] == "Open"]
    return render_template("volunteer.html", open=open, active="volunteer")

@app.route("/projects")
def projects():
    vacancies = gsheet.get_all_records()
    closed = [v["Organisation"] for v in vacancies if v["Status"] != "Open"]
    unique = []
    [unique.append(x) for x in closed if x not in unique]
    orgs = sorted(unique)
    print(orgs)
    return render_template("projects.html", orgs=orgs)

@app.route("/news")
def news():
    return render_template("news.html")


