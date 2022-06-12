from flask import render_template, request, flash, redirect, url_for
import requests
from .import bp as main 
from ..auth.forms import PokemonForm
from flask_login import login_required
from app.models import Pokemon, User



@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        #do poke stuff
        poke = form.pokename.data.lower()
        poke_search = Pokemon.query.filter_by(poke_name=poke).first()
        if not poke_search:

            url = f"https://pokeapi.co/api/v2/pokemon/{poke}"
        
            response = requests.get(url)
            if response.ok:
                poke = response.json()
                poke_dict={
                    "poke_name":poke['name'],
                    "attack_base_stat":poke ["stats"][1]["base_stat"],
                    "hp_base_stat": poke["stats"][0]["base_stat"],
                    "defense_base_stat": poke["stats"][2]["base_stat"],
                    "front_shiny": poke["sprites"]["front_shiny"],
                    "ability_name": poke["abilities"][0]["ability"]["name"],
                    "base_experience": poke["base_experience"],
                }
                poke_search= Pokemon()
                poke_search.from_dict(poke_dict)
                poke_search.save()

                if poke_search in poke_dict:
                    flash("You cannot have more than one of this Pokemon", "danger")

                if len(poke_dict) == 5:
                    flash("You already have 5 pokemon", "danger")
            else:
                flash("This is not a valid Pokemon!", 'danger')
                return redirect(url_for('main.pokemon'))
        
        return render_template('pokemon.html.j2', poke=poke_search, form=form)
        
    return render_template('pokemon.html.j2', form=form)   

@main.route('/my_team', methods=['GET','POST'])
@login_required
def pokemon_team():
    pokemen = User.pokemen.all()
    pokemon_list=pokemen[:5]
    return render_template('my_team.html.j2', pokemen=pokemon_list)



