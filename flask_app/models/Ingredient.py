from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date, datetime

class Ingredient:
    db = 'PizzaF'
    def __init__(self, data):
        self.IngredientID = data['IngredientID']
        self.Name = data['Name']
        self.Type = data['Type']
        self.baseprice = data['baseprice']
        self.Description = data['Description']
        self.CreatedAt = data['CreatedAt']
        self.UpdatedAt = data['UpdatedAt']


    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM Ingredient;"
        results = connectToMySQL(cls.db).query_db(query)
        Ingredient = []
        for row in results:
            Ingredient.append(cls(row))
        return Ingredient
    
    def PrintInfo(cls):
        s = f'{cls.IngredientID} '
        s+= f'{cls.Name} '
        s+= f'{cls.Type} '
        s+= f'{cls.baseprice} '
        s+= f'{cls.Description} '
        s+= f'{cls.CreatedAt} '
        s+= f'{cls.UpdatedAt} '
        return s

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM Ingredient WHERE IngredientID = %(IngredientID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getOneByName(cls, data):
        query = "SELECT * FROM Ingredient WHERE Name = %(Name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO Ingredient (Name, Type, baseprice, Description) VALUES (%(Name)s, %(Type)s, %(baseprice)s, %(Description)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE Ingredient SET Name=%(Name)s,  Type=%(Type)s, baseprice=%(baseprice)s, Description=%(Description)s WHERE IngredientID = %(IngredientID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM Ingredient WHERE IngredientID = %(IngredientID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

