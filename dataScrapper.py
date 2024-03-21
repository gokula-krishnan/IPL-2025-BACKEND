import requests
import json
import os
from Player import Player
from dotenv import load_dotenv
from BattingPerformance import BattingPerformance
from BowlingPerformance import BowlingPerformance 
from FieldingPerformance import FieldingPerformance

load_dotenv()

matchStartId = int(os.getenv("MATCH_START_ID"))
matchEndId = int(os.getenv("MATCH_END_ID"))
match_url = os.getenv("MATCH_URL")
series_id = os.getenv("SERIES_ID")


def getBattingPerformance(id, inningsData):
    isOut = False
    for inning in inningsData:
        if inning["inningNumber"] <= 2:
            battingStats = inning["inningBatsmen"]
            for battingStat in battingStats:
                if battingStat["player"]["id"] == id:
                    isOut = battingStat["isOut"]
                    return BattingPerformance(battingStat["runs"], battingStat["balls"], battingStat["fours"], battingStat["sixes"], isOut)
    return 0

def getBowlingPerformance(id, inningsData):
    for inning in inningsData:
        if inning["inningNumber"] <= 2:
            bowlingStats = inning["inningBowlers"]
            for bowlingStat in bowlingStats:
                if bowlingStat["player"]["id"] == id:
                    return BowlingPerformance(bowlingStat["conceded"], bowlingStat["balls"], bowlingStat["dots"], bowlingStat["wickets"], bowlingStat["maidens"], bowlingStat["wides"], bowlingStat["noballs"])
    return 0

def getFieldingPerformance(id, inningsData):
    playerCatches = 0
    playerRunouts = 0
    for inning in inningsData:
        if inning["inningNumber"] <= 2:
            wicketStats = inning["inningWickets"]
            for wicketStat in wicketStats:
                dismissedMethod = wicketStat["dismissalType"]
                dismissalFielderIds = []
                for fielder in wicketStat["dismissalFielders"]:
                    if fielder["player"] != None:
                        dismissalFielderIds.append(fielder["player"]["id"])
                if dismissedMethod == 1 and id in dismissalFielderIds:
                    playerCatches = playerCatches + 1
                elif (dismissedMethod == 4 or dismissedMethod == 5) and id in dismissalFielderIds:
                    playerRunouts = playerRunouts + 1

    if playerRunouts + playerCatches > 0:
        return FieldingPerformance(playerCatches, playerRunouts)

    return 0


def get_motm_award(player_id, match_player_awards):
    is_motm = False
    if len(match_player_awards) != 0:
        if match_player_awards[0]["player"]["id"] == player_id:
            is_motm = True
    return is_motm


for i in range(int(matchStartId), int(matchEndId)+1):
    print(i)
    currentMatchId = i
    requestURL = match_url+"?lang=en&seriesId="+series_id+"&matchId={0}".format(str(currentMatchId))

    matchResponseData = requests.get(url=requestURL)
    matchData = matchResponseData.json()
    teams = matchData["match"]["teams"]

    teamIdCount = teams[0]["team"]["id"] + teams[1]["team"]["id"]

    playerInformationDictionary = {}

    for playersForATeam in matchData["content"]["matchPlayers"]["teamPlayers"]:
        for player in playersForATeam["players"]:
            playerInfo = Player(player["player"]["id"], player["player"]["longName"], playersForATeam["team"]["id"], getBattingPerformance(player["player"]["id"], matchData["content"]["innings"]), getBowlingPerformance(player["player"]["id"], matchData["content"]["innings"]), getFieldingPerformance(player["player"]["id"], matchData["content"]["innings"]), 0, get_motm_award(player["player"]["id"], matchData["content"]["matchPlayerAwards"]))
            playerInformationDictionary[player["player"]["id"]] = playerInfo

    pointsList = []

    with open("sample.json", "r") as jsonFile:
        pointsData = json.load(jsonFile)

    for id, playerInfo in playerInformationDictionary.items():
        playerData = playerInfo.get_data()
        playerPoints = playerInfo.calculate_points()

        playerFound = False
        counter = -1
        for player in pointsData["Players"]:
            counter = counter + 1
            if playerData["id"] == player["id"]:
                playerFound = True
                matchFound = False
                matchCounter = -1
                for match in player["scores"]:
                    matchCounter = matchCounter + 1
                    if match["matchId"] == currentMatchId:
                        matchFound = True
                        #prevMotm = pointsData["Players"][counter]["scores"][matchCounter]["isMOTM"]
                        prevPoints = pointsData["Players"][counter]["scores"][matchCounter]["points"]
                        pointsData["Players"][counter]["scores"][matchCounter]["matchId"] = currentMatchId
                        pointsData["Players"][counter]["scores"][matchCounter]["opponentTeamId"] = abs(teamIdCount - playerData["teamId"])
                        pointsData["Players"][counter]["scores"][matchCounter]["battingPerformance"] = playerData["battingPerformance"]
                        pointsData["Players"][counter]["scores"][matchCounter]["bowlingPerformance"] = playerData["bowlingPerformance"]
                        pointsData["Players"][counter]["scores"][matchCounter]["fieldingPerformance"] = playerData["fieldingPerformance"]
                        pointsData["Players"][counter]["scores"][matchCounter]["battingPoints"] = playerPoints[1]
                        pointsData["Players"][counter]["scores"][matchCounter]["bowlingPoints"] = playerPoints[2]
                        pointsData["Players"][counter]["scores"][matchCounter]["fieldingPoints"] = playerPoints[3]
                        pointsData["Players"][counter]["scores"][matchCounter]["points"] = playerPoints[0]
                        #pointsData["Players"][counter]["scores"][matchCounter]["isMOTM"] = prevMotm
                        pointsData["Players"][counter]["scores"][matchCounter]["isMOTM"] = playerPoints[4]
                        pointsData["Players"][counter]["totalPoints"] -= prevPoints
                        break

                if matchFound == False:
                    pointsData["Players"][counter]["scores"].append({
                        "matchId": currentMatchId,
                        "opponentTeamId": abs(teamIdCount - playerData["teamId"]),
                        "battingPerformance": playerData["battingPerformance"],
                        "bowlingPerformance": playerData["bowlingPerformance"],
                        "fieldingPerformance": playerData["fieldingPerformance"],
                        "battingPoints": playerPoints[1],
                        "bowlingPoints": playerPoints[2],
                        "fieldingPoints": playerPoints[3],
                        "points": playerPoints[0],
                        "isMOTM": playerPoints[4]
                    })
                pointsData["Players"][counter]["totalPoints"] += playerPoints[0]
                break

        if playerFound == False:
            pointsData["Players"].append({
                "id": playerData["id"],
                "name": playerData["name"],
                "teamId": playerData["teamId"],
                "totalPoints": playerPoints[0],
                "scores": [
                    {
                        "matchId": currentMatchId,
                        "opponentTeamId": abs(teamIdCount - playerData["teamId"]),
                        "battingPerformance": playerData["battingPerformance"],
                        "bowlingPerformance": playerData["bowlingPerformance"],
                        "fieldingPerformance": playerData["fieldingPerformance"],
                        "battingPoints": playerPoints[1],
                        "bowlingPoints": playerPoints[2],
                        "fieldingPoints": playerPoints[3],
                        "points": playerPoints[0],
                        "isMOTM": playerPoints[4]
                    }
                ]
            })

    with open("sample.json", "w") as f:
        json.dump(pointsData, f)

with open("sample.json", "r") as jsonFile:
    final_points_data = json.load(jsonFile)

with open("./Data/playerPoints.json", "w") as f:
    json.dump(final_points_data, f)
