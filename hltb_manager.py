import time
import datetime as dt
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint


class HowLongToBeat:
    def __init__(self, path):
        self.chrome_driver_path = path

    def get_beat_time(self, user_url):
        with webdriver.Chrome(executable_path=self.chrome_driver_path) as self.driver:
            self.driver.get("https://howlongtobeat.com/steam")
            self.driver.maximize_window()
            time.sleep(2)

            steam_url = self.driver.find_element_by_xpath('//*[@id="global_site"]/form/div[2]/div/div/div/input')
            steam_url.send_keys(user_url, Keys.ENTER)
            time.sleep(3)

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            game_names = [game.text for game in soup.select(".steam_table tbody .spreadsheet a")]
            game_times = [game_time.text.replace("\t", "")[:-1] for game_time in soup.select(".steam_table tbody .right")]

            for game_time in game_times:
                if game_time != "-":
                    if "h" in game_time and "m" in game_time:
                        splitted = game_time.replace("h", "").replace("m", "").split()
                        splitted[0] = int(splitted[0]) * 60
                        splitted[1] = int(splitted[1])
                        game_times[game_times.index(game_time)] = splitted[0] + splitted[1]
                    elif "h" in game_time:
                        game_times[game_times.index(game_time)] = int(game_time.replace("h", "")) * 60
                    elif "m" in game_time:
                        game_times[game_times.index(game_time)] = int(game_time.replace("m", ""))

            for game in game_names:
                name = game
                if "™" in name:
                    name = name.replace("™", "")
                if "Enhanced Edition" in name:
                    name = name.replace("Enhanced Edition", "")
                if ":" in name:
                    name = name.replace(":", " ")
                game_names[game_names.index(game)] = name

            with open(f"hltb-playtime-{dt.date.today()}.csv", "w", newline='') as file:
                fieldnames = ["game_title", "time_to_beat"]
                writer = csv.DictWriter(file, fieldnames)
                writer.writeheader()
                for (game_title, time_beat) in zip(game_names, game_times):
                    writer.writerow({"game_title": game_title.upper(), "time_to_beat": time_beat})
                print(f"\nhltb-playtime-{dt.date.today()}.csv file generated.")


if __name__ == "__main__":
    pass
