import base64
import io
import json
import os
import time
import math

import requests
from app import app
from flask import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


@app.route('/')
@app.route('/index')
def index():
    pkgs = [
        {'name': 'flask',
         'use': 'Base Framework',
         'description': 'Base Framework'},
        {'name': 'flask-Bootstrap',
         'use': 'For a cleaner and better looking front-end',
         'description': 'For a cleaner and better looking front-end'},
        {'name': 'Jinja2',
         'use': 'Managing the front end pages using templates',
         'description': 'Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.'},
        {'name': 'matplotlib',
         'use': 'Generating graphs',
         'description': 'Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python'},
        {'name': 'python-dotenv',
         'use': 'Loading environment variables from a file',
         'description': 'Reads the key-value pair from .env file and adds them as environment variables'},
        {'name': 'requests',
         'use': 'for sending HTTP/1.1 requests',
         'description': 'Sending HTTP/1.1 requests'}
    ]
    return render_template('index.html', title='Home', pkgs=pkgs)


@app.route('/weather')
def weather():
    api_key = app.config['OPEN_WEATHER_API_KEY']
    api_url = app.config['OPEN_WEATHER_ONECALL_URL']
    lat = "43.073051"
    lon = "-89.401230"
    url = api_url+"?lat="+lat+"&lon="+lon+"&units=imperial&appid=" + api_key
    response = requests.get(url)
    data = json.loads(response.text)
    hrstart = int(time.strftime("%H", time.localtime(data["hourly"][0]["dt"])))
    return render_template('weather.html', title='Weather', all=data["hourly"], offset=data["timezone_offset"], hrstart=hrstart)


@app.route('/graph')
def graph():
    desc_request_url = app.config['FRED_SERIES_URL']
    request_url = app.config['FRED_SERIES_DATA_URL']
    payload = {"api_key": os.environ.get('fred_apikey'),
               "series_id": "W006RC1A027NBEA",
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

    fig = create_figure("year", data1["seriess"][0]["units"], xlist, ylist)
    return render_template('testgraph.html', title=data1["seriess"][0]["title"], data=data["observations"], dt=data1
                           , val=data, fig=fig)


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


def create_figure(xtitle, ytitle, x, y):
    fig = plt.figure(figsize=(15, 5))
    axis = fig.add_subplot(1, 1, 1)
    axis.set_xlabel(xtitle)
    axis.set_ylabel(ytitle)
    axis.grid()
    axis.plot(list(map(int, y)))
    xlabels = [""]
    xticks = [0]
    spacing = len(x)//10
    for i in range(11):
        xticks.append(spacing*i)
        xlabels.append(x[spacing*i])

    axis.set_xticks(xticks)
    axis.set_xticklabels(xlabels, rotation=70)
    fig.tight_layout()

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String
