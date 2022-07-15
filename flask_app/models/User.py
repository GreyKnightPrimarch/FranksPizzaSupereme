from ast import Try
from warnings import catch_warnings
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

class User:
    db = 'PizzaF'
    def __init__(self, data):
        self.ID = data['ID']
        self.FirstName = data['FirstName']
        self.LastName = data['LastName']
        self.Email = data['Email']
        self.Address = data['Address']
        self.City = data['City']
        self.State = data['State']
        self.ZIP = data['ZIP']
        self.PassWordHash = data['PassWordHash']
        self.CreatedAt = data['CreatedAt']
        self.UpdateAt = data['UpdatedAt']
    
    @classmethod
    def fromUser(self, data):
        self.ID = data.ID
        self.FirstName = data.FirstName
        self.LastName = data.LastName
        self.Address = data.Address
        self.City = data.City
        self.State = data.State
        self.ZIP = data.ZIP
        self.Email = data.Email
        self.PassWordHash = data.PassWordHash
        self.CreatedAt = data.CreatedAt
        self.UpdateAt = data.UpdateAt

    def fullName(self):
        return f'{self.FirstName} {self.LastName}'
    
    @staticmethod
    def validateRegister(user):
        isValid = True
        query = 'SELECT * FROM user WHERE Email = %(Email)s;'
        
        results = connectToMySQL(User.db).query_db(query, user)
        print(results)
        if (results==False):
            t = 1 
        elif len(results) >= 1:
            isValid = False
            flash("That Email is already in our database")
        
        if not EMAIL_REGEX.match(user['Email']):
            isValid = False
            flash("Invalid Email format")
        if len(user['FirstName']) < 2:
            isValid = False
            flash('Please use at least 2 characters for the first name')
            flash('Please use at least 2 characters for the first name')
        if len(user['LastName']) < 2:
            isValid = False
            flash('Please use at least 2 characters for the last name')
        if len(user['State']) != 2:
            isValid = False
            flash('State must be two letter State code i.e. Califonia: CA')
        if len(user['City']) < 3:
            isValid = False
            flash('City name must be at least 3 characters')
        if len(user['ZIP']) != 5:
            isValid = False
            flash('ZIP must be 5 characters')
        if len(user['Password']) < 8:
            isValid = False
            flash('PassWordHash must be at least 8 characters long')
        if user['Password'] != user['PasswordConfirm']:
            isValid = False
            flash('Passwords do not match')
        return isValid
    
    @staticmethod
    def validateLogin(user):
        isValid = True
        query = 'SELECT * FROM user WHERE Email = %(Email)s;'
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) < 1:
            isValid = False
            flash("No such email registered")
        else:
            results = User(results[0])
        if not EMAIL_REGEX.match(user['Email']):
            isValid = False
            flash("Invalid Email format")
        print("results:",results)
        check = bcrypt.check_password_hash(results.PassWordHash, user['Password'])
        if(not(check)):
            flash("Invalid Password")
        return isValid

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM user;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM user WHERE ID = %(ID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getEmail(cls, data):
        query = "SELECT * FROM user WHERE Email = %(Email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        try:
            query = 'INSERT INTO user (FirstName, LastName, Address, City, State, ZIP, Email, PassWordHash) VALUES (%(FirstName)s, %(LastName)s, %(Address)s, %(City)s, %(State)s, %(ZIP)s, %(Email)s, %(Password)s);'
            return connectToMySQL(cls.db).query_db(query, data)
        except:
            print("save: Something else went wrong") 

    @classmethod
    def updateByID(cls, data):
        try:
            query = "UPDATE user SET FirstName=%(FirstName)s,  LastName=%(LastName)s, Address=%(Address)s, City=%(City)s, Address=%(State)s, City=%(ZIP)s, Email=%(Email)s, Password=%(Password)s WHERE ID = %(ID)s;"
            return connectToMySQL(cls.db).query_db(query, data)
        except:
            print("updateByID: Something else went wrong") 

        
    @classmethod
    def update(cls, data):
        pass

    @classmethod
    def delete(cls, data):
        pass