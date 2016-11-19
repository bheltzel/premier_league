from django.shortcuts import render

from .models import Users
from django.http import HttpResponse
from django.template import loader
import requests
import json
import csv

league_id_const = "270578"

url_fpl = "https://fantasy.premierleague.com/drf/"
url_standings = "leagues-classic-standings/"
url_players = "boostrap-static"


def get_users(league_id, page):
    url_league = url_fpl + url_standings + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(page)
    req = requests.get(url_league)
    json_response = req.json()
    json_data = json.loads(req.text)
    standings = json_response["standings"]["results"]
    if not standings:
        return None

    entries = []

    Users.objects.all().delete()

    for player in standings:
        entries.append(player["entry_name"].encode('ascii', 'ignore'))
        p_name = player.get("entry_name")
        p_rank = player.get("rank")
        entries.append(player["rank"])
        # rank = 1
        print(p_name + ", " + str(p_rank))

        u = Users(user_name=p_name, user_rank=p_rank)
        u.save()

    return entries


def index(request):
    get_users(league_id_const, 1)
    standings = Users.objects.order_by('user_rank')
    template = loader.get_template('fpl_data/index.html')
    context = {
        'standings': standings,
    }
    # output = ', '.join(u.user_name for u in standings)
    return HttpResponse(template.render(context, request))



