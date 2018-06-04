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
    phone = db.Column(db.Text, nullable=False)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.coordinator_id'))
    mobilizees = db.relationship("Mobilizee", backref="mobilizer")

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self, name, username, email, phone, password, coordinator_id):
        self.name = name
        self.username = username
        self.email = email
        self.phone = phone
        self.password = password
        self.coordinator_id = coordinator_id

    def __repr__(self):
        return '<Mobilizer {}>'.format(self.mobilizer_id)

class Mobilizee(db.Model):
    mobilizee_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.Text, nullable=False)
    fname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    notes = db.relationship("Note", backref="mobilizee")
    mobilizer_id = db.Column(db.Integer, db.ForeignKey('mobilizer.mobilizer_id'))

    def __init__(self, lname, fname, email, phone, address, mobilizer_id=-1):
        self.lname = lname
        self.fname = fname
        self.email = email
        self.phone = phone
        self.address = address
        self.notes = []
        self.mobilizer_id = mobilizer_id

    def __repr__(self):
        return '<Mobilizee {}>'.format(self.mobilizer_id)

class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    mobilizee_id = db.Column(db.Integer, db.ForeignKey('mobilizee.mobilizee_id'))
    content = db.Column(db.Text, nullable=False)

    def __init__(self, mobilizee_id, content):
        self.mobilizee_id = mobilizee_id
        self.content = content

    def __repr__(self):
        return '<Note {}>'.format(self.mobilizer_id)

class Coordinator(db.Model):
    coordinator_id = db.Column(db.Integer, primary_key=True)
    mobilizers = db.relationship("Mobilizer", backref="coordinator")
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable = False)
    removal_requests = db.relationship("Request", backref="request_coordinator")

    def __init__(self,  username, password):
        self.username = username
        self.password = password

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password):
        return sha256.verify(password, hash)

class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    mobilizee_id = db.Column(db.Integer, db.ForeignKey('mobilizee.mobilizee_id'))
    coordinator = db.Column(db.Integer, db.ForeignKey('coordinator.coordinator_id'))

    def __init__(self, mobilizee_id, coordinator_id):
        self.mobilizee_id = mobilizee_id
        self.coordinator = coordinator_id