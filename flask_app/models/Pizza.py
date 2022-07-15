from ast import Try
from warnings import catch_warnings
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.Ingredient import Ingredient
from flask_app.models.PizzaIngredients import PizzaIngredients

class Pizza:
    db = 'PizzaF'
    def __init__(self, data):
        self.PizzaID = data['PizzaID']
        self.Name = data['Name']
        self.Crust_ID = data['Crust_ID']
        self.Size_ID = data['Size_ID']
        self.Pi_CombinationID = data['Pi_CombinationID']
        self.Description = data['Description']
        self.CreatedAt = data['CreatedAt']
        self.UpdateAt = data['UpdatedAt']

    
    @classmethod
    def fromUser(self, data):
        self.PizzaID = data.PizzaID
        self.Name = data.Name
        self.Crust_ID = data.Crust_ID
        self.Size_ID = data.Size_ID
        self.Pi_CombinationID = data.Pi_CombinationID
        self.Description = data.Description
        self.CreatedAt = data.CreatedAt
        self.UpdateAt = data.UpdateAt


    def fullName(self):
        return f'{self.Crust_ID} {self.Size_ID}'
    
    @staticmethod
    def validateRegister(Pizza):
        isValid = True
        query = 'SELECT * FROM Pizza WHERE Name = %(Name)s;'
        results = connectToMySQL(Pizza.db).query_db(query, Pizza)
        if (results!=False):
            isValid = False
            flash("That Name is already in our database")
        if len(Pizza['Name']) < 2:
            isValid = False
            flash('Please use at least 3 characters for the Name')
        if len(Pizza['Description']) != 2:
            isValid = False
            flash('State must be two letter State code i.e. Califonia: CA')
        return isValid
    

    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM Pizza;'
        results = connectToMySQL(cls.db).query_db(query)
        Pizzas = []
        for row in results:
            Pizzas.append(cls(row))
        return Pizzas

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM Pizza WHERE PizzaID = %(PizzaID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getFristOnebyComboID(cls, data):
        query = "SELECT * FROM Pizza WHERE Pi_CombinationID = %(Pi_CombinationID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getAllbyComboID(cls, data):
        query = "SELECT * FROM Pizza WHERE Pi_CombinationID = %(Pi_CombinationID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        Pizzas = []
        for row in results:
            Pizzas.append(cls(row))
        return Pizzas

    @classmethod
    def getFristOnebyCrust_ID(cls, data):
        query = "SELECT * FROM Pizza WHERE Crust_ID = %(Crust_ID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getAllbyCrust_ID(cls, data):
        query = "SELECT * FROM Pizza WHERE Crust_ID = %(Crust_ID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        Pizzas = []
        for row in results:
            Pizzas.append(cls(row))
        return Pizzas

    @classmethod
    def getFristOnebySize_ID(cls, data):
        query = "SELECT * FROM Pizza WHERE Size_ID = %(Size_ID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getAllbySize_ID(cls, data):
        query = "SELECT * FROM Pizza WHERE Size_ID = %(Size_ID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        Pizzas = []
        for row in results:
            Pizzas.append(cls(row))
        return Pizzas

    @classmethod
    def getAllbyName(cls, data):
        query = "SELECT * FROM Pizza WHERE Name = %(Name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        Pizzas = []
        for row in results:
            Pizzas.append(cls(row))
        return Pizzas
    
    @classmethod
    def getFristOnebyName(cls, data):
        query = "SELECT * FROM Pizza WHERE Name = %(Name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save(cls, data):
        try:
            query = 'INSERT INTO Pizza (Crust_ID, Size_ID, Pi_CombinationID, Name, Description) VALUES (%(Crust_ID)s, %(Size_ID)s, %(Pi_CombinationID)s, %(Name)s, %(Description)s);'
            return connectToMySQL(cls.db).query_db(query, data)
        except:
            print("Something else went wrong") 

        
    @classmethod
    def update(cls, data):
        query = "UPDATE Pizza SET Crust_ID=%(Crust_ID)s,  Size_ID=%(Size_ID)s, Pi_CombinationID=%(Pi_CombinationID)s, Description=%(Description)s, Name=%(Name)s WHERE PizzaID = %(PizzaID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        pass