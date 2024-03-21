from BattingPerformance import BattingPerformance

class Player:

    FOUR_POINTS = 2
    SIX_POINTS = 3
    MILESTONE = 25
    MILESTONE_POINTS = 10
    WICKET_POINTS = 25
    MAIDEN_POINTS = 15
    DOTS_POINTS = 1
    CATCH_POINTS = 15
    RUNOUT_POINTS = 10

    def __init__(self, id, name, teamId, battingPerfmance, bowlingPerformance, fieldingPerformance, bonus, is_motm):
        self.id = id
        self.name = name
        self.teamId = teamId
        self.battingPerfmance = battingPerfmance
        self.bowlingPerformance = bowlingPerformance
        self.fieldingPerformance = fieldingPerformance
        self.bonus = bonus
        self.is_motm = is_motm


    
    def get_data(self):
        return {
            "id" : self.id,
            "name": self.name,
            "teamId": self.teamId,
            "battingPerformance": self.battingPerfmance.get_data() if self.battingPerfmance !=0 else {},
            "bowlingPerformance": self.bowlingPerformance.get_data() if self.bowlingPerformance !=0 else {},
            "fieldingPerformance": self.fieldingPerformance.get_data() if self.fieldingPerformance !=0 else {}
        }
        # if self.battingPerfmance != 0:
        #     self.battingPerfmance.get_data()
        # else:
        #     print("NO DATA")
        
        # print("BOWL")
        # if self.bowlingPerformance != 0:
        #     self.bowlingPerformance.get_data()
        # else:
        #     print("NO DATA")

        # print("FIELD")
        # if self.fieldingPerformance != 0:
        #     self.fieldingPerformance.get_data()
        # else:
        #     print("NO DATA")

    def calculate_points(self):
        points = 0

        battingPoints = 0
        bowlingPoints = 0 
        fieldingPoints = 0

        # batting

        if self.battingPerfmance != 0:

            runs = self.battingPerfmance.get_runs()

            # 1 run = 1 pt
            battingPoints = battingPoints + runs

            # four = 2pts,six = 3pts
            battingPoints = battingPoints + (self.battingPerfmance.get_fours() * Player.FOUR_POINTS + self.battingPerfmance.get_sixes() * Player.SIX_POINTS)

            # every 25 run milestone = 10pts
            battingPoints = battingPoints + runs//Player.MILESTONE * Player.MILESTONE_POINTS

            # SR bonus = runs - balls
            battingPoints = battingPoints + (runs - self.battingPerfmance.get_balls())

            # out for duck = -10 pts
            if (self.battingPerfmance.get_out_status() == True and runs == 0):
                battingPoints = battingPoints - 10

        #bowling

        if self.bowlingPerformance != 0:
            
            wickets = self.bowlingPerformance.get_wickets()

            # 1 wicket = 25pts
            bowlingPoints = bowlingPoints + (wickets * Player.WICKET_POINTS)

            maidens = self.bowlingPerformance.get_maidens()

            # 1 maiden = 15pts
            bowlingPoints = bowlingPoints + (maidens * Player.MAIDEN_POINTS)

            dots = self.bowlingPerformance.get_dotsBowled()

            # 1 dot = 1pt
            bowlingPoints = bowlingPoints + (dots * Player.DOTS_POINTS)

            ballsBowled = self.bowlingPerformance.get_ballsBowled()
            runsConceded = self.bowlingPerformance.get_runsConceded()
            economyBonus = (2*ballsBowled) - runsConceded

            # economy = 2*balls - runs
            bowlingPoints = bowlingPoints + economyBonus

            # 3w = 25pts
            # 5w = 50pts
            # 7w = 100pts

            if wickets - 3 >=0:
                bowlingPoints += 25
            
            if wickets - 5 >=0:
                bowlingPoints += 50
            
            if wickets - 7 >=0:
                bowlingPoints += 100
        
        #fielding

        if self.fieldingPerformance != 0:

            catches = self.fieldingPerformance.get_catches()
            # 1 catch = 15pts
            fieldingPoints = fieldingPoints + catches * Player.CATCH_POINTS

            runouts = self.fieldingPerformance.get_runouts()
            # 1 runout/stumping = 10pts
            fieldingPoints = fieldingPoints + runouts * Player.RUNOUT_POINTS

        points = battingPoints + bowlingPoints + fieldingPoints
        
        return [points, battingPoints, bowlingPoints, fieldingPoints, self.is_motm]
