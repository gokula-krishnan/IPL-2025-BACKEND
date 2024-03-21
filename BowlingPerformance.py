class BowlingPerformance:

    def __init__(self, runs, balls, dots, wickets, maidens, wides, noballs):
        self.runs = runs
        self.balls = balls
        self.dots = dots
        self.wickets = wickets
        self.maidens = maidens
        self.wides = wides
        self.noballs = noballs

    
    def get_data(self):
        return {
            "runs": self.runs,
            "balls": self.balls,
            "dots": self.dots,
            "wickets": self.wickets,
            "maidens": self.maidens,
            "wides": self.wides,
            "noballs": self.noballs
        }

    def get_runsConceded(self):
        return self.runs
    
    def get_ballsBowled(self):
        return self.balls
    
    def get_dotsBowled(self):
        return self.dots
    
    def get_wickets(self):
        return self.wickets
    
    def get_maidens(self):
        return self.maidens