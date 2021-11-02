from flask import (Flask, render_template, request, session, flash, redirect)
from model import connect_to_db
from pprint import pformat
import os
import requests
import crud
from jinja2 import StrictUndefined




app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

API_KEY = os.environ['DICTIONARY_KEY']



@app.route('/')
def index():
    """Show homepage."""

    return render_template('log-in.html')

@app.route('/log-in', methods=['POST'])
def log_in():
    """Process user log-in"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    # welcome = f"Welcome back {user.first_name}!"
    

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.first_name}!")

    return redirect('/')
    # return render_template('testing.html', welcome_message = welcome)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)









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





# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0')