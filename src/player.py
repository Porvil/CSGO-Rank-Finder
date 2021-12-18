from unidecode import unidecode

"""
Class to hold data for a player
"""
class Player:
    def __init__(self, name, curRank, bestRank, totalWins, HS, KD):
        self.name = name
        self.curRank = curRank
        self.bestRank = bestRank
        self.totalWins = totalWins
        self.HS = HS
        self.KD = KD
    
    def __str__(self):
        return unidecode(self.name) + " " + str(self.curRank) + " " + str(self.bestRank) + " " + str(self.totalWins) + " " + str(self.HS) + " " + str(self.KD)
    
    def getPrintableString(self, ranks):
        return unidecode(self.name) + " " + str(ranks[self.curRank]) + " " + str(ranks[self.bestRank]) + " " + str(self.totalWins) + " " + str(self.HS) + " " + str(self.KD)
    
    def __repr__(self):
        return str(self)
    
    def getCopyString(self):
        return str(self.name) + " " + str(self.curRank) + " " + str(self.bestRank) + " " + str(self.totalWins) + " " + str(self.HS) + " " + str(self.KD)