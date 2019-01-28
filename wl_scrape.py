from lxml import html
import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup


url = 'https://www.winstonslab.com/matches/match.php?id=3417'
page_response = requests.get(url, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")
allRows = []
mapNames = []
rows = page_content.find_all("tr")[15:]

data = []
maps_raw = page_content.findAll("div", {"class": "mapname"})
maps = [maps_raw[i].attrs['title'] for i in range(len(maps_raw)//2)]

map_idx = -1
count = 0

for r in rows:
    player = [re.findall(r"[^\n\t]+", r.text)]
    if player[0][0] == "Player":
        continue
    if count%12 == 0:
        map_idx += 1
    data += [player + [maps[map_idx]]]
    count += 1

print([re.findall(r"[^\n\t]+", rows[0].text)]+["Map"])
for d in data:
    print(d)









