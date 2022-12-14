from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import mysql.connector
from datetime import datetime
# from db_manager import DbManager

class BetFair:

    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("headless")
    options.add_argument("window-size=1200x600")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def __init__(self, epoch = 1, epoch_time = ""):
        self.epoch = epoch
        self.epoch_time = epoch_time
        self.total_counts = 0
        # self.db_manager = DbManager()
        self.odds_list = []
        self.host = "45.8.227.145"
        self.user = "oddsmatcher"
        self.password = "~exY([5~fjxN"
        self.database = "oddsmatcher-353030358ce0"
        self.port = "57558"

    def fetch_data(self, item):
        link_menu = item.find_element(By.XPATH, "div/span[@class = 'section-header-label']/span[@class = 'section-header-title']")
        list_title = link_menu.text
        print(list_title)
        temp_list = []
        match_list = item.find_elements(By.XPATH, "ul[contains(@class, 'event-list')]/li")
        for match_item in match_list:
            time_element = match_item.find_elements(By.XPATH, "div/div[contains(@class, 'avb-col-inplay')]//span[contains(@class, 'date')]")
            if len(time_element) > 0:
                event_date = time_element[0].text
                event_time = event_date
            else:
                event_date = ""
                event_time = ""
            team1 = ""
            team2 = ""
            equal = ""
            first = ""
            draw = ""
            second = ""
            under = ""
            over = ""
            gg = ""
            ng = ""
            teams = match_item.find_elements(By.XPATH, "div/div[contains(@class, 'avb-col-runners')]//*[contains(@class, 'team-name')]")
            if len(teams) != 0:
                team1 = teams[0].text
                team2 = teams[1].text
            equal = team1 + " - " + team2
            odds = match_item.find_elements(By.XPATH, "div/div[contains(@class, 'avb-col-markets')]//div[contains(@class, 'details-market market-3-runners')]/div[contains(@class, 'runner-list')]//li")
            uo_odds = match_item.find_elements(By.XPATH, "div/div[contains(@class, 'avb-col-markets')]//div[contains(@class, 'details-market market-2-runners')]/div[contains(@class, 'runner-list')]//li")
            odd_index = 0
            for odd_item in odds:
                odd_info = odd_item.find_elements(By.XPATH, "a/span")
                if len(odd_info) > 0 and odd_info[0].text != "":
                    if odd_index == 0:
                        first = odd_info[0].text
                    elif odd_index == 1:
                        draw = odd_info[0].text
                    elif odd_index == 2:
                        second = odd_info[0].text
                odd_index = odd_index + 1
            odd_index = 0
            for odd_item in uo_odds:
                odd_info = odd_item.find_elements(By.XPATH, "a/span")
                if len(odd_info) > 0:
                    if odd_index == 0:
                        over = odd_info[0].text
                    elif odd_index == 1:
                        under = odd_info[0].text
                odd_index = odd_index + 1
            print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
            row = (list_title, "", team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "betfair", self.epoch_time)
            self.odds_list.append(row)
            # self.db_manager.insert_row(row)
            # self.insert_row(row)
            # temp_list.append(row)
            self.total_counts = self.total_counts + 1
            # print(self.total_counts, "matches fetched", end="\r")
        # self.insert_data(temp_list)

    def main(self):
        start_time = time.time()
        now_time = datetime.fromtimestamp(time.time())
        self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        self.driver.get("https://www.betfair.it/sport/football")
        if self.epoch == 1:
            time.sleep(3)
            close_btn = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            close_btn.click()
        self.epoch = self.epoch + 1
        time.sleep(3)
        soccer_menu = self.driver.find_element(By.XPATH, "//div[@class='chooser-container']//div[contains(@class, 'ui-toggle-button-options')]/span[contains(@class, 'ui-toggle-button-option')][2]/a")
        soccer_menu.click()
        time.sleep(3)
        sport_list = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'section-list')]/li")
        # print(len(sport_list))
        for i in range(len(sport_list)):
            item = sport_list[i]
            self.fetch_data(item)
        # time.sleep(1800)
        self.insert_data(self.odds_list)
        print("completed time is ", time.time() - start_time)
        # self.main()
        self.odds_list = []
        self.total_counts = 0
        self.driver.quit()
        # self.driver.close()

    def run(self):
        threading.Timer(3600, self.run).start()
        now_time = datetime.fromtimestamp(time.time())
        print("BetFair =======> ", self.total_counts, "Matches Saved")
        self.total_counts = 0
        self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        print(self.epoch, self.epoch_time)
        self.main()

    def insert_row(self, odds_list):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            port = self.port
        )
        sql = "INSERT INTO `python_odds_table_new` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor = mydb.cursor()
        mycursor.execute(sql, odds_list)
        mydb.commit()
        mycursor.close()

    def insert_data(self, odds_list):
        if len(odds_list) > 0:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                port = self.port
            )
            sql = "UPDATE `python_odds_table_new` SET `deleted_at` = CURRENT_TIMESTAMP WHERE `bookmarker` = '" + odds_list[0][-2] + "';"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
            mycursor.close()
            sql = "INSERT INTO `python_odds_table_new` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor = mydb.cursor()
            mycursor.executemany(sql, odds_list)
            mydb.commit()
            mycursor.close()

if __name__ == "__main__":
    betfair = BetFair()
    betfair.main()