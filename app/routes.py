from flask import render_template, request
import requests
from app import app
from app.forms import NameForm, LoginForm, SignUpForm

@app.route('/')
def index():
    return render_template('/index.html')

def get_pokemon_info(name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')
    if response.ok:
        data = response.json()
        poke_info = {
            'Name': data['name'].title(),
            'HP': data['stats'][0]['base_stat'],
            'Defense': data['stats'][3]['base_stat'],
            'Attack': data['stats'][4]['base_stat'],
            'Ability': data['abilities'][0]['ability']['name'].title(),
            'Base XP': data['base_experience'],
            'Sprite URL': data['sprites']['front_default'],
            'shinySprite URL': data['sprites']['front_shiny']
        }
        return poke_info

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon_info():
    form = NameForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name')
        if name:
            response = get_pokemon_info(name)
            if response:
                return render_template('pokemon.html', pokemon=response, form=form)
            else:
                return render_template('pokemon.html', error="Pokemon not found", form=form)
        else:
            return render_template('pokemon.html', error="Please provide a Pokemon name", form=form)
    else:
        return render_template('pokemon.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return f'{email} {password}'
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm() 
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        return f'{username} {email} {password}'
    else:
        return render_template('signup.html', form=form)