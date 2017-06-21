class User():
    def __init__(self,name,email,password, active = True):
        self.name = name
        self.email = email
        self.password = password
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
        c = g.db.execute("""INSERT INTO users(username,email,password)
                                    VALUES(?,?,?)""",[self.name,self.email,self.password])
        g.db.commit()
