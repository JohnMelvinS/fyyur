#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys

from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
# connect to a local postgresql database
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Utilities.
#----------------------------------------------------------------------------#

def populate_venue_model(form, venue_id=''):
  venue=Venue()
  if venue_id:
    venue=Venue.query.get(venue_id)
  venue.name = form.name.data
  venue.city = form.city.data
  venue.state = form.state.data
  venue.address = form.address.data
  venue.phone = form.phone.data
  venue.genres = form.genres.data
  venue.facebook_link = form.facebook_link.data
  venue.image_link = form.image_link.data
  venue.website = form.website_link.data
  venue.seeking_talent = form.seeking_talent.data
  venue.seeking_description = form.seeking_description.data
  return venue

def populate_artist_model(form, artist_id=''):
  artist=Artist()
  if artist_id:
    artist=Artist.query.get(artist_id)
  artist.name = form.name.data
  artist.city = form.city.data
  artist.state = form.state.data
  artist.phone = form.phone.data
  artist.genres = form.genres.data
  artist.facebook_link = form.facebook_link.data
  artist.image_link = form.image_link.data
  artist.website = form.website_link.data
  artist.seeking_venue = form.seeking_venue.data
  artist.seeking_description = form.seeking_description.data
  return artist

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  # Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
  artists=Artist.query.order_by(db.desc(Artist.created_at)).limit(10).all()
  artists_count = len(artists)
  venues=Venue.query.order_by(db.desc(Venue.created_at)).limit(10).all()
  venues_count = len(venues)
  return render_template('pages/home.html', artists=artists, artists_count=artists_count, venues=venues, venues_count=venues_count)

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  # venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  venues = Venue.query.order_by('city', 'state').all()
  city_state = ''
  data = []

  for venue in venues:
    num_upcoming_shows = 0
    for show in venue.shows:
      if show.start_time > datetime.now():
        num_upcoming_shows+=1

    if city_state == venue.city + venue.state:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name":venue.name,
        "num_upcoming_shows": num_upcoming_shows # a count of the number of upcoming shows
      })
    else:
      city_state = venue.city + venue.state
      data.append({
        "city":venue.city,
        "state":venue.state,
        "venues": [{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": num_upcoming_shows # a count of the number of upcoming shows
        }]
      })
      
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')

  # Implement Search Venues by City and State. Searching by "San Francisco, CA" should return all venues in San Francisco, CA.
  conditions = []
  for word in search_term.replace(',','').split():
    conditions.append(Venue.name.ilike('%{}%'.format(word)))
    conditions.append(Venue.city.ilike('%{}%'.format(word)))
    conditions.append(Venue.state.ilike('%{}%'.format(word)))

  data = Venue.query.filter(or_(*conditions))

  response={
    "count": data.count(),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id

  venue = Venue.query.get(venue_id)

  venue.past_shows = []
  venue.past_shows_count = 0
  venue.upcoming_shows = []
  venue.upcoming_shows_count = 0
  
  for show in venue.shows:
    artist=Artist.query.get(show.artist_id)
    if show.start_time > datetime.now():
      venue.upcoming_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time.strftime("%A, %b %d, %Y at %-I:%M%p")
      })
      venue.upcoming_shows_count+=1
    else :
      venue.past_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time.strftime("%A, %b %d, %Y at %-I:%M%p")
      })
      venue.past_shows_count+=1

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # insert form data as a new Venue record in the db, instead
  # modify data to be the data object returned from db insertion
  error = False
  form = VenueForm()
  venue=populate_venue_model(form)
  try:
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue \"' + venue.name + '\" was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print (sys.exc_info)
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue \"' + venue.name + '\" could not be listed!')
  finally:
    db.session.close()
    if not error :
      # return render_template('pages/home.html')
      # return index()
      return render_template('pages/show_venue.html', venue=venue)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  error = False
  try:
    venue=Venue.query.get(venue_id)
    
    shows_count = 0
    for show in venue.shows:
      shows_count += 1

    if shows_count == 0:
      Venue.query.filter_by(id=venue_id).delete()
      db.session.commit()
      # on successful db delete, flash success
      flash('Venue was successfully deleted!')
    else :
      error = True
      # on unsuccessful db delete, flash an error instead.
      flash('An error occurred. Venue could not be deleted as venue has shows!')
    
  except:
    error = True
    db.session.rollback()
    # print (sys.exc_info)
    # on unsuccessful db delete, flash an error instead.
    flash('An error occurred. Venue could not be deleted!')
  finally:
    db.session.close()
    if not error :
      return {}, 200
    else:
      return {}, 400

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')

  # Implement Search Artists by City and State. Searching by "San Francisco, CA" should return all artists in San Francisco, CA.
  conditions = []
  for word in search_term.replace(',','').split():
    conditions.append(Artist.name.ilike('%{}%'.format(word)))
    conditions.append(Artist.city.ilike('%{}%'.format(word)))
    conditions.append(Artist.state.ilike('%{}%'.format(word)))

  data = Artist.query.filter(or_(*conditions))
  
  response={
    "count": data.count(),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id

  artist=Artist.query.get(artist_id)

  artist.past_shows = []
  artist.past_shows_count = 0
  artist.upcoming_shows = []
  artist.upcoming_shows_count = 0
  
  for show in artist.shows:
    venue=Venue.query.get(show.venue_id)
    if show.start_time > datetime.now():
      artist.upcoming_shows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": show.start_time.strftime("%A, %b %d, %Y at %-I:%M%p")
      })
      artist.upcoming_shows_count+=1
    else :
      artist.past_shows.append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": show.start_time.strftime("%A, %b %d, %Y at %-I:%M%p")
      })
      artist.past_shows_count+=1

  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  #populate form with fields from artist with ID <artist_id>
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  error = False
  form = ArtistForm()

  # if form.validate_on_submit():
  #   print("Valid phone number")
  try:
    artist=populate_artist_model(form, artist_id)
    db.session.commit()
    # on successful db update, flash success
    flash('Artist \"' + form.name.data + '\" was successfully edited!')
  except:
    error = True
    db.session.rollback()
    print (sys.exc_info)
    # on unsuccessful db update, flash an error instead.
    flash('An error occurred. Artist \"' + form.name.data + '\" could not be edited!')
  finally:
    db.session.close()
    if not error :
      return redirect(url_for('show_artist', artist_id=artist_id))
  # else:
  #   # on unsuccessful db update, flash an error instead.
  #   flash('An error occurred. Artist \"' + form.name.data + '\" could not be edited!')
  #   return redirect(url_for('/artists/<int:artist_id>/edit', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.get(venue_id)
  # populate form with values from venue with ID <venue_id>
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website_link.data = venue.website
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  form = VenueForm()
  try:
    venue=populate_venue_model(form, venue_id)
    db.session.commit()
    # on successful db update, flash success
    flash('Venue \"' + form.name.data + '\" was successfully edited!')
  except:
    error = True
    db.session.rollback()
    print (sys.exc_info)
    # on unsuccessful db update, flash an error instead.
    flash('An error occurred. Venue \"' + form.name.data + '\" could not be edited!')
  finally:
    db.session.close()
    if not error :
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # insert form data as a new Artist record in the db, instead
  # modify data to be the data object returned from db insertion
  error = False
  form = ArtistForm()
  artist=populate_artist_model(form)
  try:
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist \"' + artist.name + '\" was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print (sys.exc_info)
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist \"' + artist.name + '\" could not be listed!')
  finally:
    db.session.close()
    if not error :
      # return render_template('pages/home.html')
      # return index()
      return render_template('pages/show_artist.html', artist=artist)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # replace with real venues data.
  data = []
  shows = Show.query.order_by(Show.start_time.desc()).all()
  for show in shows:
    venue = Venue.query.filter_by(id=show.venue_id).first()
    artist = Artist.query.filter_by(id=show.artist_id).first()
    data.extend([{
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": show.start_time.strftime("%A, %b %d, %Y at %-I:%M%p")
    }])
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # insert form data as a new Show record in the db, instead
  error = False
  try:
    form = ShowForm()
    show=Show()
    show.artist_id = form.artist_id.data
    show.venue_id = form.venue_id.data
    show.start_time = form.start_time.data
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print (sys.exc_info)
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
    if not error :
      # return render_template('pages/home.html')
      # return index()
      return redirect(url_for('shows'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
