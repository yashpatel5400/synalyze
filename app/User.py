"""
__authors__     = Yash, Will, Peter
__description__ = Class definition of the User object as defined as those
to be stored in the User DB (users table)
__name__        = User.py
"""
from flask import g

class User():
    def __init__(self, userid, name, email, active=True):
        self.userid = userid
        self.name   = name
        self.email  = email
        self.active = active

    def is_authenticated():
        #return true if user is authenticated, provided credentials
        return True

    def is_active():
        #return true if user is activte and authenticated
        return self.active

    def is_annonymous():
        #return true if annon, actual user return false
        return False
        
    def get_id():
        #return unicode id for user, and used to load user from user_loader callback
        return str(self.id)

    def add(self):
        c = g.db.execute("""INSERT INTO users(userid, name, email) 
            VALUES(?,?,?)""",[self.userid, self.name, self.email])
        g.db.commit()
