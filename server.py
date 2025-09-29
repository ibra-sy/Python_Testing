import json
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def saveClubs(clubs_data):
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs_data}, c, indent=4)

        
def saveCompetitions(competitions_data):
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions_data}, comps, indent=4)


app = Flask(__name__)
app.secret_key = "something_special"
app.jinja_env.globals.update(datetime=datetime)

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    clubs_found = [club for club in clubs if club["email"] == request.form["email"]]
    if not clubs_found:
        flash("Désoler, code incorrect. Email innexitant.")
        return redirect(url_for("index"))
    club = clubs_found[0]

    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    clubs_found = [c for c in clubs if c["name"] == club]
    competitions_found = [c for c in competitions if c["name"] == competition]

    # Vérification pour éviter un crash si le club ou la compétition n'est pas trouvé
    if not clubs_found or not competitions_found:
        flash("Une erreur est survenue. Le club ou la compétition est introuvable.")
        return redirect(url_for('index'))
    
    foundClub = clubs_found[0]
    foundCompetition = competitions_found[0]
    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = next(
        (c for c in competitions if c["name"] == request.form["competition"]), None
    )
    club = next((c for c in clubs if c["name"] == request.form["club"]), None)

    if not competition or not club:
        flash("Erreur lors de la réservation, veuillez réessayer.")
        return redirect(url_for("index"))

    placesRequired = int(request.form["places"])

    if placesRequired <= 0:
        flash("You must book at least 1 place.")
    elif placesRequired > 12:
        flash("You cannot book more than 12 places for a single competition.")
    elif placesRequired > int(club['points']):
        flash("You don't have enough points to book that many places.")
    elif placesRequired > int(competition['numberOfPlaces']):
        flash("There are not enough places available in this competition.")
    else:
        club['points'] = int(club['points']) - placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        saveClubs(clubs)  # Sauvegarder les données des clubs
        saveCompetitions(competitions) # Sauvegarder les données des compétitions
        flash('Great-booking complete!')

    return render_template("welcome.html", club=club, competitions=competitions)



@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
