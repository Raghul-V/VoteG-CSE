from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    batch = db.Column(db.String(1), nullable=False)
    votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Person {self.id}>"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        try:
            new_vote = request.form.get("new-vote")
            if new_vote:
                old_vote = request.form.get("old-vote")
                if old_vote:
                    old_vote_for = Person.query.get_or_404(old_vote)
                    old_vote_for.votes -= 1
                new_vote_for = Person.query.get_or_404(new_vote)
                new_vote_for.votes += 1
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your vote!..."
    leaderboard = Person.query.order_by(-Person.votes, Person.batch, Person.name).all()
    return render_template("index.html", leaderboard=leaderboard)


if __name__ == '__main__':
    app.run(debug=True)

