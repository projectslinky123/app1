import base64
import io
import json
import math
import os
import time
import re
from datetime import datetime
from app.fns.scraperfns import cleanupdata, getpagedata, getdf, getspan
from app.fns.graphfns import create_figure
from app.fns.otherfns import textanalysis
from app.forms import InputText, InputTicker
import pandas as pd
import matplotlib.pyplot as plt
import requests
from app import app
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from bs4 import BeautifulSoup


@app.route('/')
@app.route('/index')
def index():
    pkgs = [
        {'name': 'beautifulsoup4',
         'use': 'Data extraction',
         'description': 'Beautiful Soup is a Python library for pulling data out of HTML and XML files',
         'website': 'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'},
        {'name': 'flask',
         'use': 'Base Framework',
         'description': 'Base Framework'},
        {'name': 'flask-Bootstrap',
         'use': 'For a cleaner and better looking front-end',
         'description': 'For a cleaner and better looking front-end'},
        {'name': 'pandas',
         'use': 'data transformation',
         'description': 'pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.',
         'website': 'https://pandas.pydata.org/'},
        {'name': 'jinja2',
         'use': 'Managing the front end pages using templates',
         'description': 'Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.'},
        {'name': 'matplotlib',
         'use': 'Generating graphs',
         'description': 'Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python'},
        {'name': 'python-dotenv',
         'use': 'Loading environment variables from a file',
         'description': 'Reads the key-value pairs from a .env file and adds them as environment variables'},
        {'name': 'requests',
         'use': 'Sending HTTP/1.1 requests',
         'description': 'Sending HTTP/1.1 requests'},
        {'name': 'selenium webdriver',
         'use': 'Scrapping page data',
         'description': 'Selenium WebDriver drives a browser natively, as a real user would, either locally or on remote machines.It is most used for automated testing and automated scrapping of data of web pages'}
    ]
    return render_template('index.html', title='Home', pkgs=pkgs)


@app.route('/contactme')
def contactme():
    return render_template('contactme.html')


@app.route('/weather')
def weather():
    api_key = app.config['OPEN_WEATHER_API_KEY']
    api_url = app.config['OPEN_WEATHER_ONECALL_URL']
    lat = "43.073051"
    lon = "-89.401230"
    url = api_url+"?lat="+lat+"&lon="+lon+"&units=imperial&appid=" + api_key
    response = requests.get(url)
    data = json.loads(response.text)

    for v in data["hourly"]:
        v["hr"] = time.strftime("%I %p", time.localtime(v["dt"]))

    return render_template('weather.html', title='Weather', all=data["hourly"], projectdesc="Data retreived from https://api.openweathermap.org")


@app.route('/graph')
def graph():
    title, data, xaxisLabel, yaxisLabel, xlist, ylist = getgraphdata("A939RC0A052NBEA")
    fig = create_figure("year", yaxisLabel, xlist, ylist)
    return render_template('testgraph.html', title=title, data=data["observations"]
                           , val=data, fig=fig, projectdesc="Data retreived from https://api.stlouisfed.org/fred. The graph is built using the matplotlib package")

@app.route('/scrapertest')
def scrapertest():
    url = "https://www.nasdaq.com/market-activity/stocks/fun/latest-real-time-trades"
    html = getpagedata(url)
    soup = BeautifulSoup(html, "html.parser")
    tabledata = soup.find('table', {'class': 'latest-real-time-trades__table'})

    return render_template('test.html', title="Data scrapped from wikipedia"
                           , url=url, data=tabledata)


@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    url = "https://www.nasdaq.com/market-activity/stocks/{{ticker}}/latest-real-time-trades"
    form = InputTicker()
    txt = form.ticker.data
    stockName = ""
    if txt is None or len(txt) == 0:
        df = {"Text is an empty string"}
    else:
        txt = txt.replace("\r\n", "\n")
        txt = re.sub('[^A-Za-z0-9]+', '', txt)
        url = url.replace("{{ticker}}", txt)

        html = getpagedata(url)
        if html is None or len(html) == 0:
            df = pd.DataFrame(["Ticker is invalid or data on the ticket cannot be found"], columns=['Error'])  # {"Ticker is invalid or data on the ticket cannot be found"}
        else:
            dataproperty = {'class': 'symbol-page-header__name'}
            stockName = getspan(html, dataproperty)
            tableproperty = {'class': 'latest-real-time-trades__table'}
            df = getdf(html, tableproperty)
            df.columns = df.columns.to_series().apply(cleanupdata)
            df = df.applymap(cleanupdata)

    res = isinstance(df, pd.DataFrame)
    return render_template('scraper.html', title="Data scrapped from Nasdaq"
                           , url=url, results=res, stockName=stockName, data=df
                           , projectdesc="<p>The Seleium webdriver along with a headless chrome browser is used to download the page data</P><p>Beautifulsoup is then used to extract the real time trades table from the downloaded HTML data.</p><p>Pandas is then used for data transformations before the results are displayed on the page.</p><p>'NLS' in the results stands for Nasdaq Last Sale</p>"
                           , form=form)


@app.route('/txtanalysis', methods=['GET', 'POST'])
def txtanalysis():
    form = InputText()
    txt = form.inputtext.data
    if txt is None or len(txt) == 0:
        data = {"Text is an empty string"}
        dataprefix = None
    else:
        txt = txt.replace("\r\n", "\n")
        data = textanalysis(txt)
        dataprefix = "Number of"
    return render_template('txtanalysis.html', title="Text Analysis Report", dataprefix=dataprefix
                           , data=data, form=form)


@app.route('/aboutproject')
def aboutproject():
    projectdata = [
        {'num': '1'
            , 'name': 'Weather'
            , 'description': 'CCDS'
            , 'data from': app.config['OPEN_WEATHER_ONECALL_URL']
            , 'techused': ['SQL', 'DBAmp']
         },
        {'num': '2'
            , 'name': 'Weather'
            , 'subtitle': 'SWF'
            , 'body': 'Test post #2'
            , 'from': '2012'
            , 'to': '2014'
         }
    ]
    return render_template('aboutproject.html', projectdata=projectdata)


@app.route('/aboutme')
def aboutme():
    user = {'fname': ''
            , 'lname': ''}
    workexp = [
        {'postnum': '1'
            , 'title': 'Systems Analyst'
            , 'subtitle': 'CCDS'
            , 'body': 'Test post #1'
            , 'from': '2014'
            , 'techused': ['SQL', 'DBAmp']
         },
        {'postnum': '2'
            , 'title': 'Financial Analyst'
            , 'subtitle': 'SWF'
            , 'body': 'Test post #2'
            , 'from': '2012'
            , 'to': '2014'
         }
    ]
    education = [
        {'num': '1'
            , 'title': 'Weatherhead School of Management at Case Western Reserve University'
            , 'subtitle': 'Master of Science in Management, Finance'
            , 'body': 'Test post #1'
            , 'from': '2008'
            , 'to': '2009'
         },
        {'num': '2'
            , 'title': 'Birla Institute of Technology and Science, Pilani'
            , 'subtitle': 'Bachelor of Engineering, Computer Science'
            , 'body': 'Test post #1'
            , 'from': '2004'
            , 'to': '2008'
         }
    ]
    return render_template('myresume.html', title='About me', user=user, workexp=workexp, education=education)


def getgraphdata(seriesId):
    desc_request_url = app.config['FRED_SERIES_URL']
    request_url = app.config['FRED_SERIES_DATA_URL']
    payload = {"api_key": os.environ.get('fred_apikey'),
               "series_id": seriesId,
               "file_type": "json"}
    response1 = requests.get(desc_request_url, params=payload)
    data1 = response1.json()
    response = requests.get(request_url, params=payload)
    data = response.json()
    xlist = []
    ylist = []
    for k in range(len(data["observations"])):
        xlist.append(data["observations"][k]["date"])
        ylist.append(math.floor(float(data["observations"][k]["value"])))

    return data1["seriess"][0]["title"], data, "year", data1["seriess"][0]["units"], xlist, ylist
