import os
import zoneinfo
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask_assets import Environment, Bundle
from ratings import indScraper, dunksScraper, bbrScraper, ratingsCalculator, driver, get_ratings


app = Flask(__name__, static_url_path='/static') 
# app.config.from_object(Config())

my_timezone = zoneinfo.ZoneInfo("America/Chicago")
scheduler = BackgroundScheduler(timezone=my_timezone)


# Function to scrape and calculate ratings
def scrape_and_calculate_ratings():
    # Scrape the ratings from each website
    dunks_dict = get_ratings(dunksScraper, 'scrape_dddratings')
    ind_dict = get_ratings(indScraper, 'scrape_indratings')
    bbr_dict = get_ratings(bbrScraper, 'scrape_bbratings')

    # Calculate the ratings
    calculator = ratingsCalculator(bbr_dict, dunks_dict, ind_dict)
    calculator.calculate_and_sort_ratings()
    ratings = calculator.get_sorted_ratings()

    # Store the ratings in the app config
    app.config['RATINGS'] = ratings

# Run function once at startup then schedule it to run once a day at the specified time
scrape_and_calculate_ratings()
scheduler.add_job(scrape_and_calculate_ratings, 'cron', hour=9, minute=0)
scheduler.start()

@app.route('/', methods=['GET'])
def show_ratings():
    # Retrieve the stored ratings
    ratings = app.config.get('RATINGS', [])
    return render_template('index.html', ratings=ratings)

