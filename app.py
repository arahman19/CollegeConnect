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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    #Should log the user out and return to homepage
    return render_template('index.html')
    

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')