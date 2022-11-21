from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy() # avoid circular import

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  # implement any missing fields, as a database migration using Flask-Migrate
  genres = db.Column(db.ARRAY(db.String))
  website = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='venue', lazy=True)
  # define 'created_at' to default to now()
  created_at = db.Column(db.DateTime, server_default=func.now())
  # define 'last_modified_at' to use the current_timestamp SQL function on update
  last_modified_at = db.Column(db.DateTime, onupdate=func.now())

class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  # genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  # implement any missing fields, as a database migration using Flask-Migrate
  genres = db.Column(db.ARRAY(db.String))
  website = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='artist', lazy=True)
  # define 'created_at' to default to now()
  created_at = db.Column(db.DateTime, server_default=func.now())
  # define 'last_modified_at' to use the current_timestamp SQL function on update
  last_modified_at = db.Column(db.DateTime, onupdate=func.now())

# Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'
  
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  # define 'created_at' to default to now()
  created_at = db.Column(db.DateTime, server_default=func.now())
  # define 'last_modified_at' to use the current_timestamp SQL function on update
  last_modified_at = db.Column(db.DateTime, onupdate=func.now())