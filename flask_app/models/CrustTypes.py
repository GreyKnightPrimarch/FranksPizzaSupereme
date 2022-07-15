from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date, datetime


class CrustTypes:
    db = 'PizzaF'
    def __init__(self, data):
        self.CrustID = data['CrustID']
        self.Name = data['Name']
        self.Type = data['Type']
        self.baseprice = data['baseprice']
        self.Description = data['Description']
        self.CreatedAt = data['CreatedAt']
        self.UpdatedAt = data['UpdatedAt']


    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM CrustTypes;"
        results = connectToMySQL(cls.db).query_db(query)
        CrustTypes = []
        for row in results:
            CrustTypes.append(cls(row))
        return CrustTypes
    
    @staticmethod
    def convertToJson(data):
        temp = CrustTypes(data)
        vart = {
            "CrustID": temp.CrustID,
            "Name": temp.Name,
            "Type": temp.Type,
            "baseprice": temp.baseprice,
            "Description": temp.Description,
            "CreatedAt": temp.CreatedAt,
            "UpdatedAt": temp.UpdatedAt
                }
        return vart
    
    def PrintInfo(cls):
        s = f'{cls.CrustID} '
        s+= f'{cls.Name} '
        s+= f'{cls.Type} '
        s+= f'{cls.baseprice} '
        s+= f'{cls.Description} '
        s+= f'{cls.CreatedAt} '
        s+= f'{cls.UpdatedAt} '
        return s

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM CrustTypes WHERE CrustID = %(CrustID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getOneByName(cls, data):
        query = "SELECT * FROM CrustTypes WHERE Name = %(Name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO CrustTypes (Name, Type, baseprice, Description) VALUES (%(Name)s, %(Type)s, %(baseprice)s, %(Description)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE CrustTypes SET Name=%(Name)s,  Type=%(Type)s, baseprice=%(baseprice)s, Description=%(Description)s WHERE CrustID = %(CrustID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM CrustTypes WHERE CrustID = %(CrustID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

