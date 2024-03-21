class BattingPerformance:

    def __init__(self, runs, balls, fours, sixes, isOut):
        self.runs = runs if runs != None else 0
        self.balls = balls if balls != None else 0
        self.fours = fours if fours != None else 0
        self.sixes = sixes if sixes != None else 0
        self.isOut = isOut
    
    def get_data(self):
        return {
            "runs": self.runs,
            "balls": self.balls,
            "fours": self.fours,
            "sixes": self.sixes,
            "isOut": self.isOut
        }

    def get_runs(self):
        return int(self.runs)
    
    def get_balls(self):
        return int(self.balls)
    
    def get_fours(self):
        return int(self.fours)

    def get_sixes(self):
        return int(self.sixes)

    def get_out_status(self):
        return self.isOut