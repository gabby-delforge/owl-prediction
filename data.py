from bs4 import BeautifulSoup
import requests
import pickle

URLS = [
    "ranking",
    "schedule",
    "matches",
    "match",
    "teams",
    "news",
    "data/countries",
    # "v2/email",
    "live-match",
    "v2/streams",
    "maps",
    "vods",
    "live-match",
    # "players",
    "standings"
]

OWL = []

def retrieve_data():
    """Deserialize data."""
    with open('data/owl_data.bin', 'rb') as pickle_file:
        data = pickle.load(pickle_file)
        return data

def retrieve_classes():
    """Deserialize classes."""
    with open('data/owl_classes.bin', 'rb') as pickle_file:
        classes = pickle.load(pickle_file)
        return classes


def get_url(query):
    if query in URLS:
        return "https://api.overwatchleague.com/" + query
    else:
        return "Error: Could not retrieve url: https://api.overwatchleague.com/" + query


def update_data():
    """Update and serialize data."""
    for url in URLS:
        RAW_DATA[url] = BeautifulSoup(requests.get(get_url(url)).text, "html.parser")
        print(str(url) + ": " + str(RAW_DATA[url]))

    with open('data/owl_data.bin', mode='wb') as binary_file:
        pickle.dump(RAW_DATA, binary_file)

    with open('data/owl_classes.bin', mode='wb') as classes_file:
        pickle.dump(OWL, classes_file)


def start():
    return


def update_classes():
    """Update data structures."""
    return


class Owl:
    """List of seasons."""
    def __init__(self):
        self.seasons = []


class Season:
    """List of teams, season standings."""
    def __init__(self):
        self.teams = []


class Stage:
    """"Stage standings."""
    def __init__(self):
        self.standings = []


class Match:
    """Competing teams, match data, winner."""
    def __init__(self):
        self.teams = []


class Team:
    """List of players, cumulative team stats."""
    def __init__(self):
        self.players = []


class Player:
    """Cumulative player stats."""
    def __init__(self):
        self.playtime = 0


RAW_DATA = retrieve_data()
OWL = retrieve_classes()
update_data()
update_classes()
