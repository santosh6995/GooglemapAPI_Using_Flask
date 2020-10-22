
import requests
from bs4 import BeautifulSoup
from bs2json import bs2json
from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    return render_template('home_url.html')


@app.route('/', methods=['POST'])
def post_url():
    url = request.form['url']
#    url = 'http://neocando.case.edu/cando/housingReport/lbxml.jsp?parcel=673-12-062'
    document = requests.get(url)

    #Extracting XML data from url
    soup= BeautifulSoup(document.content,"lxml-xml")
    converter = bs2json() #converting Beautifulsoup to Dictionary 

    tag = soup.find('lbstream')
    jsons = converter.convert(tag)
#    return  jsonify(jsons) # Returns the json data output
   
    
    parcel = {}
    parcel['id'] = jsons['lbstream']['parcelid']['id']['text']
    parcel['latitude'] = float(soup.find('LATITUDE').value.text)
    parcel['longitude'] = float(soup.find('LONGITUDE').value.text)
   
    parcel['st'] = str(soup.find('number').value.text)+ ' ' + str(soup.find('street').value.text) + ',' + ' '+ str(soup.find('mcdnme').value.text) + ',' + ' ' + str(soup.find('neighbor').value.text)+ ' ' + '-' +' '+ str(soup.find('zip').value.text)
    parcel['filename'] = str(parcel['id'])+'_main_pic.JPG'
    
    return render_template('home.html', parcel= parcel)

if __name__ == "__main__":
    app.run(debug=True)