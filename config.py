import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'htyulotuiupoiyfytjktbnyuty'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')
    # Public Endpoints
    OPEN_WEATHER_ONECALL_URL = "https://api.openweathermap.org/data/2.5/onecall"
    FRED_SERIES_URL = "https://api.stlouisfed.org/fred/series"
    FRED_SERIES_DATA_URL = "https://api.stlouisfed.org/fred/series/observations"
