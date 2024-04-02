from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_mail import Mail, Message

app = Flask(__name__, static_url_path='/Static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Account(db.Model):
    # Id : Field which stores unique id for every row in 
    # database table.
    # first_name: Used to store the first name if the user
    # last_name: Used to store last name of the user
    # Age: Used to store the age of the user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Username : {self.username}, Password: {self.password}, Email: {self.email}"
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
    
@app.route('/database')
def database():
    accounts = Account.query.all()
    return render_template('database.html', accounts=accounts)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/profileedit')
def profileedit():
    return render_template('profileedit.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        issues = {
        'website': 'the website',
        'account': 'my account',
        'another': 'another user'
        }

        name = request.form.get('name')
        issue = issues[request.form.get('prob')]
        desc = request.form.get('details')
        mail = Mail(app)

        app.config['MAIL_SERVER']='smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'collegeconnectassistance@gmail.com'
        app.config['MAIL_PASSWORD'] = 'vjwe qvdp epjj mhre'
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True

        mail = Mail(app)
    
        msg = Message( 
                    name + ' regarding ' + issue, 
                    sender ='collegeconnectassistance@gmail.com', 
                    recipients = ['collegeconnectassistance@gmail.com'] 
                ) 
        msg.body = desc
        mail.send(msg)
        return redirect('/contact')
    return render_template('contact.html')



@app.route('/create', methods=["POST"])
def account():
     
    # In this function we will input data from the 
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
 
    # create an object of the Account class of models
    # and store data as a row in our datatable
    if username != '' and password != '' and email is not None:
        a = Account(username=username, password=password, email=email)
        db.session.add(a)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run()