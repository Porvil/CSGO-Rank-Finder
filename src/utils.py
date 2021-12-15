import os
import sys
import pyperclip
from player import Player
from prettytable import PrettyTable

# All CSGO Ranks
ranks = {
         -1 : "UNKNOWN",                                                             # Unknown
         0  : "EXPIRED",                                                             # Expired
         1  : "S1",    2 : "S2",    3 : "S3",    4 : "S4",    5 : "SE",   6 : "SEM", # Silver
         7  : "GN1",   8 : "GN2",   9 : "GN3",  10 : "GNM",                          # Gold Nova
         11 : "MG1",  12 : "MG2",  13 : "MGE",  14 : "DMG",                          # Master Guardian
         15 : "LE",   16 : "LEM",                                                    # Legendary Eagle
         17 : "SMFC",                                                                # Supreme
         18 : "GE"                                                                   # Global 
        }

# GLOBAL FILENAMES
CWD = os.getcwd()
FRIEND_FILENAME = "/friends.txt"
UI_FILENAME = "GUI.ui"
ICON_FILENAME = "icon.ico"
IMAGE_FOLDER =  "images/"

# URL for web scraping
URL = 'https://csgostats.gg/player/'

# UI STATIC STRING DATA
TEXT_PLACEHOLDER   = 'copy "status" command result from CSGO console and click "Show Ranks" button \n\nenter friends steam ID/steam64 ID and press "Add Friends" button to blocklist them while finding ranks'
INIT_STATUS        = 'CSGO Rank Finder'
FRIENDS_ADDED      = 'friend ID\'s successfully added to blocklist'
WRONG_FRIENDS_TEXT = 'wrong steam ID\'s or steam64 ID\'s provided'
RANKS_FOUND        = 'rank search successful'
WRONG_INPUT_TEXT   = 'wrong input provided(excluding blocklist friends from search)'

# GLOBAL DATA FOR UI
NO_OF_COLUMNS = 6
HEADER_LABELS = ["Name", "Rank", "Best Rank", "Wins", "HS %", "KD"]
HEADER_LABEL_SIZES = [175, 200, 200, 75, 75, 75]

"""
Input  - 
Output - returns "friend.txt" CWD path
"""
def getFriendsFilePath():
    return CWD + FRIEND_FILENAME

"""
Input  - 
Output - returns .ui file path used by GUI
"""
def getUIFilePath():
    return resource_path(UI_FILENAME)

"""
Input  - 
Output - returns icon file path used by GUI
"""
def getIconFilePath():
    return resource_path(ICON_FILENAME)

"""
Input  - rank of player
Output - returns path to rank image
"""
def getRankImagePath(rank):
    return resource_path(IMAGE_FOLDER) + str(rank) + ".png"

""" 
Input  - relative_path of the resource
Output - returns absolute path to resource [works for dev and for PyInstaller]
"""
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

"""
Input  - 
Output - returns data from clipboard
"""
def getClipboardData():
    return pyperclip.paste()

"""
Input  - takes string input
Output - writes the input to clipboard
"""
def sendClipboardData(data):
    return pyperclip.copy(data)

"""
Input  - 
Output - reads from file and returns list of friends(steam64id's)
"""
def readFriendsFile():
    friends = []
    fi = open(getFriendsFilePath(),"a+")
    fi.seek(0)
    for friend in fi.readlines():
        try:
            friends.append(int(friend))
        except:
            pass
    
    fi.close()
    return friends

"""
Input  - list of friends(steam64id's) and writes to file
Output - 
"""
def writeFriendsFile(friends):
    fi = open(getFriendsFilePath(),"a")
    for friend in friends:
        fi.write(str(friend) + "\n")
    
    fi.close()

"""
Input  - list of "Player" object
Output - returns PrettyTable string
"""
def getPrettyTableString(players):
    data = []
    
    for player in players:
        data.append([player.name, ranks[player.curRank], ranks[player.bestRank], player.totalWins, player.HS, player.KD])
    
    tb = PrettyTable()
    tb.field_names = HEADER_LABELS
    tb.add_rows(data)
    
    return tb.get_string()