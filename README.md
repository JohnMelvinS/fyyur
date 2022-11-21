Fyyur
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

### 2. Frontend Dependencies
 * **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/)

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── migrations *** Your database migrations via Flask-Migrate
  ├── models.py *** Your SQLAlchemy models
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in `models.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`

Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `models.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.

## User Functionalities
  * When a user submits a new artist record, the user can see it populate in /artists, as well as search for the artist by name and have the search return results.
  * User can go to the URL `/artist/<artist-id>` to visit a particular artist’s page using a unique ID per artist.
  * Venues are displayed in groups by city and state.
  * Search allows partial string matching and case-insensitive.
  * Past shows versus Upcoming shows is distinguished in Venue and Artist pages.
  * A user can click on the venue for an upcoming show in the Artist's page, and on that Venue's page, see the same show in the Venue Page's upcoming shows section.

##### Stand Out
* View Recent Listed Artists Carousel and Recently Listed Venues Carousel on the homepage, returning results for Artists and Venues sorting by newly created. Limited to the 10 most recently listed items.
* Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.

## Developer Functionalities
As a fellow developer on this application, you should be able to run `flask db upgrade`, and have your local database (once set up and created) be populated with the right tables to run this application and have it interact with your postgres server, serving the application's needs completely with real data that you can seed your database with.

## Run Fyyur locally
1. **Download the project code locally**
```
git clone https://github.com/JohnMelvinS/fyyur.git
```

2. **Install virtualenv using:**
```
pip install virtualenv
```

3. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

4. **Install the dependencies:**
```
pip install -r requirements.txt
```

5. **Connect to a PostgreSQL database in `config.py`**
```
SQLALCHEMY_DATABASE_URI = '<Put your local database url>'
```

6. **Apply the changes described by the migration script to your database**
```
flask db upgrade
```
>**Note** - If you receive `ModuleNotFoundError: No module named 'dateutil'` error, deactivate and re-activate your virtualenv and then try to apply changes to your database.

7. **Run the development server:**
```
export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
python3 app.py
```

8. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)