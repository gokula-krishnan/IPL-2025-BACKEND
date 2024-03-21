import json

# open auction team list file
teamListFile = open('IPL_2023_TEAMS/teamList.json')
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
