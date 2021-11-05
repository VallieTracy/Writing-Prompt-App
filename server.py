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
    """Show landing page."""

    return render_template('log-in.html')

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

@app.route('/log-in', methods=['POST'])
def log_in():
    
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')
  
    else:
        writing_dictionary = writing_functions.get_random_dictionary()
        prompt_name = writing_dictionary['name']
        writing_directions = writing_dictionary['directions']
        prompt = writing_dictionary['prompt']
        random_word_qty = writing_dictionary['random_word_qty']
        
        session["prompt_name"] = prompt_name
        session["prompt"] = prompt
        session["random_word_qty"] = random_word_qty
        session["user_email"] = user.email
        welcome = f"Welcome back {user.first_name}!"
        return render_template('writing_directions.html', welcome_message=welcome, writing_directions=writing_directions,name=prompt_name)
        


# Route that directs to writing_prompt.html
@app.route('/writing-prompt')
def writing_prompt():

    random_word1 = crud.get_random_word()
    random_word2 = crud.get_unique_second_word()
    prompt_name = session["prompt_name"]
    the_prompt = session["prompt"]
    word_qty = session["random_word_qty"]
    return render_template('writing_prompt.html', word1=random_word1, word2=random_word2, name=prompt_name, prompt=the_prompt, word_qty=word_qty)

# Route that will store a user's nugget of writing
@app.route('/store-nugget', methods=['POST'])
def store_nugget():

    nugget = request.form.get('nugget')
    email = session["user_email"]
    if nugget != '':
        crud.create_nugget(nugget, email)
        flash('Your nugget was successfully stored!')
        
    else:
        flash('No nuggets added.')
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

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