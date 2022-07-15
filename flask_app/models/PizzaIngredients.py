from flask_app.config.mysqlconnection import connectToMySQL
from flask import Request, flash
from datetime import date, datetime
from flask import Flask, render_template, session, redirect, flash, request
from flask_app.models.Ingredient import Ingredient


class PizzaIngredients:
    db = 'PizzaF'
    def __init__(self, data):
        self.RowID = data['RowID']
        self.CombinationID = data['CombinationID']
        self.Pi_IngredientID = data['Pi_IngredientID']
        self.CreatedAt = data['CreatedAt']
        self.UpdatedAt = data['UpdatedAt']
        self.IQty = data['IQty']
        

    @classmethod
    def SaveArrayOfIngredients(cls, data, quantities):
        comboid = PizzaIngredients.getNextComboid();
        indgs = Ingredient.getAll();
        ind_names = []
        check = False
        for i in indgs:
            ind_names.append(i.Name);
        for i in range(0, len(data)):
            if((data[i].Name in indgs) or (data[i].Name in ind_names)):
                temp = {"Name": data[i].Name}
                ind = Ingredient.getOneByName(temp)
                temp = {"Pi_IngredientID": ind.Pi_IngredientID,
                        "IQty": quantities[i],
                        "CombinationID":comboid}
                PizzaIngredients.save(temp)
                check = True
            elif((data[i] in indgs)):
                temp = {"Name": data[i]}
                ind = Ingredient.getOneByName(temp)
                temp = {"Pi_IngredientID": ind.Pi_IngredientID,
                        "IQty": quantities[i],
                        "CombinationID":comboid}
                PizzaIngredients.save(temp)
                check = True
        return check

    @classmethod
    def SaveArrayOfIngredientsByRequest(cls):
        comboid = PizzaIngredients.getNextComboid();
        indgs = Ingredient.getAll();
        ind_names = []
        request_indg = request.form.getlist('ingredients[]')
        ingredientsQty = request.form.getlist('ingredientsQty[]')
        for i in indgs:
            ind_names.append(i.Name);
        for i in range(0, len(request_indg)):
            if((request_indg[i] in indgs) or (request_indg[i] in ind_names)):
                temp = {"Name": request_indg[i]}
                request.form.getlist('ingredients[]')
                ind = Ingredient.getOneByName(temp)
                temp = {"Pi_IngredientID": ind.Pi_IngredientID,
                        "IQty": ingredientsQty[i],
                        "CombinationID":comboid}
                PizzaIngredients.save(temp)
                
    
    @classmethod
    def getAll(cls):
        query = "SELECT * FROM PizzaIngredients;"
        results = connectToMySQL(cls.db).query_db(query)
        PizzaIngredients = []
        for row in results:
            PizzaIngredients.append(cls(row))
        return PizzaIngredients
    
    @classmethod
    def getAllbyIngredientsByComboID(cls, data):
        query = "SELECT Pi_IngredientID FROM PizzaIngredients WHERE CombinationID = %(CombinationID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        ing = []
        if len(results) < 1:
            return False
        for row in results:
            temp ={"IngredientID": row.Pi_IngredientID}
            temp2 = Ingredient.getOne(temp)
            ing.append(temp2)
        return ing
    
    @classmethod
    def getAllbyIngredientsByComboIDToDescription(cls, data):
        inds = PizzaIngredients().getAllbyIngredientsByComboID(data)
        stre ="["
        for i in range(0, len(inds)-1):
            stre += (i+", ")
        stre += inds[len(inds)-1] + "]"
        return stre
    
    @classmethod
    def getNextComboid(cls):
        query = "Select CASE WHEN Max(CombinationID) is null THEN 1 ELSE Max(CombinationID)+1 END from PizzaIngredients"
        #query = "Select CASE WHEN Max(CombinationID)+1 is null then 1 end from PizzaIngredients"
        results = connectToMySQL(cls.db).query_db(query)
        #print("\tresults: ", results[0]['CASE WHEN Max(CombinationID) is null THEN 1 ELSE Max(CombinationID)+1 END'])
        results = results[0]['CASE WHEN Max(CombinationID) is null THEN 1 ELSE Max(CombinationID)+1 END']
        results = int(results)
        return results
        
    def PrintInfo(cls):
        s = f'{cls.CombinationID} '
        s+= f'{cls.Pi_IngredientID} '
        s+= f'{cls.CreatedAt} '
        s+= f'{cls.UpdatedAt} '
        return s

    @classmethod
    def getOne(cls, data):
        query = "SELECT * FROM PizzaIngredients WHERE CombinationID = %(CombinationID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getOneByPi_IngredientID(cls, data):
        query = "SELECT * FROM PizzaIngredients WHERE Pi_IngredientID = %(Pi_IngredientID)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO PizzaIngredients (Pi_IngredientID, CombinationID, IQty) VALUES (%(Pi_IngredientID)s, %(CombinationID)s, %(IQty)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE PizzaIngredients SET Pi_IngredientID=%(Pi_IngredientID)s  WHERE CombinationID = %(CombinationID)s and Pi_IngredientID = %(Pi_IngredientID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM PizzaIngredients WHERE CombinationID = %(CombinationID)s;"
        return connectToMySQL(cls.db).query_db(query, data)

