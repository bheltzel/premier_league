from django.shortcuts import render, render_to_response
from .models import Users, Players
from .sheets import sheet_dump, bulk_sheet_dump
from .constants import *
import requests
import json


def get_users_scores(league_id, page):
    response = requests.get(url_fpl + url_standings + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(page)).json()
    with open("league_standings.json", 'w') as outfile:
        json.dump(response, outfile)

    with open("league_standings.json") as json_data:
        all_users = json.load(json_data)

    map_user_name = {}
    entries = []
    # for user in all_users["standings"]["results"]:
    #     map_user_name[str(user["entry"])] = user["entry_name"]
    #     # entries[user["entry_name"]]  #.encode('ascii', 'ignore'))
    #     print(user)
    #     for gameweek in range(1, 12):
    #         json_response = requests.get(url_fpl + "entry/" + str(user["entry"]) + "/event/" + str(gameweek) + "/picks").json()
    #         all_entries = json_response["entry_history"]
    #         pts = all_entries.get("points")
    #         u_name = map_user_name[str(user["entry"])]
    #         # sheet_dump(u_name, pts, gameweek, gameweek)
    #
    #         print(u_name + ', ' + str(pts))
    #         gameweek += 1

    for gameweek in range(1, 2):
        week_winner_name = ''
        week_winner_pts = 0
        for user in all_users["standings"]["results"]:
            json_response = requests.get(
                url_fpl + "entry/" + str(user["entry"]) + "/event/" + str(gameweek) + "/picks").json()
            map_user_name[str(user["entry"])] = user["entry_name"]

            all_entries = json_response["entry_history"]
            pts = all_entries.get("points")
            u_name = map_user_name[str(user["entry"])]
            #
            # i stopped here on 1/5. im trying to create a list so i can dump that list into the google sheet.
            # figure out how to create a list. current sheet dump bulk setup does work
            #
            entries.insert[gameweek, pts, u_name]
            if pts > week_winner_pts:
                week_winner_pts = pts
                week_winner_name = u_name

        # print(str(gameweek) + ': ' + week_winner_name + ', ' + str(week_winner_pts))
        # print(week_winner_name)
        print(entries)
        gameweek += 1
    #
    # # for user in all_users["standings"]["results"]:
    #     user_id = user.get("entry")
    #     for gameweek in range(1, 12):
    #         json_response = requests.get(url_fpl + "entry/" + str(user_id) + "/event/" + str(gameweek) + "/picks").json()
    #         all_entries = json_response["entry_history"]
    #         pts = all_entries.get("points")
    #         u_name = map_user_name[str(user_id)]
    #         # sheet_dump(u_name, pts, gameweek, gameweek)
    #
    #         gameweek += 1

    # print(map_user_name)

    # bulk_sheet_dump(map_user_name)


def get_users(league_id, page):
    json_response = requests.get(url_fpl + url_standings + str(league_id) + "?phase=1&le-page=1&ls-page=" + str(page)).json()
    json_standings = json_response["standings"]["results"]
    if not json_standings:
        return None

    Users.objects.all().delete()
    row_num = 1

    for user in json_standings:
        u_name = user.get("entry_name")
        u_rank = user.get("rank")
        u_total = user.get("total")
        # sheet_dump(u_name, u_rank, u_total, row_num)
        # print(u_name + ", " + str(u_rank) + ", " + str(u_total))
        row_num += 1
        Users(user_name=u_name, user_rank=u_rank, user_total=u_total).save()

    return None


def index(request):
    get_users(league_id_const, 1)

    get_users_scores(league_id_const, 1)

    # bulk_sheet_dump([["a1", "b1"], ["a2", "b2"]])

    standings = Users.objects.order_by('-user_total')
    context = {'standings': standings}

    return render(request, 'fpl_data/index.html', context)
