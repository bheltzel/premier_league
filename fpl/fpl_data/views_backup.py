from django.shortcuts import render, render_to_response
from .models import Users, Players
from .sheets import sheet_dump
from .constants import *
import requests
import json


def save_league_standings(league_id, page):
    response = requests.get(url_fpl + url_standings + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(page)).json()
    with open("league_standings.json", 'w') as outfile:
        json.dump(response, outfile)

    with open("league_standings.json") as json_data:
        d = json.load(json_data)
        return d


def get_players():
    Players.objects.all().delete()
    r = requests.get(url_fpl + url_players).json()
    all_players = r["elements"]
    if not all_players:
        return None

    for player in all_players:
        p_name = player.get("web_name")
        # Players(player_name=player.get("web_name")).save()

    return None


def get_users(league_id, page):
    json_response = requests.get(url_fpl + url_standings + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(page)).json()
    json_standings = json_response["standings"]["results"]
    if not json_standings:
        return None

    # entries = []

    Users.objects.all().delete()

    row_num = 1

    for user in json_standings:
        # entries.append(user["entry_name"].encode('ascii', 'ignore'))
        u_name = user.get("entry_name")
        u_rank = user.get("rank")
        u_total = user.get("total")
        # sheet_dump(u_name, u_rank, u_total, row_num)
        print(u_name + ", " + str(u_rank) + ", " + str(u_total))
        row_num += 1
        Users(user_name=u_name, user_rank=u_rank, user_total=u_total).save()

    return None


def get_points(user_id, gameweek):
    url_league = url_fpl + "entry/" + str(user_id) + "/event/" + str(gameweek) + "/picks"
    json_response = requests.get(url_league).json()
    all_players = json_response["entry_history"]
    pts = all_players.get("points")

    map_user_name = {}
    all_users = save_league_standings(league_id_const, gameweek)

    for user in all_users["standings"]["results"]:
        map_user_name[str(user["entry"])] = user["entry_name"]

    u_name = map_user_name[user_id]
    return pts, u_name


def get_users_scores(user_id):
    for x in range(1, 13):
        pts, u_name = get_points(user_id, x)
        sheet_dump(u_name, pts, x, x)
        x += 1


def index(request):
    get_users(league_id_const, 1)
    save_league_standings(league_id_const, 1)

    # get_users_scores("2677936")
    # get_points("263672", "1")
    get_users_scores("263672")
    standings = Users.objects.order_by('-user_total')
    # standings = Users.objects.filter(user_rank=2)
    context = {'standings': standings}

    return render(request, 'fpl_data/index.html', context)


# def get_picks(user_id, gameweek):
#     url_league = url_fpl + "entry/" + str(user_id) + "/event/" + str(gameweek) + "/picks"
#     req = requests.get(url_league)
#     json_response = req.json()
#     all_players = json_response["picks"]
#     row_num = 1
#
#     for player in all_players:
#         print(player)
#         p_name = player.get("element")
#         sheet_dump(p_name, '', '', row_num)
#         row_num += 1
