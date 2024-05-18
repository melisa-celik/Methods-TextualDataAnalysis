class User:
    def __init__(self, userID, name, email, password):
        self.userID = userID
        self.name = name
        self.email = email
        self.password = password

    def toDict(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }