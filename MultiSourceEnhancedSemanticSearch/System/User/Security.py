import os
import json
import hashlib
from MultiSourceEnhancedSemanticSearch.System.User.User import User

class UserAuthenticator:
    def __init__(self, dbFile="users.json"):
        self.dbFile = dbFile
        if not os.path.exists(self.dbFile):
            with open(self.dbFile, "w") as f:
                json.dump([], f)

    def hashPassword(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, userID, name, email, password):
        with open(self.dbFile, "r") as f:
            users = json.load(f)

        if any(user["userID"] == userID for user in users):
            raise ValueError("User ID already exists")

        hashedPassword = self.hashPassword(password)
        user = User(userID, name, email, hashedPassword)
        users.append(user.toDict())

        with open(self.dbFile, "w") as f:
            json.dump(users, f)

        return "User registered successfully"

    def login(self, userID, password):
        with open(self.dbFile, "r") as f:
            users = json.load(f)

        hashedPassword = self.hashPassword(password)
        for user in users:
            if user["userID"] == userID and user["password"] == hashedPassword:
                return "Login successful"

        return "Login failed: Invalid credentials"

    def getUsers(self):
        with open(self.dbFile, "r") as f:
            users = json.load(f)
        return users