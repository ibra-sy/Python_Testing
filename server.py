"""
Main Flask application file for the GUDLFT registration system.
"""

import json
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for


def load_clubs():
    """Loads clubs from a JSON file."""
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    """Loads competitions from a JSON file."""
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


def save_clubs(clubs_data):
    """Saves clubs data to a JSON file."""
    with open("clubs.json", "w") as c:
        json.dump({"clubs": clubs_data}, c, indent=4)


def save_competitions(competitions_data):
    """Saves competitions data to a JSON file."""
    with open("competitions.json", "w") as comps:
        json.dump({"competitions": competitions_data}, comps, indent=4)


app = Flask(__name__)
app.secret_key = "something_special"

# Makes the 'datetime' object available in all Jinja2 templates.
app.jinja_env.globals.update(datetime=datetime)

# Load data at application startup.
competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    """Renders the login page."""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """Handles user login and displays the main welcome page."""
    club = next((c for c in clubs if c["email"] == request.form["email"]), None)
    if not club:
        flash("Sorry, that email was not found.")
        return redirect(url_for("index"))

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Renders the booking page for a specific competition and club."""
    found_club = next((c for c in clubs if c["name"] == club), None)
    found_competition = next((c for c in competitions if c["name"] == competition), None)

    if not found_club or not found_competition:
        flash("Something went wrong. The club or competition could not be found.")
        return redirect(url_for("index"))

    return render_template("booking.html", club=found_club, competition=found_competition)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    """Handles the logic for purchasing places in a competition."""
    club = next((c for c in clubs if c["name"] == request.form["club"]), None)
    competition = next(
        (c for c in competitions if c["name"] == request.form["competition"]), None
    )

    if not club or not competition:
        flash("An error occurred during booking. Please try again.")
        return redirect(url_for("index"))

    try:
        places_required = int(request.form["places"])
    except (ValueError, TypeError):
        flash("Invalid number of places provided.")
        return render_template("welcome.html", club=club, competitions=competitions)

    club_points = int(club["points"])
    competition_places = int(competition["numberOfPlaces"])

    if places_required <= 0:
        flash("You must book at least 1 place.")
    elif places_required > 12:
        flash("You cannot book more than 12 places in a single transaction.")
    elif places_required > club_points:
        flash(f"You don't have enough points. You need {places_required} but only have {club_points}.")
    elif places_required > competition_places:
        flash(f"Not enough places available. Only {competition_places} left.")
    else:
        club["points"] = club_points - places_required
        competition["numberOfPlaces"] = competition_places - places_required
        save_clubs(clubs)
        save_competitions(competitions)
        flash("Great! Booking complete.")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/points")
def points_dashboard():
    """Renders the public points leaderboard."""
    return render_template("points.html", clubs=clubs)


@app.route("/logout")
def logout():
    """Logs the user out and redirects to the login page."""
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)