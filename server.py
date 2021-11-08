from flask import (Flask, render_template, request, session, flash, redirect, jsonify)
from model import connect_to_db
from pprint import pformat
import os
import requests
import crud
from jinja2 import StrictUndefined
import writing_functions
import data.prompts as dp

app = Flask(__name__)
app.secret_key = 'cookiescookiescookiesyumyumyummy'

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
        """get random writing dict and store in session"""
        writing_dictionary = writing_functions.get_random_dictionary()
        session["writing_dictionary"] = writing_dictionary 

        """store user object in session"""
        session["user_email"] = user.email
        session["first_name"] = user.first_name

        """Variables for writing_directions.html"""
        writing_directions = writing_dictionary['directions']
        prompt_name = writing_dictionary['name']
        
        first_name = user.first_name        
        welcome = f"Welcome back {first_name}!"

        return render_template('writing_directions.html', writing_directions=writing_directions, prompt_name=prompt_name, welcome_message=welcome)

@app.route('/new-prompt')  
def new_directive():
    writing_dictionary = writing_functions.get_random_dictionary()
    session["writing_dictionary"] = writing_dictionary
    

    welcome = f"Here's a new writing directive for you {user.first_name}..."
    render_template('writing_directions.html', welcome_message=welcome, writing_directions=writing_directions,name=prompt_name)    


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
    
    writer = session["first_name"]
    email = session("user_email")
    # email = session["user"].email
    nuggets = crud.get_nuggets_by_email(email)

    return render_template('homepage.html', writer=writer)

@app.route('/homepage.json')
def nugget_info():
    email = session["user_email"]
    nuggets = crud.get_nuggets_by_email(email)
    return jsonify(nuggets)

@app.route('/data/prompts.json')
def prompts_json():
    return jsonify(dp.prompts_dicts)

# @app.route('/api-call')
# def api_call():
#     """Testing working with Merriam's Dictionary API"""

#     base_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
#     word = 'voluminous'
#     url = base_url + word
#     payload = {'key': API_KEY}

#     response = requests.get(url, params=payload)

#     data = response.json()
#     data_id = data[0]['meta']['stems']
#     # events = data['_embedded']['events']

#     return render_template('search.html',
#                            pformat=pformat,
#                            data_id=data_id)

@app.route('/add-word', methods=['POST'])
def api_word_add():
    email = session["user_email"]
    word = (request.form.get('word')).lower()
    base_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
    url = base_url + word
    payload = {'key': API_KEY}
    response = requests.get(url, params=payload)
    data = response.json()

    try:
        stems = data[0]['meta']['stems']
        flash(f"Huzzah! We've located {word} in the Merriam-Webster Dictionary!")
        if word in crud.get_all_words():
            flash("BUT it's already in the DB so it's not being added.")
            flash(stems)
        else:
            flash("AND it's not in the DB so we've added it for you!")
            crud.create_word(word, email)

    except:
        flash(f"{word} is not in the Merriam-Webster Dictionary.")
    return redirect('/homepage')

@app.route('/homepage-words.json')
def word_info():
    email = session["user_email"]
    words = crud.get_words_by_email(email)
    return jsonify(words)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)









# # *****************************************************************************************
# # VERSION 2.0
# # API Call to Merriam Webster
# # In order to run, need to write 'source secrets.sh' into terminal first!
# @app.route('/api-call')
# def api_call():
#     """Testing working with Merriam's Dictionary API"""

#     # keyword = request.args.get('keyword', '')
#     # postalcode = request.args.get('zipcode', '')
#     # radius = request.args.get('radius', '')
#     # unit = request.args.get('unit', '')
#     # sort = request.args.get('sort', '')

#     base_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'
#     word = 'voluminous'
#     url = base_url + word
#     payload = {'key': API_KEY}

#     response = requests.get(url, params=payload)

#     data = response.json()
#     data_id = data[0]['meta']['stems']
#     # events = data['_embedded']['events']

#     return render_template('search.html',
#                            pformat=pformat,
#                            data_id=data_id)
# # *****************************************************************************************





# # if __name__ == '__main__':
# #     app.debug = True
# #     app.run(host='0.0.0.0')