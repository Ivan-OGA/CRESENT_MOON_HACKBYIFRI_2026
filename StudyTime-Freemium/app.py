from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#on configure la db de notre fichier instance studytime.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studytime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# *************************************************************************************************
# *************************************************************************************************


# *************************************************************************************************
# *************************************************************************************************
# définitions des tables de bases de données  utilisées via sqlAlchemy 

#table pour contenir les infos de l'étudiant
class Profil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    matricule = db.Column(db.String(50))
    etablissement = db.Column(db.String(200))
    filiere = db.Column(db.Text)


#table pour contenir les infos de cours , comme les noms , les identifiants , les crédits de la matière , etc
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    next_class = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Float, nullable=False)


#table pour gérer les id des questions  
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    questions = db.relationship('Question', backref='subject', lazy=True)

# table pour les quizs 
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200))
    option_a = db.Column(db.String(100))
    option_b = db.Column(db.String(100))
    option_c = db.Column(db.String(100))
    option_d = db.Column(db.String(100))
    correct_answer = db.Column(db.String(1))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

# *************************************************************************************************
# *************************************************************************************************


# *************************************************************************************************
# *************************************************************************************************
#

#definitions de fonction  insert_questions pour enregistrer ,montrer et vérifier les quiz sur la page quiz.html 

def insert_questions():
    if Subject.query.count() == 0:
        topo = Subject(name="Topologie")
        linux = Subject(name="Administration Linux")
        db.session.add_all([topo, linux])
        db.session.commit()

        questions = [
            # Topologie
            Question(question_text="Quelle topologie utilise un câble central ?",
                     option_a="Anneau", option_b="Bus", option_c="Étoile", option_d="Maillée",
                     correct_answer="B", subject_id=topo.id),

            Question(question_text="Quelle topologie connecte tous les noeuds entre eux ?",
                     option_a="Bus", option_b="Étoile", option_c="Maillée", option_d="Anneau",
                     correct_answer="C", subject_id=topo.id),

            Question(question_text="Quel masque correspond au préfixe /26 ?",
                     option_a="255.255.255.0", option_b="255.255.255.192", option_c="255.255.255.128",
                     option_d="255.255.255.224", correct_answer="B", subject_id=topo.id),

            Question(question_text="Quelle classe d'adresse appartient à 10.0.0.1 ?",
                     option_a="Classe A", option_b="Classe B", option_c="Classe C", option_d="Classe D",
                     correct_answer="A", subject_id=topo.id),

            Question(question_text="Combien d'hôtes maximum peut-on avoir dans un réseau 192.168.5.0/26 ?",
                     option_a="62", option_b="64", option_c="32", option_d="126",
                     correct_answer="A", subject_id=topo.id),

            # Linux
            Question(question_text="Quelle commande liste les fichiers ?",
                     option_a="ls", option_b="cd", option_c="pwd", option_d="mkdir",
                     correct_answer="A", subject_id=linux.id),

            Question(question_text="Quelle commande change les permissions ?",
                     option_a="chmod", option_b="cp", option_c="rm", option_d="touch",
                     correct_answer="A", subject_id=linux.id),

            Question(question_text="La commande pour modifier les droits tel que seul l'utilisateur puisse tout et le groupe écrire uniquement un fichier file.txt est ?",
                     option_a="chmod 700 file.txt", option_b="chmod 744 file.txt",
                     option_c="chmod 740 file", option_d="chmod u=rwx,g=r,o= file.txt",
                     correct_answer="D", subject_id=linux.id),

            Question(question_text="Quel fichier contient les utilisateurs ?",
                     option_a="/etc/passwd", option_b="/home", option_c="/bin", option_d="/var",
                     correct_answer="A", subject_id=linux.id),

            Question(question_text="Que fait touch file.txt ?",
                     option_a="Supprime un fichier txt", option_b="Crée un fichier file.txt",
                     option_c="Recherche le fichier file.txt", option_d="Aucune des réponses",
                     correct_answer="B", subject_id=linux.id)
        ]
        db.session.add_all(questions)
        db.session.commit()


# *************************************************************************************************
# *************************************************************************************************
# *************************************************************************************************
# *************************************************************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
# Etablissont les routes vers les pages html pour la gestion dynamique !

# route principale  vers (index.html)

@app.route('/')
def home():
    courses = Course.query.all()
    total_cours = len(courses)
    total_credits = sum(c.credits for c in courses)
    moyenneG = round(sum(c.grade for c in courses) / total_cours, 2) if total_cours > 0 else 0
    success_courses = len([c for c in courses if c.grade >= 10])
    success_rate = round((success_courses / total_cours) * 100, 2) if total_cours > 0 else 0
#retour de données , de même que vers index.html
    return render_template('index.html',
                           courses=courses,
                           total_cours=total_cours,
                           total_credits=total_credits,
                           moyenneG=moyenneG,
                           success_rate=success_rate)

# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
@app.route("/profil", methods=["GET", "POST"])
def profil():
    # Toujours récupérer le premier profil dans la BDD
    profil_utilisateur = Profil.query.first()

    if request.method == "POST":
        # Crée uniquement si aucun profil n'existe
        if not profil_utilisateur:
            profil_utilisateur = Profil(
                username=request.form.get("username"),
                email=request.form.get("email"),
                matricule=request.form.get("matricule"),
                etablissement=request.form.get("etablissement"),
                filiere=request.form.get("filiere")
            )
            db.session.add(profil_utilisateur)
            db.session.commit()
    return render_template("profil.html", profil=profil_utilisateur)
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
@app.route("/add_course", methods=["POST"])
def add_course():
    name = request.form["name"]
    credits = int(request.form["credits"])
    next_class = request.form["next_class"]
    grade = float(request.form["grade"])

    new_course = Course(name=name, credits=credits, next_class=next_class, grade=grade)
    db.session.add(new_course)
    db.session.commit()

    return redirect("/myclasses")
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    subjects = Subject.query.all()
    questions = None

    if request.method == "POST":
        subject_id = int(request.form.get("subject_id"))
        questions = Question.query.filter_by(subject_id=subject_id).all()
        score = 0
        for q in questions:
            user_answer = request.form.get(f"question_{q.id}")
            if user_answer == q.correct_answer:
                score += 1
        total = len(questions)
        percentage = round((score / total) * 20, 2)  # note sur 20

        # Mise à jour dans la BDD
        subject = Subject.query.get(subject_id)
        course = Course.query.filter_by(name=subject.name).first()
        if course:
            course.grade = percentage
            db.session.commit()

        return render_template("quiz.html",
                               subjects=subjects,
                               result=True,
                               score=score,
                               total=total,
                               percentage=percentage)

    # GET request
    subject_id = request.args.get("subject_id")
    if subject_id:
        subject_id = int(subject_id)
        questions = Question.query.filter_by(subject_id=subject_id).all()

    return render_template("quiz.html",
                           subjects=subjects,
                           questions=questions,
                           result=False,
                           subject_id=subject_id if subject_id else None)
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
@app.route("/myclasses") 
def myclasses():
    courses = Course.query.all()  # prend tous les cours depuis la DB
    return render_template("myclasses.html", courses=courses)
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
@app.route("/rattrapage") #page dynamiquement gérée avec js
def rattrapage():
    return render_template("rattrapage.html")
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
@app.route("/planning") #page dynamiquement gérée avec js
def planning():
    return render_template("planning.html")
# ***********************************************************
# ***********************************************************
# ***********************************************************
# ***********************************************************
# *************************************************************************************************
# *************************************************************************************************
# *************************************************************************************************
# *************************************************************************************************
#Lancement de l'app web"
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Insérer les matières + questions si vide
        insert_questions()

        # petite condition pour insérer les  cours topologie et linux si le bd est vide 
        if Course.query.count() == 0:
            db.session.add(Course(name="Topologie", credits=2, next_class="Mardi 10h", grade=0))
            db.session.add(Course(name="Administration Linux", credits=4, next_class="Jeudi 14h", grade=0))
            db.session.commit()

    app.run(debug=True)


































































































































    

# *************************************************************************************************




