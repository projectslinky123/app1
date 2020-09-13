from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Suraj'}
    return render_template('index.html', title='Home', user=user)

@app.route('/weather')
def weather():
    user = {'username': 'Suraj'}
    return render_template('weather.html', title='Weather', user=user)

@app.route('/aboutme')
def aboutme():
    user = {'fname': 'Suraj'
            , 'lname': 'Ramesh'}
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