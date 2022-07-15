from numpy import array
from flask_app import app
from flask import Flask, render_template, session, redirect, flash, request
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt

class UserFavedPizzas:
    
    db = 'PizzaF'
    
    def __init__(self, data):
        self.PizzaID = data['PizzaID']
        self.Description = data['Description']
        self.Crust_ID = data['Crust_ID']
        self.Size_ID = data['Size_ID']
        self.Name = data['Name']
        self.Pi_CombinationID = data['Pi_CombinationID']
        self.LikeID = data['LikeID']
        self.Pizza_Id = data['Pizza_Id']
        self.User_ID = data['User_ID']
        self.active = data['active']

    
    @classmethod
    def obtainAllPizzasWithUserfavorties(cls,data,bool=True):
        #bool is meant to represent if the favorite pizza is an current (Active) pizza favortie or not. 1 = true/yes, 0 = false,no
        if(bool):
            bool = 1
        elif(bool==False):
            bool = 0
        else:
            try:
                bool = int(bool)
            except:
                bool = 1
        data['active']=bool
        #query = "Select * from pizza left join ( select * from favoritepizza where User_ID = %(ID)s and active = %(active)s) as sub on pizza.PizzaID = sub.Pizza_ID"
        query = "Select * from pizza left join ( select Pizza_Id, LikeID, User_ID, active from favoritepizzas where User_ID = %(ID)s and active = %(active)s) as sub on pizza.PizzaID = sub.Pizza_ID"
        results = connectToMySQL(cls.db).query_db(query, data)
        daPizzas = []
        for row in results:
            daPizzas.append(cls(row))
        return daPizzas
    
    @classmethod
    def convertToDict(cls):
        data ={
            "PizzaID": cls.PizzaID,
            "Description": cls.Description,
            "Crust_ID": cls.Crust_ID,
            "Size_ID": cls.Size_ID,
            "Name": cls.Name,
            "Pi_CombinationID": cls.Pi_CombinationID,
            "LikeID": cls.LikeID,
            "Pizza_Id": cls.Pizza_Id,
            "User_ID": cls.User_ID,
            "active": cls.active,
        }
        return data
        
