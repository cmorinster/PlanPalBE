import os
import base64
from datetime import datetime, timedelta
from app import db
#from werkzeug.security import generate_password_hash, check_password_hash


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creatorname = db.Column(db.String(150), nullable=False)
    creatoremail = db.Column(db.String(150), nullable=False)
    eventname = db.Column(db.String(150), nullable=False)
    polldescription = db.Column(db.String(500), nullable=True)
    shareresults = db.Column(db.Boolean, nullable=False, default=False)
    eventdate = db.Column(db.DateTime,nullable=True)
   # eventhash = db.Column(db.String(150), nullable=True)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   # dateexpiration = db.Column(db.DateTime)
    invitees = db.relationship('Invitees', backref='event', lazy=True)
    questions = db.relationship('Questions', backref='poll', lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|{self.creatorname}>"

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'creatorname': self.creatorname,
            'creatoremail': self.creatoremail,
            'eventname' : self.eventname,
            'polldescription': self.polldescription,
            'shareresults': self.shareresults,
            #'eventhash': self.eventhash,
            'datecreated': self.datecreated, 
            #'dateexpiration': self.dateexpiration,
            'invitees': self.invitees,
            'questions': self.questions

            
        }

    # def get_token(self, expires_in=1200):
    #     now = datetime.utcnow()
    #     if self.token and self.token_expiration > now + timedelta(minutes=1):
    #         return self.token
    #     self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    #     self.token_expiration = now + timedelta(seconds=expires_in)
    #     db.session.commit()
    #     return self.token

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # def update(self, data):
    #     for field in data:
    #         if field not in {'creatorname', 'creatoremail', 'password', 'is_admin'}:
    #             continue
    #         if field == 'password':
    #             setattr(self, field, generate_password_hash(data[field]))
    #         else:
    #             setattr(self, field, data[field])
    #     db.session.commit()


class Invitees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inviteename= db.Column(db.String(150), nullable= False)
    inviteeemail= db.Column(db.String(150), nullable= False)
    event_id= db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    answers = db.relationship('PollAnswers', backref='answerer')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Character {self.id}|{self.name}>"

    
    def to_dict(self):   
        return{
            'id': self.id,
            'inviteename': self.inviteename,
            'inviteeemail': self.inviteeemail
        }

        

    # def update(self, data):
    #     for field in data:
    #         if field not in {'id', 'type', 'strength', 'agility', 'intellegence', 'speed', 'endurance', 'camoflague', 'health', 'description', 'link', 'wins', 'champion' }:
    #             continue
    #         setattr(self, field, data[field])
    #     db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questiondate= db.Column(db.String(150), nullable= False)
    questiontime= db.Column(db.String(150), nullable= False)
    event_id= db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    answers = db.relationship('PollAnswers', backref='question')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Character {self.id}|{self.name}>"

    
    def to_dict(self):   
        return{
            'id': self.id,
            'questiondate': self.questiondate,
            'questiontime': self.questiontime
        
        }

        

    # def update(self, data):
    #     for field in data:
    #         if field not in {'id', 'type', 'strength', 'agility', 'intellegence', 'speed', 'endurance', 'camoflague', 'health', 'description', 'link', 'wins', 'champion' }:
    #             continue
    #         setattr(self, field, data[field])
    #     db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class PollAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer= db.Column(db.Boolean, nullable= False)
    questions_id= db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    invitees_id= db.Column(db.Integer, db.ForeignKey('invitees.id'), nullable=False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Answer {self.id}|{self.answer}>"

    
    def to_dict(self):   
        return{
            'id': self.id,
            'answer': self.answer,
            'question': Questions.query.get(self.id).to_dict(),
            'answerer': Invitees.query.get(self.id).to_dict()
        }

        



    def delete(self):
        db.session.delete(self)
        db.session.commit()