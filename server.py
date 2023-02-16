from utils import load_competitions, load_clubs, get_future_competitions
from flask import Flask, render_template, request, redirect, flash, url_for

clubs = load_clubs()
competitions = load_competitions()
max_bookable_places = 12
error_default = 'Something went wrong | Please try again'
error_email = 'Please enter a valid email'
validation_booking = 'Booking complete!'


def create_app(config=None):
    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.from_object(config)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/show_summary', methods=['POST'])
    def show_summary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            return render_template('welcome.html', club=club, competitions=competitions)
        except IndexError:
            flash(error_email)
            return redirect(url_for('index'))

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        try:
            club = [c for c in clubs if c['name'] == club][0]
            competition = [c for c in get_future_competitions(competitions) if c['name'] == competition][0]
            if club and competition:
                max_places = int(club['points'])
                if max_places > max_bookable_places:
                    max_places = max_bookable_places
                return render_template('booking.html', club=club, competition=competition, max_places=max_places)
        except IndexError:
            flash(error_default)
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
