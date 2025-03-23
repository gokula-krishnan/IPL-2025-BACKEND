import json
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

all_team_data = []
folder_path = "Data/SQUAD_DATA"

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Check if the file is a JSON file
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
                all_team_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")

for i, id in enumerate(teamIds):
    print("Writing team details")
    teamInfo = all_team_data[i]
    with open('Data/teams.csv', 'a', newline='\n') as teamFile:
        writer = csv.writer(teamFile)
        writer.writerow([teamInfo["content"]["squadDetails"]["squad"]["teamId"], teamInfo["content"]["squadDetails"]["squad"]["teamName"]])

    print("Writing Player details")
    with open('Data/players.csv', 'a', newline='\n') as playerFile:
        writer = csv.writer(playerFile)
        for player in teamInfo["content"]["squadDetails"]["players"]:
            writer.writerow([player["player"]["id"], player["player"]["longName"], teamInfo["content"]["squadDetails"]["squad"]["teamId"]])


# for id in teamIds:
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
#     teamInfo = requests.get(url=requestURL.format(id), headers=headers).json()
#     print("Writing team details")
#     with open('Data/teams.csv', 'a', newline='\n') as teamFile:
#         writer = csv.writer(teamFile)
#         writer.writerow([teamInfo["content"]["squadDetails"]["squad"]["teamId"], teamInfo["content"]["squadDetails"]["squad"]["teamName"]])
#
#     print("Writing Player details")
#     with open('Data/players.csv', 'a', newline='\n') as playerFile:
#         writer = csv.writer(playerFile)
#         for player in teamInfo["content"]["squadDetails"]["players"]:
#             writer.writerow([player["player"]["id"], player["player"]["longName"], teamInfo["content"]["squadDetails"]["squad"]["teamId"]])
