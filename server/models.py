from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship: A Hero has many HeroPowers
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    
    # Serialization: Exclude hero_powers.hero to avoid infinite recursion
    serialize_rules = ('-hero_powers.hero',)

    def __repr__(self):
        return f'<Hero {self.id}: {self.super_name}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship: A Power has many HeroPowers
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    
    # Serialization: Exclude hero_powers.power
    serialize_rules = ('-hero_powers.power',)

    # Validation: description must be present and at least 20 characters long
    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

    def __repr__(self):
        return f'<Power {self.id}: {self.name}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Foreign Keys
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    # Relationships back to parents
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    # Serialization: Exclude parent relationships to avoid recursion
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    # Validation: strength must be one of: 'Strong', 'Weak', 'Average'
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return value

    def __repr__(self):
        return f'<HeroPower {self.id}: {self.strength}>'