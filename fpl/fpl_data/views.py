from django.shortcuts import render, render_to_response
from chartit import PivotDataPool, PivotChart, DataPool, Chart

from .models import Users, Players
import requests
import math
import json

league_id_const = "270578"

url_fpl = "https://fantasy.premierleague.com/drf/"
url_standings = "leagues-classic-standings/"
url_players = "bootstrap-static"


def get_players():
    Players.objects.all().delete()
    r = requests.get(url_fpl + url_players).json()
    all_players = r["elements"]
    if not all_players:
        return None

    for player in all_players:
        # p_name = player.get("web_name")
        Players(player_name=player.get("web_name")).save()

    return None


def get_picks(user_id, gameweek):
    r = requests.get(url_fpl + "entry/" + str(user_id) + "event/" + str(gameweek) + "/picks").json()["picks"]
    if not r:
        return None

    for p in r:
        print(p["element"])


def get_gameweek_score(user_id, gameweek):
    url = url_fpl + "entry/" + str(user_id) + "/event/" + str(gameweek) + "/picks"
    print(url)
    r = requests.get(url)
    resp = r.json()
    all_picks = resp["entry_history"]
    if not all_picks:
        return None

    for u in all_picks:
        tot = u.get["total_points"]
        print(tot)

    return None


def get_users_scores(user_id):
    x = 1
    if x != 13:
        print(get_gameweek_score(user_id, x))
        x = x + 1


def get_users(league_id, page):
    url_league = url_fpl + url_standings + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(page)
    req = requests.get(url_league)
    json_response = req.json()
    json_standings = json_response["standings"]["results"]
    if not json_standings:
        return None

    entries = []

    Users.objects.all().delete()

    for user in json_standings:
        entries.append(user["entry_name"].encode('ascii', 'ignore'))
        u_name = user.get("entry_name")
        u_rank = user.get("rank")
        u_total = user.get("total")
        print(u_name + ", " + str(u_rank) + ", " + str(""))

        Users(user_name=u_name, user_rank=u_rank, user_total=u_total).save()

    return entries


def index(request):
    get_users(league_id_const, 1)
    get_users_scores("2677936")
    standings = Users.objects.order_by('-user_total')
    # standings = Users.objects.filter(user_rank=2)
    context = {'standings': standings}

    #print(standings)
    #print(Users.objects.count())
    return render(request, 'fpl_data/index.html', context)

#
# def chart():
#     ds = DataPool(
#         series=
#         [{'options': {
#             'source': Users.objects.all()},
#             'terms': [
#                 'id',
#                 'user_total',
#                 ]}
#         ])
#
#     cht = Chart(
#         datasource=ds,
#         series_options=[
#             {'options': {
#               'type': 'line',
#               'stacking': False},
#                 'terms': {
#                     'id': [
#                         'user_total']
#               }}],
#         )
#
#     return render_to_response({'cht': cht})
