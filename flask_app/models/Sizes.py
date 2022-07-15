from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date, datetime


class Sizes:
    db = 'PizzaF'
    def __init__(self, data):
        self.SizeID = data['SizeID']
        self.Name = data['Name']
        self.Diameter = data['Diameter']
        self.Description = data['Description']
        self.CreatedAt = data['CreatedAt']
        self.UpdatedAt = data['UpdatedAt']
        self.Multiplier = data['Multiplier']


    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM Sizes;"
        results = connectToMySQL(cls.db).query_db(query)
        Sizes = []
        for row in results:
            Sizes.append(cls(row))
        return Sizes
    
    def PrintInfo(cls):
        s = f'{cls.SizeID} '
        s+= f'{cls.Name} '
        s+= f'{cls.Diameter} '
        s+= f'{cls.Description} '
        s+= f'{cls.CreatedAt} '
        s+= f'{cls.UpdatedAt} '
        s+= f'{cls.Mulitplier} '
        return s

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM Sizes WHERE SizeID = %(SizeID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getOneByName(cls, data):
        query = "SELECT * FROM Sizes WHERE Name = %(Name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO Sizes (Name, Diameter, Description) VALUES (%(Name)s, %(Diameter)s, %(Description)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE Sizes SET Name=%(Name)s, Diameter=%(Diameter)s, Description=%(Description)s WHERE SizeID = %(SizeID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM Sizes WHERE SizeID = %(SizeID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

