import datetime
import http.client
import json
import os

from dotenv import load_dotenv

load_dotenv()

# set .env variables to match. api key obtained from: 
# https://dashboard.api-football.com

key = os.getenv('MY_API_KEY')
season = os.getenv('SEASON')
team = os.getenv('TEAM')
get_next = os.getenv('GET_NEXT')

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

    print("Today's Date is: " + str(current_date))
    print("The next match is on: " + str(match_date))

    if(i["fixture"]["venue"]["id"] == 510):
        if(match_date == currentDate):
            print("UH-OH! The football is going to be playing at home. Do " + 
            "not move the car!")
        else:
            print("WARNING: The next Rovers match will be at home on: " + 
                str(match_date) + 
                ". Until then, you can move the car")
    else:
        print("The football is playing away for their next game." + 
        " You are free to move the car.")
