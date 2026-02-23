from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# CONFIGURATION DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studytime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# profil


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    matricule= db.Column(db.String(50))
    etablissement = db.Column(db.String(200))
    filière = db.Column(db.Text)


# routes


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profil")
def profil():
    return render_template("profil.html")

@app.route("/save_profile", methods=["POST"])
def save_profile():

    username = request.form.get("username")
    email = request.form.get("email")
    matricule= request.form.get("matricule")
    etablissement = request.form.get("etablissement")
    filière = request.form.get("filière")

    new_profile = Profile(
        username=username,
        email=email,
        matricule=matricule,
        etablissement=etablissement,
        filière=filière
    )

    db.session.add(new_profile)
    db.session.commit()

    return redirect("/profil")

# Lancement

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)