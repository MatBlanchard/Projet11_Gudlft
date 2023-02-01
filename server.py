import json
from flask import Flask,render_template,request,redirect,flash,url_for


def load_clubs():
    with open('clubs.json') as clubs:
         return json.load(clubs)['clubs']


def load_competitions():
    with open('competitions.json') as comps:
         return json.load(comps)['competitions']

max_bookable_places = 12

def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_object(config)
    competitions = load_competitions()
    clubs = load_clubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/show_summary',methods=['POST'])
    def show_summary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            return render_template('welcome.html', club=club, competitions=competitions)
        except IndexError:
            flash('please enter a valid email')
            return redirect(url_for('index'))


    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        try:
            club = [c for c in clubs if c['name'] == club][0]
            competition = [c for c in competitions if c['name'] == competition][0]
            if club and competition:
                max_places = int(club['points'])
                if max_places > max_bookable_places:
                    max_places = max_bookable_places
                return render_template('booking.html', club=club, competition=competition, max_places=max_places)
        except IndexError:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchase_places',methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
        club['points'] = int(club['points'])-places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app