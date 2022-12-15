from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from db_manager import DbManager

class Snai:

    options = Options()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def __init__(self, epoch = 1, epoch_time = ""):
        self.epoch = epoch
        self.epoch_time = epoch_time
        self.total_counts = 0
        self.db_manager = DbManager()
        self.odds_list = []

    def fetch_data(self, item):
        link_menu = item.find_element(By.XPATH, "a")
        # link_menu.click()
        self.driver.execute_script("arguments[0].click();", link_menu)
        list_title = link_menu.text
        # print(list_title)
        time.sleep(3)
        sub_list = item.find_elements(By.XPATH, "div//a[contains(@class, 'list-group-item')]")
        for sub_item in sub_list:
            # sub_item.click()
            self.driver.execute_script("arguments[0].click();", sub_item)
            sub_title = sub_item.text.replace("&nbsp;", "")
            # print("--- " + sub_title)
            time.sleep(3)
            start_time = time.time()
            delay = 0
            loading = 1
            while loading == 1:
                loading_element = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'box_container')]//div[contains(@class, 'panel-primary')]/div[contains(@ng-show, '!manif.showManif')]")
                if len(loading_element) > 0:
                    if 'ng-hide' in loading_element[0].get_attribute("class").split():
                        loading = 0
                end_time = time.time()
                delay = (int)(end_time - start_time)
                if delay >= 60:
                    loading = 0
            time.sleep(2)
            match_date_list = self.driver.find_elements(By.XPATH, "//div[contains(@ng-if, 'manif.visualizzazioneScorecast==0')]")
            # print(len(match_date_list))
            event_date = ""
            for date_item in match_date_list:
                event_date = date_item.find_element(By.XPATH, "h4/a").text
                match_list = date_item.find_elements(By.XPATH, "div/div[contains(@class, 'container-fluid container-fluid-custom')]/div[contains(@class, 'rowPref ng-scope')]")
                # print(len(match_list))
                event_time = ""
                for match_item in match_list:
                    event_time = match_item.find_element(By.XPATH, "div/div[contains(@class, 'matchDescriptionFirstCol')]/*[contains(@class, 'hourMatchFootball')]").text
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
                    equal = match_item.find_element(By.XPATH, "div/div[contains(@class, 'matchDescriptionFirstCol')]/*[contains(@class, 'descriptionTextBlue')]").text
                    team1 = equal.split("-")[0]
                    team2 = equal.split("-")[1]
                    event_odds = match_item.find_elements(By.XPATH, "div/div[contains(@class, 'ng-scope')]/div")
                    odd_index = 0
                    for odd_item in event_odds:
                        if odd_index == 6:
                            odd_info = odd_item.find_element(By.XPATH, "span[contains(@class, 'footballBlueBetting')]")
                            first = odd_info.text
                        elif odd_index == 5:
                            odd_info = odd_item.find_element(By.XPATH, "span[contains(@class, 'footballBlueBetting')]")
                            draw = odd_info.text
                        elif odd_index == 4:
                            odd_info = odd_item.find_element(By.XPATH, "span[contains(@class, 'footballBlueBetting')]")
                            second = odd_info.text
                        elif odd_index == 3:
                            uo_info = odd_item.find_elements(By.XPATH, "div/span[contains(@class, 'footballBlueBetting')]")
                            if len(uo_info) > 0:
                                under = uo_info[0].text
                            else:
                                under = odd_info.text
                        elif odd_index == 2:
                            uo_info = odd_item.find_elements(By.XPATH, "div/span[contains(@class, 'footballBlueBetting')]")
                            if len(uo_info) > 0:
                                over = uo_info[0].text
                            else:
                                over = odd_info.text
                        elif odd_index == 1:
                            odd_info = odd_item.find_element(By.XPATH, "span[contains(@class, 'footballBlueBetting')]")
                            gg = odd_info.text
                        elif odd_index == 0:
                            odd_info = odd_item.find_element(By.XPATH, "span[contains(@class, 'footballBlueBetting')]")
                            ng = odd_info.text
                        odd_index = odd_index + 1
                    row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "snai", self.epoch_time)
                    # self.db_manager.insert_row(row)
                    if self.total_counts == 200:
                        self.db_manager.insert_data(self.odds_list)
                        self.odds_list = []
                        self.total_counts = 0
                    if team1 != "" and team2 != "":
                        # print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng + " " + self.epoch_time)
                        self.odds_list.append(row)
                        self.total_counts = self.total_counts + 1
                    # print(list_title, sub_title, self.total_counts, "matches fetched", end="\r")

    def main(self):
        self.driver.get("https://www.snai.it/sport")
        if self.epoch == 1:
            time.sleep(3)
            close_btn = self.driver.find_element(By.ID, "cookie_consent_banner_closer")
            close_btn.click()
        soccer_menu = self.driver.find_element(By.ID, "heading_0")
        soccer_menu.click()
        time.sleep(5)
        soccer_sidebar = self.driver.find_element(By.ID, "CALCIO_0")
        sport_list = soccer_sidebar.find_elements(By.XPATH, "div[contains(@class, 'panel-body')]/div[contains(@class, 'subOne')]/div")
        # print(len(sport_list))
        for i in range(len(sport_list)):
            item = sport_list[i]
            # print(item.get_attribute("outerHTML"))
            # print("===============")
            self.fetch_data(item)
        self.db_manager.insert_data(self.odds_list)
        # self.driver.quit()
        # self.driver.close()

    def run(self):
        threading.Timer(1800, self.run).start()
        now_time = datetime.fromtimestamp(time.time())
        self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        print(self.epoch, self.epoch_time)
        self.main()
        self.epoch = self.epoch + 1

if __name__ == "__main__":
    snai = Snai()
    snai.run()