from flask import (Flask, render_template, request, session, flash, redirect)
from model import connect_to_db
from pprint import pformat
import os
import requests
import crud
from jinja2 import StrictUndefined
import writing_functions

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
    random_word = crud.get_random_word()

    writing_dictionary = writing_functions.get_random_dictionary()
    prompt_name = writing_dictionary['name']
    writing_directions = writing_dictionary['directions']


    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')

    # So far, the else statement is just redirecting to a new html page and displaying the welcome message.  For testing purposes only!    
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        welcome = f"Welcome back {user.first_name}!"
        return render_template('writing_directions.html', welcome_message=welcome, word=random_word, writing_directions=writing_directions,name=prompt_name)
        
@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/register-user', methods=['POST'])
def register_user():
    """Process user registration"""
    
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('An account with that email already exists.')
        return redirect('/register')
    else:
        crud.create_user(email, first_name, last_name, password)
        flash('Account created.  Please log-in.')
        return redirect('/')


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