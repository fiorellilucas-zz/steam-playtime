import requests
import hltb_manager
import datetime as dt
import csv
from pprint import pprint

API_ENDPOINT = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001"

print("ATTENTION! YOUR STEAM PROFILE MUST BE PUBLIC FOR THIS PROGRAM TO WORK\n")
print("Download the WebDriver for Chrome from https://chromedriver.chromium.org/.")
print("Go to https://steamcommunity.com/dev, follow the instructions and grab your Steam API Key.\n")

steam_api_key = str(input("Steam API Key: "))
steam_id = str(input("Steam profile ID: "))
steam_url = str(input("Steam profile URL: "))
chrome_webdriver_path = str(input("Chrome WebDriver Path: "))

params = {
    "steamid": steam_id,
    "include_appinfo": "true",
    "key": steam_api_key,
}

response = requests.get(url=API_ENDPOINT, params=params)
response.raise_for_status()

games_list = response.json()["response"]["games"]
hltb_mng = hltb_manager.HowLongToBeat(chrome_webdriver_path)

steam_playtime = {}

for game in games_list:
    name = game["name"]
    if "™" in name:
        name = name.replace("™", "")
    if "Enhanced Edition" in name:
        name = name.replace("Enhanced Edition", "")
    if ":" in name:
        name = name.replace(":", " ")
    steam_playtime[name.rstrip().lstrip()] = game["playtime_forever"]

hltb_playtime = hltb_mng.get_beat_time(steam_url)

with open(f"steam-playtime-{dt.date.today()}.csv", "w", newline='') as file:
    fieldnames = ["game_title", "playtime_forever"]
    writer = csv.DictWriter(file, fieldnames)
    writer.writeheader()
    for (game_title, playtime) in steam_playtime.items():
        writer.writerow({"game_title": game_title.upper(), "playtime_forever": playtime})
    print(f"steam-playtime-{dt.date.today()}.csv file generated.")

