from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fp.fp import FreeProxy
import time

options = Options()
proxy = FreeProxy(country_id=["ID"], https=True).get()
proxy = proxy.replace("http://", "")
proxy = proxy.replace("https://", "")
# proxy = "134.238.252.143:8080"
print(proxy)
options.add_argument("start-maximized")
options.add_argument("--proxy-server=" + proxy)
options.add_argument("ignore-certificate-errors")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fetch_data(item):
	item.click()
	list_title = item.find_element(By.XPATH, "a").text
	print(list_title)
	time.sleep(3)
	sub_list = item.find_elements(By.XPATH, "ul/li")
	for sub_item in sub_list:
		sub_item.click()
		sub_title = sub_item.find_element(By.XPATH, "a").text
		print("--- " + sub_title)
		time.sleep(3)
		match_list = driver.find_elements(By.XPATH, "//div[@class='containerEvents']/div")
		# print(len(match_list))
		for match_item in match_list:
			time_info = match_item.get_attribute("c_dat")
			event_date = time_info.split("T")[0]
			event_time = time_info.split("T")[1]
			equal = match_item.get_attribute("c_dav")
			team1 = equal.split(" - ")
			team2 = equal.split(" - ")
			first = ""
			draw = ""
			second = ""
			under = ""
			over = ""
			gg = ""
			ng = ""
			event_odds = match_item.find_elements(By.XPATH, "*[@class='bets']/div[contains(@class, 'odds p1')]//div[contains(@class, 'oddPrematch')]")
			odd_index = 0
			for odd_item in event_odds:
				odd_info = odd_item.find_elements(By.XPATH, "div/a")
				locked = 0
				if 'lock' in odd_item.get_attribute("class").split():
					locked = 1
				else:
					if odd_index == 0:
						first = odd_item.get_attribute("c_quo")
					elif odd_index == 1:
						draw = odd_item.get_attribute("c_quo")
					elif odd_index == 2:
						second = odd_item.get_attribute("c_quo")
				odd_index = odd_index + 1
			event_odds = match_item.find_elements(By.XPATH, "*[@class='bets']/div[contains(@class, 'odds p2')]//div[contains(@class, 'oddPrematch')]")
			odd_index = 0
			for odd_item in event_odds:
				odd_info = odd_item.find_elements(By.XPATH, "div/a")
				locked = 0
				if 'lock' in odd_item.get_attribute("class").split():
					locked = 1
				else:
					if odd_index == 0:
						gg = odd_item.get_attribute("c_quo")
					elif odd_index == 1:
						ng = odd_item.get_attribute("c_quo")
				odd_index = odd_index + 1
			event_odds = match_item.find_elements(By.XPATH, "*[@class='bets']/div[contains(@class, 'odds p3')]//div[contains(@class, 'oddPrematch')]")
			odd_index = 0
			for odd_item in event_odds:
				odd_info = odd_item.find_elements(By.XPATH, "div/a")
				locked = 0
				if 'lock' in odd_item.get_attribute("class").split():
					locked = 1
				else:
					if odd_index == 0:
						under = odd_item.get_attribute("c_quo")
					elif odd_index == 1:
						over = odd_item.get_attribute("c_quo")
				odd_index = odd_index + 1
			print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
		sub_item.click()

def main():
    driver.get("https://www.betaland.it/")
    time.sleep(500)
    cookie_close_btn = driver.find_element(By.ID, "LinkButton2")
    cookie_close_btn.click()
    time.sleep(10)
    modal_close_btn = driver.find_element(By.XPATH, "//div[@class='btn-close']")
    modal_close_btn.click()
    soccer_sidebar = driver.find_element(By.ID, "mhs-1")

    # Get last menu item for expand and click
    soccer_menu = soccer_sidebar.find_element(By.XPATH, "a")
    soccer_menu.click()
    sport_list = soccer_sidebar.find_elements(By.XPATH, "ul/li")
    time.sleep(2)
    for i in range(len(sport_list)):
        item = sport_list[i]
        fetch_data(item)
    # driver.quit()
    # driver.close()

if __name__ == "__main__":
    main()