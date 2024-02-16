from . import main
from flask import request, render_template, redirect, flash, url_for
import requests
# from app import app
from app.models import User, Pokemon, UserPokemon, db
from .forms import NameForm
from flask_login import current_user

@main.route('/')
def index():
    return redirect(url_for('main.pokemon_info'))

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

@main.route('/pokeapp', methods=['GET', 'POST'])
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

# from flask import request, flash, redirect, url_for

@main.route('/catch', methods=['POST'])
def catch_pokemon():
    username = request.form.get('username')
    pokemon_name = request.form.get('pokemon_name')

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))  # Assuming you have an index route

    # Check if the Pokémon exists or add it to the database
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    if not pokemon:
        # If the Pokémon doesn't exist, create a new entry for it
        pokemon_info = get_pokemon_info(pokemon_name)  # Assuming you have a function to get Pokémon info
        if not pokemon_info:
            flash('Failed to retrieve Pokémon info', 'error')
            return redirect(url_for('index'))  # Redirect to the index route with an error message

        # Create a new Pokémon entry
        pokemon = Pokemon(
            name=pokemon_info['Name'],
            base_hp=pokemon_info['HP'],
            base_atk=pokemon_info['Attack'],
            base_def=pokemon_info['Defense'],
            image=pokemon_info['Sprite URL']
        )
        pokemon.save()
        flash(f'{pokemon_name} added to Pokédex', 'success')  # Flash success message for adding Pokémon

    # Check if the user has already caught the maximum number of Pokémon
    if len(user.pokemon_caught) >= 6:
        flash('You already have 6 Pokémon! Release one before catching another.', 'warning')
        return redirect(url_for('main.pokemon_info'))  # Redirect to the index route with a warning message

    # Check if the user already caught the Pokémon
    if UserPokemon.query.filter_by(user_id=user.id, pokemon_name=pokemon_name).first():
        flash('You already caught this Pokemon', 'warning')
        return redirect(url_for('main.pokemon_info'))  # Redirect to the index route with a warning message

    # Create a new UserPokemon instance
    user_pokemon = UserPokemon(user_id=user.id, pokemon_name=pokemon_name)
    user_pokemon.save()
    flash(f'You caught {pokemon_name}!', 'success')  # Flash success message for catching Pokémon

    return redirect(url_for('main.pokemon_info'))  # Redirect to the index route

@main.route('/release/<pokemon_id>', methods=['POST'])
def release_pokemon(pokemon_id):
    # Assuming you have a function to get the current user
    user = current_user
    # Assuming you have a function to get the user's caught Pokémon
    pokemon = UserPokemon.query.filter_by(user_id=user.id, id=pokemon_id).first()
    if not pokemon:
        flash('Pokemon not found', 'error')
        return redirect(url_for('my_pokemon'))  # Redirect to the My Pokémon page
    db.session.delete(pokemon)
    db.session.commit()
    flash('Pokemon released successfully', 'success')
    return redirect(url_for('main.my_pokemon'))  # Redirect to the My Pokémon page

@main.route('/mypokemon')
def my_pokemon():
    user = current_user
    caught_pokemon = UserPokemon.query.filter_by(user_id=user.id).all()

    return render_template('mypokemon.html', caught_pokemon=caught_pokemon)

@main.route('/search', methods=['GET', 'POST'])
def search_users():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('search.html', users=users)

@main.route('/battle/<int:opponent_id>', methods=['GET'])
def battle(opponent_id):
    opponent = User.query.get(opponent_id)

    if opponent:
        # Perform battle logic here
        # For simplicity, let's assume the challenger always wins
        flash(f"You are battling {opponent.username}!", 'info')
        return redirect(url_for('main.index'))  # Redirect to homepage after battle
    else:
        flash("Opponent not found", 'error')
        return redirect(url_for('main.search_users'))  # Redirect to search page if opponent not found
    
@main.route('/matchup/<int:opponent_id>')
def matchup(opponent_id):
    current_user_team = current_user.pokemon_team
    opponent = User.query.get(opponent_id)
    if opponent:
        opponent_team = opponent.pokemon_team  # Retrieve the opponent's Pokémon team
        return render_template('matchup.html', current_user_team=current_user_team, opponent_team=opponent_team, opponent=opponent)
    else:
        flash("Opponent not found", 'error')
        return redirect(url_for('main.search_users'))  # Redirect to search page if opponent not found
