from flask import Flask, request, render_template
import requests

app = Flask(__name__)

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
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            response = get_pokemon_info(name)
            if response:
                return render_template('pokemon.html', pokemon=response)
            else:
                return render_template('pokemon.html', error="Pokemon not found")
        else:
            return render_template('pokemon.html', error="Please provide a Pokemon name")
    else:
        return render_template('pokemon.html')