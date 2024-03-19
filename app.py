from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/Static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forums')
def forums():
    return render_template('forums.html')

@app.route('/roommate')
def roommate():
    return render_template('roommate.html')

@app.route('/market')
def market():
    return render_template('market.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    #Should log the user out and return to homepage
    return render_template('index.html')
    

@app.route('/profile')
def profile():
    return render_template('profile.html')