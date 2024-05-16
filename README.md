# CollegeConnect

CollegeConnect is a web application designed to help college students connect through forums and find compatible roommates based on various criteria.

## Features

- User authentication and profile management
- Forums for general discussion, feedback, news, and events
- Roommate finder based on user-specified criteria such as age, gender, grade, religion, drug use, neatness, interests, and chronotype

## Technologies Used

- Python
- Flask (with Flask-WTF for forms and Flask-SQLAlchemy for database interactions)
- HTML/CSS
- SQLite (for the database)
- Bootstrap (for front-end styling)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/CollegeConnect.git
   cd CollegeConnect
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
   
5. Add initial topics to the database:

   ```bash
   flask init-db
   ```

6. Run the application

   ```bash
   flask run
   ```

7. Open your web browser and go to http://127.0.0.1:5000/ to see the application in action.

## Usage

### User Authentication

* Sign up for a new account.
* Log in with your credentials.
* Edit your profile information.

### Forums

* Browse existing topics and threads.
* Create new threads and posts.
* Delete your own threads and posts.

### Roommate Finder

* Fill out the roommate criteria form to find potential roommates.
* The system will match you with roommates based on your specified criteria.
