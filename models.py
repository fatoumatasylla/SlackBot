#import os
from config import DATABASE_URL
from app import app 
from datetime import datetime
import random

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, func, PrimaryKeyConstraint,text
from sqlalchemy import Table, Text,MetaData
from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.schema import Table
from sqlalchemy.event import listen
from flask_migrate import Migrate
from offylist import offyusers
from functions import sc
from attachements import offyvalues
#create database

db_name = DATABASE_URL
engine = create_engine(db_name) 


#metadata = MetaData()
Base = declarative_base()

migrate = Migrate(app, Base)
#connection = engine.connect()
#trans = connection.begin()

Session = sessionmaker(bind=engine, expire_on_commit=False)
#expire_on_commit=False
session= Session()

class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True)
    slack_id =  Column(String(10), index=True)
    real_name = Column(String(40), index=True)  
    slack_name = Column(String(40), index=True)  
    last_activity = Column(DateTime, default=func.now(),index=True)
    job = Column(String(255), default= None )
    last_match = Column(String(255), default= None)

    cause = relationship('Cause', secondary='user_cause')
    #,cascade="save-update,delete" lazy='joined'
    
    def __init__(self, slack_id, real_name, slack_name, last_activity, job=None,last_match =None):
        self.slack_id = slack_id
        self.real_name = real_name
        self.job = job
        self.last_activity = last_activity
        self.last_match = last_match
        if slack_name is None:
            self.slack_name = real_name
        else:
            self.slack_name = slack_name 
    def __repr__(self):
        return f"User(slack_id:'{self.slack_id}', real_name:'{self.real_name}' ,slack_name: '{self.slack_name}', last_activity:'{self.last_activity}', job:'{self.job}',last_match'{self.last_match})"
        
class Cause(Base):
    __tablename__ = 'causes'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    user = relationship('User', secondary='user_cause')
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"Cause(name='{self.name}')"

class UserCause(Base):
    __tablename__ = 'user_cause' 
    user_id = Column(Integer, ForeignKey('users.id'), primary_key = True)
    cause_id = Column(Integer, ForeignKey('causes.id'), primary_key = True)



class Planning(Base):
    __tablename__ = "planning"
    id = Column(Integer, primary_key = True)
    day = Column(DateTime, default=func.now(), index=True)
    value = Column(String(255))
    def __init__(self,value,day =func.now() ):
        self.value = value;
        sel.day = day
def comit():
    try:
        session.flush()
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
def add_bdd(obj):
    session.add(obj)
    try:
        session.flush()
        session.expire_on_commit=True
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def add_multiple(list_obj):
    session.add_all(list_obj)
    try:
        session.flush()
        session.expire_on_commit=True
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()

def delete_bdd(obj):
    try:
        session.delete(obj)
    except:
        session.rollback()
    finally:
        session.close()

def add_user_causes(slack_id,list_id_cause):
    user = session.query(User).filter(User.slack_id == slack_id)

    for c in range(1,len(list_id_cause)):
        c_id = session.query(Cause).filter(Cause.id == list_id_cause[c])
        user.cause.append(c_id)
def  add_user_cause(slack_id,id_cause):
    user = session.query(User).filter(User.slack_id == slack_id)
    cause = session.query(Cause).filter(Cause.id == id_cause)
    user.cause.append(cause)


def query_users(user_dict_info):
    u = user_dict_info
    user = session.query(User).filter(User.slack_id == u.slack_id).first()
    if user == None:
        add_bdd(u)
        mes = "non"
    else:
        mes = "oui"
    return mes
def users():
    query = session.query(User).all()
    for u in query:
        print(u)
           
def verif_user(id):
    """ recherche si l'user est unique """
    #query = session.query(func.count(User.slack_id).filter(User.slack_id == id))

    query = session.query(User).filter(User.slack_id == id).all()
    for u in query:
        print(u)


def update_cause(slack_id,list_cause):
    print("hello")
    #remove all user cause dans add new list of cause `
    # # s cause if from user_cause w user = ( s userid f user w u.slackid = slack id)
    #for c in cause add_usser_cause()
    #query = query(User).filter(Cause.id_user == "user.id_user")

def update_arg(user,Table,element,newvalue):
    """update last match , last activity , """
    query = session.query(Table).filter(Table.slack_id == user.slack_id)
    query.update({Table.element : newvalue})
    comit()

def update_user_info(slack_id,element,newvalue):
    """update last match , last activity , """
    session.query(User).filter(User.slack_id == slack_id).\
            update({User.element : newvalue})
    comit()
            
   #to update for week update

def search_user_value(user_id):
    causes = session.query(UserCause).filter(text(user_id = user_id)).all()
    print("hello")

def match(slack_id, list_causes):
    print("hello")
    #list_causes is
    #s random lim 1O 
    # if last match == none get n import et up 
    # update last match with user id
    #subquery = session.query(UserCause).filter(UserCause.cause_id.in_(list_causes).\
    #   count(UserCause.cause_id).group_by(UserCause.user_id).order_by()

    #search user 
    user = session.query(User).filter(User.slack_id == slack_id)
    id = user.id
    query = session.query(User).\
        filter(text(id+" NOT IN (SELECT count(cause_id) AS nbCauses FROM user_cause WHERE cause_id IN ("+list_causes+") GROUP BY user_id ORDER BY nbcauses DESC LIMIT 3) ORDER BY last_activity DESC LIMIT 10"))
    #query = session.query(User).filter(User.id.notin_(subquery), )
    match = random.choice(query)
    update_user_info(slack_id,"last_match",match.slack_id)
    #seéarch match value 
    causes = session.query(UserCause).filter(text(user_id = match.id)).all()
    #list User_causes
    for c in causes:
        if len(causes) == 1:
            message = "hello,\n@"+match.real_name+" avez "+offyvalues[c.cause_id]+"cette cause en commun "
        
        else:
            message = "hello,\n@"+match.real_name+ " partagez ces causes:\n"
            for i in range(len(causes)):
                message = message + "\n"+offyvalues[c.cause_id] 

    return message


def init_bdd():
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #c1 = Cause("DÉVELOPPER LE VIETNAM")
    #c2 = Cause("LA MONDIALISATION POSITIVE")
    #c3 = Cause("CRÉER DE LA VALEUR PARTAGÉE")
    #c4 = Cause("PENSER ET AGIR DURABLE")
    #c5 = Cause("PARTAGER LE SAVOIR")

    #session.add_all([c1,c2,c3,c4,c5])



    #session.add_all([u1,u2,u3,u4,u5])

    u = session.query(User).filter(User.id == 1).all()
    c = session.query(Cause).filter(User.id == 1)
    #import pdb; pdb.set_trace()

    for user in u:
        print ( "id:"+u.slack_id )
    
   # session.add(UserCause(u.id, c.id,1))
    #u1.cause.append(c1)

    try:
        session.flush()
        session.expire_on_commit=True
        session.commit()
        print("EVERYTHING IN GIRL")
    except:
        session.rollback()
        print("EXEPTION BITCH")
    finally:
        session.close()
        print("CLOSE BITCH")

    for user in u:
        print ( "id:"+u.slack_id )

    #u1.cause.append(c4)

 