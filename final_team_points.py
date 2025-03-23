import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# open auction team list file
teamListFile = open('IPL_2025_TEAMS/teamList.json')
teamListData = json.load(teamListFile)

#  initialise results
results = {}

#  load playerPoints file
pointFile = open('./Data/playerPoints.json')
pointsData = json.load(pointFile)

# loop through the team list
for team in teamListData:
    playersList = teamListData[team]
    # initialise team in results blob
    results[team] = ''
    # initialise pointSum for each team
    pointSum = []
    # for each player in team list, get points and add to pointSum
    for player in playersList:
        for x in pointsData['Players']:
            if x['id'] == player:
                pointSum.append(x['totalPoints'])
                pointSum.extend([25 for match in x['scores'] if match['isMOTM']])
    # store to the results blob
    results[team] = sum(pointSum)

# sort by points
sortList = sorted(results.items(), key=lambda x: x[1],reverse=True)
for team in sortList:
    print(team)


# Function to update Gist content
def update_gist():
    # Read JSON data from file
    # Prepare Gist payload
    payload = {
        "files": {}
    }

    # Iterate through each key-value pair in JSON data and add to payload
    payload["files"][os.getenv('gist_file_name')] = {"content": json.dumps(pointsData)}

    # Prepare headers with access token
    headers = {
        "Authorization": f"Bearer {os.getenv('access_token')}",
        "Accept": "application / vnd.github + json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Make PATCH request to update Gist
    response = requests.patch(f"https://api.github.com/gists/{os.getenv('gist_id')}", headers=headers, json=payload)

    # Check if update was successful
    if response.status_code == 200:
        print("Gist content updated successfully.")
    else:
        print(f"Failed to update Gist. Status code: {response.status_code}")
        print(f"Error message: {response.text}")


update_gist()
