"""
__authors__     = Yash, Will, Peter
__description__ = Class definition of the User object as defined as those
to be stored in the User DB (users table)
__name__        = user.py
"""

from flask import g
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, userid, name, email, active=True):
        self.userid = userid
        self.name   = name
        self.email  = email
        self.active = active

    def is_authenticated(self):
        #return true if user is authenticated, provided credentials
        return True

    def is_active(self):
        #return true if user is activte and authenticated
        return self.active

    def is_annonymous(self):
        #return true if annon, actual user return false
        return False
        
    def get_id(self):
        #return unicode id for user, and used to load user from user_loader callback
        return self.userid

    def __str__(self):
        return """
        self.userid = {}
        self.name   = {}
        self.email  = {}
        """.format(self.userid, self.name, self.email)