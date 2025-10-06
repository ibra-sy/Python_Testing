"""Main Flask application file for the GUDLFT registration system."""

import json
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


def load_json(filename: str, key: str):
    """Load data from a JSON file."""
    filepath = BASE_DIR / filename
    with open(filepath, encoding="utf-8") as file:
        return json.load(file)[key]


def save_json(filename: str, key: str, data):
    """Save data to a JSON file."""
    filepath = BASE_DIR / filename
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump({key: data}, file, indent=4)


def load_clubs():
    """Load all clubs from the JSON file."""
    return load_json("clubs.json", "clubs")


def load_competitions():
    """Load all competitions from the JSON file."""
    return load_json("competitions.json", "competitions")


def save_clubs(clubs_data):
    """Save clubs to the JSON file."""
    save_json("clubs.json", "clubs", clubs_data)


def save_competitions(competitions_data):
    """Save competitions to the JSON file."""
    save_json("competitions.json", "competitions", competitions_data)


# ----------------------------------------------------------------------
# Flask app initialization
# ----------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "something_special"

# Make datetime globally available in Jinja templates
app.jinja_env.globals.update(datetime=datetime)

# Load data once at startup
competitions = load_competitions()
clubs = load_clubs()

# Normalize data types and ensure bookings tracking exists
for club in clubs:
    try:
        club["points"] = int(club.get("points", 0))
    except (ValueError, TypeError):
        club["points"] = 0

for competition in competitions:
    try:
        competition["numberOfPlaces"] = int(competition.get("numberOfPlaces", 0))
    except (ValueError, TypeError):
        competition["numberOfPlaces"] = 0
    if not isinstance(competition.get("bookings"), dict):
        competition["bookings"] = {}

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------


@app.route("/", methods=["GET"])
def index():
    """Render the login page."""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """Handle user login and display the main welcome page."""
    email = request.form.get("email")
    if not email:
        flash("Please enter an email address.")
        return redirect(url_for("index"))

    club = next((c for c in clubs if c.get("email") == email), None)
    if not club:
        flash("Sorry, that email was not found.")
        return redirect(url_for("index"))

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>", methods=["GET"])
def book(competition: str, club: str):
    """Render the booking page for a specific competition and club."""
    found_club = next((c for c in clubs if c.get("name") == club), None)
    found_competition = next(
        (c for c in competitions if c.get("name") == competition), None
    )

    if not found_club or not found_competition:
        flash("Something went wrong. The club or competition " "could not be found.")
        return redirect(url_for("index"))

    # Compute cumulative bookings for this club
    bookings = found_competition.get("bookings", {})
    already_booked = int(bookings.get(found_club["name"], 0))
    remaining_quota = max(0, 12 - already_booked)

    return render_template(
        "booking.html",
        club=found_club,
        competition=found_competition,
        already_booked=already_booked,
        remaining_quota=remaining_quota,
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    """Handle the logic for purchasing places in a competition."""
    club_name = request.form.get("club")
    competition_name = request.form.get("competition")

    club = next((c for c in clubs if c.get("name") == club_name), None)
    competition = next(
        (c for c in competitions if c.get("name") == competition_name), None
    )

    if not club or not competition:
        flash("An error occurred during booking. Please try again.")
        return redirect(url_for("index"))

    try:
        places_required = int(request.form.get("places", 0))
    except (ValueError, TypeError):
        flash("Invalid number of places provided.")
        return render_template("welcome.html", club=club, competitions=competitions)

    club_points = int(club.get("points", 0))
    competition_places = int(competition.get("numberOfPlaces", 0))
    bookings = competition.get("bookings", {})
    already_booked = int(bookings.get(club_name, 0))

    if places_required <= 0:
        flash("You must book at least 1 place.")
    elif places_required > 12:
        flash("You cannot book more than 12 places in a single transaction.")
    elif already_booked >= 12:
        flash("You have already booked the maximum of 12 places for this competition.")
    elif already_booked + places_required > 12:
        remaining = 12 - already_booked
        flash(
            f"Booking exceeds limit. You already have {already_booked}; "
            f"you can only add {remaining} more to reach 12."
        )
    elif places_required > club_points:
        flash(f"Not enough points. You have {club_points} but need {places_required}.")
    elif places_required > competition_places:
        flash(f"Not enough places available. Only {competition_places} left.")
    else:
        club["points"] = club_points - places_required
        competition["numberOfPlaces"] = competition_places - places_required
        bookings[club_name] = already_booked + places_required
        competition["bookings"] = bookings
        save_clubs(clubs)
        save_competitions(competitions)
        flash("Great! Booking complete.")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/points", methods=["GET"])
def points_dashboard():
    """Render the public points leaderboard."""
    return render_template("points.html", clubs=clubs, competitions=competitions)


@app.route("/logout", methods=["GET"])
def logout():
    """Log the user out and redirect to the login page."""
    return redirect(url_for("index"))


# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
