import cloudscraper
import json
import re
from bs4 import BeautifulSoup

from utils import *

"""
Input  - steamid
Output - returns steam64id if found, else -1
"""
def steamIdToSteamId64(steamId):
    steamId64 = -1
    try:
        Universe = int(steamId[6:7])
        AccountType = 1
        AccountInstance = 1
        AccountNumber = int(steamId[10:])
        IDNumber = int(steamId[8:9])
        
        steamId64 = ( (Universe << 56) | (AccountType << 52) | (AccountInstance << 32) | (AccountNumber << 1) | IDNumber )
    except:
        pass
    return steamId64

"""
Input  - "status" command's output from CSGO console
Output - returns list of steam64id's
"""
def extractSteam64Ids(data):
    splitdata = data.splitlines()
    Ids = set()
    
    for line in splitdata:
        try:
            steamId = line.split()[-6]
            steamId64 = steamIdToSteamId64(steamId)
            if steamId64 != -1:
                Ids.add(steamId64)
        except:
            continue
    
    return Ids

"""
Input  - steam64id of player and list of friends to exclude from search
Output - returns json data(stats of player) scraped from internet
"""
def scraper(steam64id):
    url = URL + str(steam64id)
    flag = False
    while not flag:
        try:
            sc = cloudscraper.create_scraper()
            html_text = sc.get(url).text
            flag = True
        except:
            continue
        
    p = re.compile('var stats = .*')
    soup = BeautifulSoup(html_text, 'lxml')
    name = soup.find('div', id='player-name')
    scripts = soup.find_all('script')
    data = ''
    for script in scripts:
        try:
            m = p.match(script.string.strip())
            if m:
                data = m.group()
                break
        except:
            continue

    data_json = json.loads(data[12:-1])
    data_json['player_name'] = name.text
    return data_json

"""
Input  - steam64id of player and list of friends to exclude from search
Output - returns "Player" object if found, else None
"""
def getPlayerRank(steam64id, friends):
    if steam64id not in friends:
        data_json = scraper(steam64id)
        player_name = data_json['player_name']
        curr_rank = data_json['rank']
        best_rank = data_json['best']['rank']
        total_wins = data_json['comp_wins']
        headshot_rate = data_json['overall']['hs']
        kills_per_death = data_json['overall']['kpd'] 
        
        player = Player(player_name, curr_rank, best_rank, total_wins, headshot_rate, kills_per_death)
        print(player.getPrintableString(ranks))
        
        return player
    
    return None

"""
Input  - "status" command's output from CSGO console
Output - returns list of "Player" object
"""
def getRanks(status):
    friends = readFriendsFile()
    Ids = extractSteam64Ids(status)
    players = []
    for id in Ids:
        player = getPlayerRank(id, friends)
        if player != None:
            players.append(player)
    
    return players