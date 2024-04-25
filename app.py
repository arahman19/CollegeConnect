from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

app = Flask(__name__, static_url_path='/Static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config["SECRET_KEY"] = "abc"
 
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db)

class Account(db.Model, UserMixin):
    # Id : Field which stores unique id for every row in 
    # database table.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    gender = db.Column(db.Integer, default=999)
    grade = db.Column(db.Integer, default=999)
    religion = db.Column(db.Integer, default=999)
    drugs = db.Column(db.Integer, default=999)
    neatness = db.Column(db.Integer, default=999)
    chronotype = db.Column(db.Integer, default=999)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Username : {self.username}, Password: {self.password}, Email: {self.email}, Gender: {self.gender}, Grade: {self.grade}, Religion: {self.religion}, Drugs: {self.drugs}, Neatness: {self.neatness}, Chronotype: {self.chronotype}"

class RoommateCriteriaForm(FlaskForm):
    minAge = IntegerField('Minimum Age', validators=[NumberRange(min=18, max=100)])
    maxAge = IntegerField('Maximum Age', validators=[NumberRange(min=18, max=100)])
    gender = SelectField('Gender', choices=[('999', 'Any'), ('0', 'Male'), ('1', 'Female')], coerce=int)
    grade = SelectField('Grade', choices=[('999', 'Any'), ('0', 'Freshman'), ('1', 'Sophomore'), ('2', 'Junior'), ('3', 'Senior')], coerce=int)
    religion = SelectField('Religion', choices=[('999', 'Any'), ('0', 'Christian'), ('1', 'Muslim'), ('2', 'Jewish'), ('3', 'Buddhist')], coerce=int)
    drugs = SelectField('Drug Stance', choices=[('999', 'Any'), ('0', 'No Drugs'), ('1', 'Occasional'), ('2', 'Regular')], coerce=int)
    minNeatness = IntegerField('Minimum Neatness', validators=[NumberRange(min=1, max=5)])
    maxNeatness = IntegerField('Maximum Neatness', validators=[NumberRange(min=1, max=5)])
    chronotype = SelectField('Chronotype', choices=[('999', 'Any'), ('0', 'Early Bird'), ('1', 'Night Owl')], coerce=int)
    submit = SubmitField('Find Roommates')

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    threads = db.relationship('Thread', backref='topic', lazy=True)

    def __repr__(self):
        return f'<Topic {self.title}>'
    
def add_initial_topics():
        initial_topics = ['General Discussion', 'Feedback', 'News', 'Events']
        existing_topics = Topic.query.with_entities(Topic.title).all()
        existing_titles = {title[0] for title in existing_topics}

        for title in initial_topics:
            if title not in existing_titles:
                new_topic = Topic(title=title)
                db.session.add(new_topic)
    
        db.session.commit()
    
@app.cli.command('init-db')
def init_db():
    add_initial_topics()

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    user = db.relationship('Account', backref='threads')
    posts = db.relationship('Post', backref='thread', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Thread {self.title}>'
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    posted_on = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('Account', backref='posts')

    def __repr__(self):
        return f'<Post {self.content[:30]}>'
    
class ThreadForm(FlaskForm):
    title = StringField('Thread Title', validators=[DataRequired()])
    submit = SubmitField('Create Thread')
    
# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Account.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forums')
def forums():
    return render_template('forums.html')

@app.route('/topics')
def topics():
    all_topics = Topic.query.all()
    return render_template('topics.html', topics=all_topics)

@app.route('/threads/<int:topic_id>')
def threads(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    form = ThreadForm()
    return render_template('threads.html', topic=topic, form=form)

@app.route('/create-thread/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def create_thread(topic_id):
    form = ThreadForm()
    if form.validate_on_submit():
        new_thread = Thread(title=form.title.data, topic_id=topic_id, user_id=current_user.id)
        db.session.add(new_thread)
        db.session.commit()
        return redirect(url_for('threads', topic_id=topic_id))
    topic = Topic.query.get_or_404(topic_id)
    return render_template('threads.html', topic=topic, form=form)

@app.route('/delete-thread/<int:thread_id>', methods=['POST'])
@login_required
def delete_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if thread.user_id != current_user.id:
        return abort(403)
    db.session.delete(thread)
    db.session.commit()
    return redirect(url_for('threads', topic_id=thread.topic_id))


@app.route('/posts/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def posts(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if request.method == 'POST':
        post_content = request.form.get('content')
        if post_content:
            post = Post(content=post_content, thread_id=thread.id, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(request.url)
    posts = thread.posts.all()
    return render_template('posts.html', thread=thread, posts=posts)

@app.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts', thread_id=post.thread_id))

@app.route('/roommate')
@app.route('/roommate', methods=['GET', 'POST'])
def roommate():
    form = RoommateCriteriaForm()
    roommateList = []

    if form.validate_on_submit():
        criteria = accountCriteria(
            minAge=form.minAge.data,
            maxAge=form.maxAge.data,
            gender=form.gender.data,
            grade=form.grade.data,
            religion=form.religion.data,
            drugs=form.drugs.data,
            minNeatness=form.minNeatness.data,
            maxNeatness=form.maxNeatness.data,
            interests=form.interests.data,
            chronotype=form.chronotype.data
        )

        for a in database:
            check = True

            if (criteria.minAge != 999 and criteria.maxAge != 999):
                if not (a.age >= criteria.minAge and a.age <= criteria.maxAge):
                    check = False

            if (criteria.gender != 999 and check):
                if not (a.gender == criteria.gender):
                    check = False

            if (criteria.grade != 999 and check):
                if not (a.grade == criteria.grade):
                    check = False

            if (criteria.religion != 999 and check):
                if not (a.religion == criteria.religion):
                    check = False

            if (criteria.drugs != 999 and check):
                if not (a.drugs == criteria.drugs):
                    check = False

            if (criteria.minNeatness != 999 and criteria.maxNeatness != 999 and check):
                if not (a.neatness >= criteria.minNeatness and a.neatness <= criteria.maxNeatness):
                    check = False

            if (criteria.interests != "N/A" and check):
                if not (criteria.interests in a.interests):
                    check = False

            if (criteria.chronotype != 999 and check):
                if not (a.chronotype == criteria.chronotype):
                    check = False

            if check:
                roommateList.append(a)

    return render_template('roommate.html', form=form, roommateList=roommateList)

@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by 
    # filtering for the email
    if request.method == "POST":
        account = Account.query.filter_by(
            email=request.form.get("email")).first()
        # Check if the password entered is the 
        # same as the user's password
        if account.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(account)
            return redirect('/')
        else:
            return redirect('/login')
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    logout_user()
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

@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and 
    # redirects to home page
    data = Account.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

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
        return redirect('/login')
    else:
        return redirect('/signup')

if __name__ == '__main__':
    db.create_all()
    app.run()