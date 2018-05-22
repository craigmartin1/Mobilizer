from flask import session, jsonify
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import re

from Models.models import Mobilizee, Mobilizer, Coordinator, Note, Request


db = SQLAlchemy()

note_parser = reqparse.RequestParser()
note_parser.add_argument('mobilizee_id', help='This field cannot be blank', required=True)
note_parser.add_argument('note', help='This field cannot be blank', required=True)

removal_parser = reqparse.RequestParser()
removal_parser.add_argument('mobilizer_id', help='This field cannot be blank', required=True)

mobilizer_removal_parser = reqparse.RequestParser()
mobilizer_removal_parser.add_argument('mobilizer_id', help='This field cannot be blank', required=True)

remove_mobilizee_parser = reqparse.RequestParser()
remove_mobilizee_parser.add_argument('mobilizer_id', help='This field cannot be blank', required=True)
remove_mobilizee_parser.add_argument('mobilizee_id', help='This field cannot be blank', required=True)

delete_mobilizee_parser = reqparse.RequestParser()
delete_mobilizee_parser.add_argument('mobilizee_id', help='This field cannot be blank', required=True)

update_parser = reqparse.RequestParser()
update_parser.add_argument('mobilizee_id', help='This field cannot be blank', required=True)
update_parser.add_argument('email', help='This field can be blank', required=False)
update_parser.add_argument('phone', help='This field can be blank', required=False)
update_parser.add_argument('address', help='This field can be blank', required=False)

assign_parser = reqparse.RequestParser()
assign_parser.add_argument('mobilizer_id', help='This field cannot be blank', required=True)
assign_parser.add_argument('mobilizees', help='This field cannot be blank', required=True)

register_mobilizer_parser = reqparse.RequestParser()
register_mobilizer_parser.add_argument('name', help='This field cannot be blank', required=True)
register_mobilizer_parser.add_argument('username', help='This field cannot be blank', required=True)
register_mobilizer_parser.add_argument('password', help='This field cannot be blank', required=True)
register_mobilizer_parser.add_argument('email', help='This field cannot be blank', required=True)
register_mobilizer_parser.add_argument('phone', help='This field cannot be blank', required=True)

password_parser = reqparse.RequestParser()
password_parser.add_argument('password', help='This field cannot be blank', required=True)

register_mobilizee_parser = reqparse.RequestParser()
register_mobilizee_parser.add_argument('fname')
register_mobilizee_parser.add_argument('lname')
register_mobilizee_parser.add_argument('email')
register_mobilizee_parser.add_argument('phone')
register_mobilizee_parser.add_argument('address')

user_parser = reqparse.RequestParser()
user_parser.add_argument('username')
user_parser.add_argument('password')

class UnattachedMobilizees(Resource):
    pass

class SeeMobilizers(Resource):
    def get(self):
        coordinator_id = 1
        coordinator = Coordinator.query.filter(Coordinator.coordinator_id == coordinator_id).first()
        mobilizer_list = []
        for mobilizer in coordinator.mobilizers:
            mobilizer_dict = {}
            mobilizer_dict["id"] = mobilizer.mobilizer_id
            mobilizer_dict["name"] = mobilizer.username
            mobilizer_dict["phone"] = mobilizer.phone
            mobilizer_dict["email"] = mobilizer.email
            mobilizer_list.append(mobilizer_dict)
        return mobilizer_list
class SeeMobilizees(Resource):
    def get(self):
        mobilizer_id = 1
        #mobilizer_id = session['mobilizer_id']
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id == mobilizer_id).first()
        mobilizee_list = []
        for mobilizee in mobilizer.mobilizees:
            mobilizee_dict = {}
            mobilizee_dict["id"] = mobilizee.mobilizee_id
            mobilizee_dict['name'] = mobilizee.fname + " " + mobilizee.lname
            mobilizee_dict["phone"] = mobilizee.phone
            mobilizee_dict["email"] = mobilizee.email
            mobilizee_dict["address"] = mobilizee.address
            note_list = []
            for note in mobilizee.notes:
                note_list.append({"content": note.content})
            note_list.reverse()
            mobilizee_dict["notes"] = note_list
            mobilizee_list.append(mobilizee_dict)
        return mobilizee_list

class MakeNote(Resource):
    def post(self):
        data = note_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        note_content = data["note"]
        note = Note(mobilizee_id, note_content)
        mobilizee = db.session.query(Mobilizee).get(mobilizee_id)
        mobilizee.notes.append(note)
        db.session.commit()
        return {"Message": "Note appended"}

class RequestRemoval(Resource):
    def post(self):
        data = removal_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        mobilizer_id = session["mobilizer_id"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        request = Request(mobilizee_id, mobilizer.coordinator.coordinator_id)
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
        mobilizee = db.session.query(Mobilizee).get(mobilizee_id)
        if(email):
            mobilizee.email = email
        if(phone):
            mobilizee.phone = phone
        if(address):
            mobilizee.address = address
        db.session.commit()
        return {"Message": "Contact updated"}

class TestContact(Resource):
    def get(self):
        mobilizee = Mobilizee.query.filter(Mobilizee.mobilizee_id ==1).first()

        return {"email": mobilizee.email,
                "phone": mobilizee.phone,
                "address": mobilizee.address}

class AssignMobilizees(Resource):
    def post(self):
        # UPDATE DOESN'T PERSIST AFTER ASSIGNMENT?
        data = assign_parser.parse_args()
        mobilizer_id = data["mobilizer_id"]
        mobilizee_ids = data["mobilizees"]
        mobilizer = db.session.query(Mobilizer).get(mobilizer_id)
        mobilizees = db.session.query(Mobilizee).filter(Mobilizee.mobilizee_id.in_(mobilizee_ids)).all()
        mobilizer.mobilizees.extend(mobilizees)
        db.session.commit()
        return {"Message": "Mobilizees Registered"}

class RegisterMobilizer(Resource):
    def post(self):
        data = register_mobilizer_parser.parse_args()
        name = data["name"]
        username = data["username"]
        password = Mobilizer.generate_hash(data["password"])
        coordinator_id = session["coordinator_id"]
        email = data["email"]
        phone = data["phone"]
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
        mobilizer_id = session["mobilizer_id"]
        new_password = data["password"]
        mobilizer = Mobilizer.query.filter(Mobilizer.mobilizer_id==mobilizer_id).first()
        mobilizer.password = Mobilizer.generate_hash(new_password)
        db.session.commit()
        return {"Message": "Password Changed"}
    
class RegisterMobilizee(Resource):
    def post(self):
        data = register_mobilizee_parser.parse_args()
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
        db.session.query(Mobilizer).filter(Mobilizer.mobilizer_id==mobilizer_id).delete()
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

class TestMobilizee(Resource):
    def get(self):
        mobilizee = Mobilizee.query.filter(Mobilizee.mobilizee_id==1).first()
        return {"mobilizee": mobilizee.mobilizee_id}

class DeleteMobilizee(Resource):
    def post(self):
        data = delete_mobilizee_parser.parse_args()
        mobilizee_id = data["mobilizee_id"]
        db.session.query(Mobilizee).filter(Mobilizee.mobilizee_id == mobilizee_id).delete()
        db.session.commit()
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
