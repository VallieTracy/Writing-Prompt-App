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
    """When user clicks hyperlink to register"""
    
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


@app.route('/start', methods=['POST'])
def log_in():
    """Defines what happens when the user logs in"""
    
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')
  
    else:
        session['used_words'] = []
        writing_dictionary = writing_functions.get_random_dictionary()
        session["writing_dictionary"] = writing_dictionary 
        session["user_email"] = user.email
        session["first_name"] = user.first_name

        used_dicts = [writing_dictionary]
        session['used_dicts'] = used_dicts

        writing_directions = writing_dictionary['directions']
        prompt_name = writing_dictionary['name']
        
        
        img_src = writing_dictionary['img_path']    
        first_name = user.first_name        
        welcome = f"Welcome back {first_name}!"

        return render_template('writing_directions.html', writing_directions=writing_directions, prompt_name=prompt_name, welcome_message=welcome, img_src=img_src)

   
@app.route('/writing-prompt')
def writing_prompt():
    """Gets the associated values from the random writing dictionary to display on the web page"""

    writing_dictionary = session["writing_dictionary"]
    directions = writing_dictionary['directions']
    directive_name = writing_dictionary['name']
    the_prompt = writing_dictionary['prompt']
    word_qty = writing_dictionary['random_word_qty']
    time = writing_dictionary['time_given']
    loops = writing_dictionary['loops']


    random_word1 = crud.get_unique_word(session['used_words'])
    session['used_words'].append(random_word1)
    session.modified=True
    
    random_word2 = crud.get_unique_word(session['used_words'])
    session['used_words'].append(random_word2)
    session.modified=True

    first_name = session["first_name"]
    message = f"{first_name}, the timer has been started. You will have {time} for this exercise."
    message2 = f"Each time the bell chimes, the timer will reset and you'll write with the new word. You will do this {loops + 1} times."
    
    return render_template('writing_prompt.html', message=message, 
    word1=random_word1, word2=random_word2, message2=message2, loops=loops,
    name=directive_name, prompt=the_prompt, word_qty=word_qty)


@app.route('/store-nugget', methods=['POST'])
def store_nugget():
    """When button is clicked, if characters are entered into the form, it will be stored in DB. Otherwise not.
    Flash message displayed in both cases on web browser"""

    nugget = request.form.get('nugget')
    email = session["user_email"]
    if nugget != '':
        crud.create_nugget(nugget, email)
        flash('Your nugget was successfully stored!')  
        print('FLASH MESSAGE STORED!') 
    else:
        flash('No nuggets added.')
        print('FLASH MESSAGE NONE ADDED')
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    
    writer = session["first_name"]
    email = session["user_email"]
    nuggets = crud.get_nuggets_by_email(email)

    prompts = writing_functions.get_all_long_prompts()

    return render_template('homepage.html', writer=writer, prompts=prompts)

@app.route('/homepage.json')
def nugget_info():
    email = session["user_email"]
    nuggets = crud.get_nuggets_by_email(email)
    return jsonify(nuggets)

@app.route('/data/prompts.json')
def prompts_json():
    """Returns the random dictionary in json format"""
    
    writing_dictionary = session["writing_dictionary"]
    return jsonify(writing_dictionary)
    

@app.route('/random-words.json')
def get_words():
    # if session[used_words] contains all the words, then empty out session[used_words]
    # if length of session[used words] is euqal to (count query to get length of words table), then empty the session
    total_word_count = crud.count_table()
    if len(session['used_words']) >= (total_word_count - 4):
        session['used_words'] = []
        random_word1 = crud.get_unique_word(session['used_words'])
        session['used_words'].append(random_word1)
        session.modified=True
    
        random_word2 = crud.get_unique_word(session['used_words'])
        session['used_words'].append(random_word2)
        session.modified=True
    else:
        random_word1 = crud.get_unique_word(session['used_words'])
        session['used_words'].append(random_word1)
        session.modified=True
    
        random_word2 = crud.get_unique_word(session['used_words'])
        session['used_words'].append(random_word2)
        session.modified=True
    print('-------------------------------------------')
    print(f"length of session used words - {len(session['used_words'])}")
    return jsonify(random_word1, random_word2)

@app.route('/add-word', methods=['POST'])
def api_word_add():
    email = session["user_email"]
    word = (request.form.get('word')).lower()
    print(f"WORD is '{word}'!")
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

@app.route('/new-prompt')  
def new_directive():
    """If user chooses to write again, a new random dictionary is picked and new session created
    Then follows the same process of directions to the prompt itself and back to homepage"""
    
    writing_dictionary = writing_functions.get_random_dictionary()

    while writing_dictionary in session['used_dicts']:
        if len(session['used_dicts']) < 5:
            writing_dictionary = writing_functions.get_random_dictionary()
        else:
            session['used_dicts'] = []

    session['used_dicts'].append(writing_dictionary)

    session["writing_dictionary"] = writing_dictionary
    writing_directions = writing_dictionary['directions']
    prompt_name = writing_dictionary['name']
    img_src = writing_dictionary['img_path'] 
    
    writer = session["first_name"]
    email = session["user_email"]

    welcome = f"Here's a new writing directive for you {writer}..."
    return render_template('writing_directions.html', writing_directions=writing_directions, prompt_name=prompt_name, welcome_message=welcome, img_src=img_src) 



@app.route('/longer-prompt', methods=['GET'])
def longer_prompt():
    
    prompt_id = request.args.get('prompt-select') 
    dict_id = int(prompt_id)

    writing_dictionary = writing_functions.get_longer_prompt(dict_id)
    prompt_name = writing_dictionary['name'] 
    writing_directions = writing_dictionary['directions'] 
    bold_uppercase = writing_dictionary['bold-uppercase'] 
    bold = writing_dictionary['bold'] 
    text_indent = writing_dictionary['text-indent']
    underline = writing_dictionary['underline']
    text_indent_bold = writing_dictionary['text_indent_bold']
    
    
    return render_template('longer_writing.html', name=prompt_name, writing_directions=writing_directions, id=prompt_id, 
                            bold_uppercase=bold_uppercase, bold=bold, text_indent=text_indent, underline=underline, text_indent_bold=text_indent_bold)

@app.route('/logout')
def delete_sessions():
    """Deletes the user's sessions"""
    
    sessions = ['writing_dictionary', 'user_email', 'first_name', 'used_words']
    for item in sessions:
        session.pop(item, None)
    # flash("You've been signed out.")
    # return redirect('/')
    return render_template('goodbye.html')

@app.route('/sound')
def sound():

    return render_template('sound.html')

@app.route('/sound-path')
def path():
    sound_path = 'Correct Answer.mp3'
    return sound_path

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
