from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('index'))

    if not is_valid_password(password):
        flash('Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long.', 'danger')
        return redirect(url_for('index'))

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email address already used! Please login using your previous credentials or use a new email address.', 'danger')
        return redirect(url_for('index'))

    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return render_template('thankyou.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()

        if user:
            return render_template('secretPage.html')
        else:
            flash('Wrong credentials!', 'danger')
            return redirect(url_for('signin'))

    return render_template('signin.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
