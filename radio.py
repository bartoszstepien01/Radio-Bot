import requests
from bs4 import BeautifulSoup, element
from json import loads
from cryptor import Cryptor, hash

def search(query):
    response = requests.get("https://mytuner-radio.com/search/", params={
        "q": query
    })

    soup = BeautifulSoup(response.content, features="lxml")
    radio_list = soup.find("ul", {"class": "radio-list"}).children
    radio = next(radio_list)
    while type(radio) is element.NavigableString:
        radio = next(radio_list)

    return {
        "id": "https://mytuner-radio.com" + radio.find("a").get("href"),
        "name": radio.find("span").text.strip()
    }

def streams(id):
    response = requests.get(id)

    soup = BeautifulSoup(response.content, features="lxml")

    key = hash(soup.find("div", {"id": "last-update"}).get("data-timestamp"))
    for line in response.text.split("\n"):
        if "var _playlist" in line:
           streams = loads(line[line.find("(")+1:line.rfind(")")])
    
    return [Cryptor.decrypt(stream["cipher"], key, stream["iv"]) for stream in streams]