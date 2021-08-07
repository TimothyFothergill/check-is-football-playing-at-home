import datetime
import http.client
import json
import os
from flask import Flask, render_template

from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def index():
    load_dotenv()

    # set .env variables to match. api key obtained from: 
    # https://dashboard.api-football.com

    key = os.getenv('MY_API_KEY')
    season = os.getenv('SEASON')
    team = os.getenv('TEAM')
    get_next = os.getenv('GET_NEXT')
    venue = os.getenv('VENUE_ID')

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': key
        }
    q = "season=" + str(season) + "&team=" + str(team) + "&next=" + str(get_next)
    conn.request("GET", "/fixtures?" + str(q), headers=headers)

    res = conn.getresponse()
    data = res.read()
    j = json.loads(data)

    for i in j["response"]:

        match_date = datetime.datetime.strptime(
            str(i["fixture"]["date"]), 
            "%Y-%m-%d" + "T" + "%H:%M:%S" + "+00:00"
            ).date()
        current_date = datetime.date.today()
        match_date = match_date.strftime("%d %b %Y")
        current_date = current_date.strftime("%d %b %Y")

        todays_date = "Today's Date is: " + str(current_date)
        next_match = "The next match is on: " + str(match_date)

        if(i["fixture"]["venue"]["id"] == venue):
            if(match_date == current_date):
                return render_template("index.html", RESULT= """UH-OH! The 
                football is going to be playing at home. Do not move the 
                car!""",
                TODAY_DATE= todays_date, NEXT_MATCH= next_match)
            else:
                return render_template("index.html", RESULT="""WARNING: The  
                next Rovers match will be at home on:""" + str(match_date) 
                + """. Until then, you can move the car.""",
                TODAY_DATE= todays_date, NEXT_MATCH= next_match)
        else:
            return render_template("index.html", RESULT="""The football is 
            playing away for their next game. You are free to move the car.""",
                TODAY_DATE= todays_date, NEXT_MATCH= next_match)

if __name__ == "__main__":
    app.run(debug=True)
