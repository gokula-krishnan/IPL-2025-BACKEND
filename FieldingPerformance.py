class FieldingPerformance:

    def __init__(self, catches, runouts):
        self.catches = catches
        self.runouts = runouts

    
    def get_data(self):
        return {
            "catches": self.catches,
            "runoutsAndStumpings": self.runouts
        }

    def get_catches(self):
        return self.catches

    # Both stumping and runouts included
    def get_runouts(self):
        return self.runouts