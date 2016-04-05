import random
import re

from bs4 import BeautifulSoup

from gobblegobble.bot import gobble_listen
from gobblegobble.registry import RESPONSE_REGISTRY
import requests


@gobble_listen('Tell me a joke')
def test_responder(message):
    possible_replies = [
        "Do not worry, <@%s>. I only forget to recycle the Normandy's oxygen when I've discovered something truly interesting." % message.sender,
        "I enjoy the sight of humans on their knees... That is a joke. ",
        ]
    message.respond(random.choice(possible_replies))

@gobble_listen("image (.*)")
def gis(message, search_term):
    query ='+'.join(search_term)
    header = {'User-Agent': 'Mozilla/5.0'}
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    r = requests.get(url,headers=header)
    soup = BeautifulSoup(r.text)
    images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
    message.respond(images[0])

@gobble_listen("help")
def help(message):
    commands = []
    for k in RESPONSE_REGISTRY.keys():
        commands.append(k.pattern)
    message.respond("\n".join(commands))