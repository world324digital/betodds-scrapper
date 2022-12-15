from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from db_manager import DbManager

class BetFair:

    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def __init__(self, epoch = 1, epoch_time = ""):
        self.epoch = epoch
        self.epoch_time = epoch_time
        self.db_manager = DbManager()
        self.total_counts = 0
        self.odds_list = []

    def fetch_data(self, item):
        link_menu = item.find_element(By.XPATH, "div/span[@class = 'section-header-label']/span[@class = 'section-header-title']")
        list_title = link_menu.text
        # print(list_title)
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
                odd_info = odd_item.find_elements(By.XPATH, "a")
                if len(odd_info) > 0:
                    if odd_index == 0:
                        first = odd_info[0].text
                    elif odd_index == 1:
                        draw = odd_info[0].text
                    elif odd_index == 2:
                        second = odd_info[0].text
                odd_index = odd_index + 1
            odd_index = 0
            for odd_item in uo_odds:
                odd_info = odd_item.find_elements(By.XPATH, "a")
                if len(odd_info) > 0:
                    if odd_index == 0:
                        over = odd_info[0].text
                    elif odd_index == 1:
                        under = odd_info[0].text
                odd_index = odd_index + 1
            # print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
            row = (list_title, "", team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "betfair", self.epoch_time)
            self.odds_list.append(row)
            self.total_counts = self.total_counts + 1
            print(self.total_counts, "matches fetched", end="\r")

    def main(self):
        self.driver.get("https://www.betfair.com/sport/football")
        if self.epoch == 1:
            time.sleep(3)
            close_btn = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            close_btn.click()
        time.sleep(3)
        soccer_menu = self.driver.find_element(By.XPATH, "//div[@class='chooser-container']//div[contains(@class, 'ui-toggle-button-options')]/span[contains(@class, 'ui-toggle-button-option')][2]/a")
        soccer_menu.click()
        time.sleep(3)
        sport_list = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'section-list')]/li")
        # print(len(sport_list))
        for i in range(len(sport_list)):
            item = sport_list[i]
            self.fetch_data(item)
        self.db_manager.insert_data(self.odds_list)
        # self.driver.quit()
        # self.driver.close()

if __name__ == "__main__":
    betfair = BetFair()
    betfair.main()