"""
Class to hold Settings data
"""
class Settings:
    def __init__(self, excludeFriends, autoFindRank, autoCopyOutput):
        self.excludeFriends = excludeFriends
        self.autoFindRank = autoFindRank
        self.autoCopyOutput = autoCopyOutput
    
    def __str__(self):
        return str(self.excludeFriends) + " " + str(self.autoFindRank) + " " + str(self.autoCopyOutput)
    
    def __repr__(self):
        return str(self)