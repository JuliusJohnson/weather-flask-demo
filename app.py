from flask import Flask, render_template, redirect, request, send_from_directory,url_for
import json, os, requests as rqst
import development.config # contains api keys
from pprint import pprint
import pandas as pd
#urllib.request to make a requst to api
#import urllib.request
#import json to load JSON data to a python dictionary

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

app.config['DOWNLOAD_FOLDER'] = DOWNNLOAD_FOLDER

@app.route('/', methods =['POST','GET'])
def weather():
    api = development.config.openweatherapi
    if request.method == 'POST':
        city = request.form['city']
        state = request.form['state']
    else:
        city = 'Atlanta' #default city
        state = 'Georgia' #default state

    r = rqst.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api}')

    list_of_data = r.json()
    #print(list_of_data)
    lon = list_of_data['coord']['lon'] #gets longitude from inputed city
    lat = list_of_data['coord']['lat']#gets latitude from inputed city
    more_weather_data = rqst.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api}') #pulls data from openweathermap.org's one call api
    detail_weather_data = more_weather_data.json()
    
    data = {
        "city": str(city),
        "weather_description": str(detail_weather_data['current']['weather'][0]), 
        "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                    + str(list_of_data['coord']['lat']),
        "w_icon": str("http://openweathermap.org/img/wn/" + str(detail_weather_data['current']['weather'][0]['icon']) + ".png") ,
        "temp": str(detail_weather_data['current']['temp']), #Converting to Farenheight
        "feel": str(detail_weather_data['current']['feels_like']), #Converting to Farenheight
        "mintemp": str(detail_weather_data['daily'][0]['temp']['min']), 
        "maxtemp": str(detail_weather_data['daily'][0]['temp']['max']), 
    } 
    pprint(detail_weather_data['current'])

    df = pd.DataFrame.from_dict(detail_weather_data, orient="index")
    filename = f"{city}_data.csv"
    df.to_csv(f"uploads/{filename}")
   
    return render_template('index.html', data=data) #, redirect(url_for('uploaded_file', filename=filename))
    
    if __name__ == '__main__':
        app.run(debug = True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

    app.run(debug=True)

    #todo:
    #add download csv button
    #add error handling if a invalid city is chosen