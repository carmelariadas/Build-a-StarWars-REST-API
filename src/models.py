from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    birthday_year = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name,
            "birthday_year": self.birthday_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }



class Planets (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
        }

class Fav_Characters (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship(Characters)

    def __repr__(self):
        return '<Fav_Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
            "character_id": self.character_id,
        }


class Fav_Planets (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship(Planets)

    def __repr__(self):
        return '<Fav_Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id, 
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

