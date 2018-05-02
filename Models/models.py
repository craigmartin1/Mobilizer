from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256
import numpy as np
import pandas as pd
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Mobilizer(db.Model):
    mobilizer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(120), nullable = False)
    email = db.Column(db.Text, unique = True, nullable=False)
    phone = db.Column(db.Text, unique=True, nullable=False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password):
        return sha256.verify(password, hash)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, name, username, email, phone, password):
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password

    def __repr__(self):
        return '<Mobilizer {}>'.format(self.mobilizer_id)

class Mobilizee(db.Model):
    mobilizee_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.Text, nullable=False)
    fname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    #NOTE RELATIONSHIP

    def __init__(self, lname, fname, email, phone, address):
        self.lname = lname
        self.fname = fname
        self.email = email
        self.phone = phone
        self.address = address

    def __repr__(self):
        return '<Mobilizee {}>'.format(self.mobilizer_id)