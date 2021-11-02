from flask import Flask, render_template, request

from pprint import pformat
import os
import requests



app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

API_KEY = os.environ['DICTIONARY_KEY']



@app.route('/')
def index():
    """Show homepage."""

    return render_template('log-in.html')









# *****************************************************************************************
# VERSION 2.0
# API Call to Merriam Webster
# In order to run, need to write 'source secrets.sh' into terminal first!
@app.route('/api-call')
def api_call():
    """Testing working with Merriam's Dictionary API"""

    # keyword = request.args.get('keyword', '')
    # postalcode = request.args.get('zipcode', '')
    # radius = request.args.get('radius', '')
    # unit = request.args.get('unit', '')
    # sort = request.args.get('sort', '')

    base_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
    word = 'voluminous'
    url = base_url + word
    payload = {'key': API_KEY}

    response = requests.get(url, params=payload)

    data = response.json()
    data_id = data[0]['meta']['stems']
    # events = data['_embedded']['events']

    return render_template('search.html',
                           pformat=pformat,
                           data_id=data_id)
# *****************************************************************************************





if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')