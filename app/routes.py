from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from .forms import LoginForm, SignUpForm, NameForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

@app.route('/')
def index():
    return render_template('/index.html')

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
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'Welcome {queried_user.username}!', 'info')
            login_user(queried_user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username email or password', 'warning')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        new_user = User(username, email, password)
        new_user.save()
        flash('Success! Thank you for Signing Up', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))