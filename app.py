from flask import Flask, render_template, request
import json, requests as rqst
import development.config # contains api keys
from pprint import pprint
#urllib.request to make a requst to api
#import urllib.request
#import json to load JSON data to a python dictionary



app = Flask(__name__)
@app.route('/', methods =['POST','GET'])
def weather():
    api = development.config.openweatherapi
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'Atlanta' #default city

    r = rqst.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}')

    list_of_data = r.json()
    lat = list_of_data['coord']['lon'] #gets longitude from inputed city
    lon = list_of_data['coord']['lat']#gets latitude from inputed city
    more_weather_data = rqst.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api}') #pulls data from openweathermap.org's one call api
    detail_weather_data = more_weather_data.json()
    data = {
        "weather_description": str(detail_weather_data['current']['weather'][0]['description']), 
        "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                    + str(list_of_data['coord']['lat']), 
        "temp": str(detail_weather_data['current']['temp']), #Converting to Farenheight
        "feel": str(detail_weather_data['current']['feels_like']), #Converting to Farenheight
        "mintemp": str(detail_weather_data['daily'][0]['temp']['min']), 
        "maxtemp": str(detail_weather_data['daily'][0]['temp']['max']), 
    } 
    pprint(detail_weather_data['current']['weather'])
    return render_template('index.html', data=data)

    if __name__ == '__main__':
        app.run(debug = True)

