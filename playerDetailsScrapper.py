import os
from json import loads
from dotenv import load_dotenv
import requests
import csv

load_dotenv()

team_url = os.getenv("TEAM_URL")
series_id = os.getenv("SERIES_ID")

requestURL = team_url+"?seriesId="+series_id+"&squadId={0}"

teamIds = loads(os.getenv("TEAM_IDS"))

for id in teamIds:
    teamInfo = requests.get(url=requestURL.format(id)).json()
    print("Writing team details")
    with open('Data/teams.csv', 'a', newline='\n') as teamFile:
        writer = csv.writer(teamFile)
        writer.writerow([teamInfo["content"]["squadDetails"]["squad"]["teamId"], teamInfo["content"]["squadDetails"]["squad"]["teamName"]])

    print("Writing Player details")
    with open('Data/players.csv', 'a', newline='\n') as playerFile:
        writer = csv.writer(playerFile)
        for player in teamInfo["content"]["squadDetails"]["players"]:
            writer.writerow([player["player"]["id"], player["player"]["longName"], teamInfo["content"]["squadDetails"]["squad"]["teamId"]])
