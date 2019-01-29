import requests
import re
import csv
from bs4 import BeautifulSoup
import data.wl_source as src

"""
------------
MATCH DATA:
------------
team1- Home Team
team2- Away Team

------------
MAP DATA:
------------
data- List of
[Match_ID | Map | Player | K | D | +/- | Ults | FK Diff | Rating | Hero-Ratings | Show K-D(U)]
map_rosters- List of
[Match_ID | Map | Team | Player 1 | Player 2 | Player 3 | Player 4 | Player 5 | Player 6]

"""

matches = src.s1_match_IDs

def update_data(match_ID):
    url = 'https://www.winstonslab.com/matches/match.php?id=' + str(match_ID)
    page_response = requests.get(url, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")


    team1 = re.findall(r"[^\n\t]+", page_content.find("div", {"class": "team1-name"}).text)[0]
    team2 = re.findall(r"[^\n\t]+", page_content.find("div", {"class": "team2-name"}).text)[0]

    data = []
    allRows = []
    mapNames = []
    rows = page_content.find_all("tr")
    for i in range(len(rows)):
        player = [re.findall(r"[^\n\t]+", rows[i].text)]
        if player[0][0] == "Player-Hero Combo of the match":
            rows = rows[i+1:]
            break
    maps_raw = page_content.findAll("div", {"class": "mapname"})
    maps = [maps_raw[i].attrs['title'] for i in range(len(maps_raw)//2)]
    map_idx = -1
    count = 0
    map_rosters = []
    p = []
    team = team2
    for r in rows:
        player = [re.findall(r"[^\n\t]+", r.text)][0]
        if player[0] == "Player":
            map_rosters.append(p)
            p = []
            team = team1 if team == team2 else team2
            p.append(match_ID)
            p.append(maps[map_idx])
            p.append(team)
            continue
        if count%12 == 0:
            map_idx += 1
        p.append(player[0])
        player.insert(0, maps[map_idx])
        player.insert(0, match_ID)
        data.append(player)
        count += 1
    map_rosters.append(p)
    map_rosters.pop(0)
    return map_rosters, data


"""print(["Match ID"]+["Map"] + re.findall(r"[^\n\t]+", rows[0].text))
for d in data:
    print(d)"""


m = open('player_match.csv', mode='w')
n = open('map_rosters.csv', mode='w')

m_writer = csv.writer(m, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
n_writer = csv.writer(n, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

m_writer.writerow(['Match ID', 'Map', 'Player', 'K', 'D', '+/-', 'Ults', 'FK Diff', 'Rating', 'Hero-Ratings', 'Show K-D(U)'])
n_writer.writerow(['Match_ID', 'Map', 'Team','Player 1','Player 2','Player 3', 'Player 4','Player 5', 'Player 6'])

for item in matches:
    data, map_rosters = update_data(id)
    for r in data:
        m_writer.writerow(r)
    for r in map_rosters:
        n_writer.writerow(r)

m.close()
n.close()







