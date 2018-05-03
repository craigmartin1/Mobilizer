from flask import session, jsonify
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import re

db = SQLAlchemy()

class SeeMobilizees(Resource):
    def get(self):
        data = see_parser.parse_args()
        mobilizer = data['mobilizer_id']
        mobilizees = Mobilizee.query.filter(Mobilizee.mobilizer_id==mobilizer).all()
        mobilizee_list =[]
        for mobilizee in mobilizees:
            mobilizee_dict = {}
            mobilizee_dict["id"] = mobilizee.mobilizee_id
            mobilizee_dict['name'] = mobilizee.fname + " " + mobilizee.lname
            mobilizee_dict["phone"] = mobilizee.phone
            mobilizee_dict["email"] = mobilizee.email
            mobilizee_dict["address"] = mobilizee.address
            note_list = []
            for note in mobilizee.notes:
                note_list.append(note)
                note_list.reverse()
            mobilizee_dict["notes"] = note_list
            mobilizee_list.append(mobilizee_dict)
        return mobilizee_list

class MakeNote(Resource):
    def post(self):
        data = note_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        note = data["note"]
        mobilizee = Mobilizee.query.filter(Mobilizee.mobilizee_id==mobilizee_id).first()
        mobilizee.notes.append(note)
        return {"Message": "Note appended"}

class RequestRemoval(Resource):
    def post(self):
        data = removal_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        mobilizer_id = data["mobilizer_id"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        request = RemovalRequest(mobilizee_id, mobilizer.coordinator)
        db.session.add(request)
        db.session.commit()
        return {"Message": "Request sent"}

class UpdateContact(Resource):
    def post(self):
        data = update_parser.parse_args()
        email = data["email"]
        phone = data["phone"]
        address = data["address"]
        mobilizee_id = data["mobilizee_id"]
        mobilizee = Mobilizee.query.filter(Mobilizee.mobilizee_id==mobilizee_id).first()
        if(email):
            mobilizee.email = email
        if(phone):
            mobilizee.phone = phone
        if(address):
            mobilizee.address = address
        db.session.commit()
        return {"Message": "Contact updated"}

class AssignMobilizees(Resource):
    def post(self):
        data = assign_parser.parse_args()
        mobilizer_id = data["mobilizer_id"]
        mobilizee_ids = data["mobilizees"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        mobilizees = Mobilizee.query.filter(in_(Mobilizee.mobilizee_id, mobilizee_ids)).all()
        mobilizer.mobilizees.extend(mobilizees)
        db.session.commit()
        return {"Message":"Mobilizees Assigned"}

class RegisterMobilizer(Resource):
    def post(self):
        data = register_mobilizer_parser.parse_args()
        name = data["name"]
        username = data["username"]
        password = Mobilizer.hash_pwd(data["password"])
        coordinator_id = data["coordinator"]
        coordinator = Coordinator.query.filter(Coordinator.coordinator_id==coordinator_id).first()
        mobilizer = Mobilizer(name, username, email, phone, password, coordinator_id)
        db.session.add(mobilizer)
        db.session.commit()
        mobilizer = Mobilizer.query.filter(Mobilizer.username == username).first()
        coordinator.mobilizers.append(mobilizer)
        return {"Message":"Mobilizer Registered"}

class ChangePasswordMobilizer(Resource):
    def post(self):
        data = password_parser.parse_args()
        mobilizer_id = data["mobilizer_id"]
        new_password = data["password"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        mobilizer.password = Mobilizer.generate_hash(password)
        db.session.commit()

class RegisterMobilizee(Resource):
    def post(self):
        data = register_mobilizer_parser.parse_args()
        fname = data["fname"]
        lname = data["lname"]
        email = data["email"]
        phone = data["phone"]
        address = data["address"]
        mobilizee = Mobilizee(lname, fname, email, phone, address)
        db.session.add(mobilizee)
        db.session.commit()
        return {"Message": "Mobilizee Registered"}

class MassRegistration(Resource):
    def post(self):
        file = request.files['mobilizee_input']
        df = pd.read_csv(file)
        for index,row in df.iterrows():
            mobilizee = Mobilizee(row["lname"], row["fname"], row["email"], row["phone"]. row["address"])
            db.session.add(mobilizee)
        db.session.commit()
        return {"Message": "Mobilizees Registered"}

class RemoveMobilizer(Resource):
    def post(self):
        data = removal_parser.parse_args()
        mobilizer_id = data["mobilizer_id"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        mobilizer.coordinator.uncategorized_mobilizees.extend(mobilizer.mobilizees)
        db.session.delete(mobilizer)
        db.session.commit()
        return {"Message": "Mobilizer Removed"}

class RemoveMobilizee(Resource):
    def post(self):
        data= remove_mobilizee_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        mobilizer_id = data["mobilizer_id"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        mobilizee = Mobilizee.query.filter(Mobilizee.mobilizee_id==mobilizee_id).first()
        mobilizer.mobilizees.remove(mobilizee)
        mobilizer.coordinator.uncategorized_mobilizees.append(mobilizee)
        return {"Message": "Mobilizee removed"}

class DeleteMobilizee(Resource):
    def post(self):
        data = delete_mobilizee_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        mobilizee = Mobilizee.query.filter(Mobilizee.mobilizee_id==mobilizee_id).first()
        db.session.delete(mobilizee)
        db.commit()
        return {"Message": "Mobilizee deleted"}

class Login(Resource):
    def post(self):
        data = user_parser.parse_args()
        username = data["username"]
        mobilizer = Mobilizer.query.filter(Mobilizer.username==username).first()
        coordinator = Coordinator.query.filter(Coordinator.username==username).first()
        if(mobilizer):
            if(Mobilizer.verify_hash(data["password"], mobilizer.password)):
                session['mobilizer_id'] = mobilizer.mobilizer_id
                return {
                    'message': 'Logged in as {}'.format(mobilizer.username),
                    'user_type': '{}'.format(type(mobilizer).__name__),
                    'id': '{}'.format(mobilizer.mobilizer_id)
                }
            else:
                return {'err': 'Username or password not recognized'}
        elif(coordinator):
            if (Coordinator.verify_hash(data["password"], coordinator.password)):
                session['coordinator_id'] = coordinator.coordinator_id
                return {
                    'message': 'Logged in as {}'.format(coordinator.username),
                    'user_type': '{}'.format(type(coordinator).__name__),
                    'id': '{}'.format(coordinator.coordinator_id)
                }
            else:
                return {'err': 'Username or password not recognized'}
