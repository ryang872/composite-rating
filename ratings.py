import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from teams import nba_teams
import chromedriver_binary


options = webdriver.ChromeOptions()

options.add_argument("--headless=new")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--remote-debugging-pipe')
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)


# For local testing
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



# INPREDICTABLE
class indScraper:
    def __init__(self,driver):
        self.url = "http://stats.inpredictable.com/rankings/nba.php"
        self.driver = driver
        self.ind_dict = {}

    def scrape_indratings(self):
        self.driver.get(self.url)

        # Find the third 'tr' element and the next 29 'tr' elements
        tr_elements = self.driver.find_elements(By.XPATH, '(//tbody/tr)[position() >= 3 and position() <= 32]')

        # Loop through each 'tr' element
        for tr in tr_elements:    
            td_elements = tr.find_elements(By.XPATH, './td')
            
            # Check if the second and fifth 'td' exist
            if len(td_elements) > 4:       
                team_name = td_elements[1].text.strip()
                team_rating = td_elements[4].text.strip()
                team_rating = team_rating.replace('−', '-')        
                team_rating = round(float(team_rating), 1)                  
                self.ind_dict[team_name] = team_rating
        
        return self.ind_dict


# BASKETBALL REFERENCE
class bbrScraper:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.basketball-reference.com/leagues/NBA_2024_ratings.html"
        self.bbr_dict = {}

    def scrape_bbratings(self):
        self.driver.get(self.url)
        tr_elements = self.driver.find_elements(By.XPATH, '//tbody/tr')

        # Loop through each 'tr' element
        for tr in tr_elements:    
            td_elements = tr.find_elements(By.XPATH, './td')
    
            # Check if the first 'td' exists and it has an 'a' element
            if len(td_elements) > 0 and td_elements[0].find_elements(By.XPATH, './a'):       
                link_element = td_elements[0].find_element(By.XPATH, './a')    
                team_name = link_element.text       
                abbreviated_name = nba_teams[team_name]
        
                # Check if the 14th 'td' exists
                if len(td_elements) >= 14:            
                    net_rtg_adj = td_elements[13].text            
                    net_rtg_adj = net_rtg_adj.replace('−', '-')        
                    net_rtg_adj = round(float(net_rtg_adj), 1)               
                    self.bbr_dict[abbreviated_name] = net_rtg_adj

        return self.bbr_dict  


# DUNKS AND THREES
class dunksScraper:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://dunksandthrees.com"
        self.ratings_dict = {}

    def scrape_dddratings(self):
        # Navigate the webdriver to the URL
        self.driver.get(self.url)

        rating_elements = self.driver.find_elements(By.XPATH, '//tr/td[3]/div[@class="wrap svelte-1u8efr8"]/div[1]')
        team_elements = self.driver.find_elements(By.XPATH, '//tr/td[@class="team svelte-pxvppp"]/div/div[@class="team-alias svelte-pxvppp"]')

        for team_element, rating_element in zip(team_elements, rating_elements):
            rating_text = rating_element.text.replace('−', '-')
            rating = round(float(rating_text), 1)
            self.ratings_dict[team_element.text] = rating

        return self.ratings_dict

class ratingsCalculator:
    def __init__(self, bbr_dict, dunks_dict, ind_dict):
        self.bbr_dict = bbr_dict
        self.dunks_dict = dunks_dict
        self.ind_dict = ind_dict
        self.average_ratings = {}
        self.ratings = {}
        self.sorted_ratings = {}

    def calculate_average_ratings(self):
        for team in self.bbr_dict:
            if team in self.dunks_dict and team in self.ind_dict:
                average_rating = (self.bbr_dict[team] + self.dunks_dict[team] + self.ind_dict[team]) / 3
                self.ratings[team] = {
                    'bbr_rating': self.bbr_dict[team],
                    'dunks_rating': self.dunks_dict[team],
                    'ind_rating': self.ind_dict[team],
                    'average_rating': round(average_rating, 1)
                }

    def sort_ratings(self):
        # self.sorted_ratings = {k: v for k, v in sorted(self.ratings.items(), key=lambda item: item[1]['average_rating'], reverse=True)}
        self.sorted_ratings = sorted(self.ratings.items(), key=lambda item: item[1]['average_rating'], reverse=True)
        self.sorted_ratings = dict(self.sorted_ratings)

    def calculate_and_sort_ratings(self):
        self.calculate_average_ratings()
        self.sort_ratings()

    def get_sorted_ratings(self):
        return self.sorted_ratings

# Get the ratings from the scrapers
def get_ratings(scraper_class, scrape_method):
    scraper = scraper_class(driver)
    return getattr(scraper, scrape_method)()
