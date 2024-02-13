from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from .forms import NameForm

@app.route('/')
def index():
    return render_template('home.html')

def get_pokemon_info(name):
    if name.isdigit():
        name = str(int(name))
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
            'Shiny Sprite URL': data['sprites']['front_shiny'],
            'ID': data['id']
        }
        return poke_info

@app.route('/pokeapp', methods=['GET', 'POST'])
def pokemon_info():
    form = NameForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get('name')
        if name:
            response = get_pokemon_info(name)
            if response:
                return render_template('pokeapp.html', pokemon=response, form=form)
            else:
                return render_template('pokeapp.html', error="Pokemon not found", form=form)
        else:
            return render_template('pokeapp.html', error="Please provide a Pokemon name", form=form)
    else:
        return render_template('pokeapp.html', form=form)