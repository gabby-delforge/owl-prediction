from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

url = "https://www.winstonslab.com/matches/match.php?id=3417"

client = urlopen(url)
page_html = client.read()
client.close()

html_soup = soup(page_html, "html.parser")

rating_container = html_soup.findAll("div", {"class": "col-md-6"})
rating_container = rating_container[2:]