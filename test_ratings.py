import unittest
from selenium import webdriver
from ratings import indScraper, bbrScraper, dunksScraper, ratingsCalculator, get_ratings

class TestRatings(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()

    def test_indScraper(self):
        scraper = indScraper(self.driver)
        ratings = scraper.scrape_indratings()
        self.assertIsInstance(ratings, dict)
        self.assertGreater(len(ratings), 0)

    def test_bbrScraper(self):
        scraper = bbrScraper(self.driver)
        ratings = scraper.scrape_bbratings()
        self.assertIsInstance(ratings, dict)
        self.assertGreater(len(ratings), 0)

    def test_dunksScraper(self):
        scraper = dunksScraper(self.driver)
        ratings = scraper.scrape_dddratings()
        self.assertIsInstance(ratings, dict)
        self.assertGreater(len(ratings), 0)

    def test_ratingsCalculator(self):
        bbr_dict = {'Team A': 5.0, 'Team B': 4.0}
        dunks_dict = {'Team A': 3.0, 'Team B': 2.0}
        ind_dict = {'Team A': 2.0, 'Team B': 1.0}
        calculator = ratingsCalculator(bbr_dict, dunks_dict, ind_dict)
        calculator.calculate_and_sort_ratings()
        sorted_ratings = calculator.get_sorted_ratings()
        self.assertIsInstance(sorted_ratings, dict)
        self.assertGreater(len(sorted_ratings), 0)

    def test_get_ratings(self):
        ratings = get_ratings(indScraper, 'scrape_indratings')
        self.assertIsInstance(ratings, dict)
        self.assertGreater(len(ratings), 0)

if __name__ == '__main__':
    unittest.main()