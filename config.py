import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
    OPEN_WEATHER_ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"

    fred_series_url = "https://api.stlouisfed.org/fred/series"
