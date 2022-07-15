from xml.etree.ElementTree import tostring
from flask_app import app
from flask import Flask, render_template, session, redirect, flash, request
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app.models.Sizes import Sizes
from flask_app.models.CrustTypes import CrustTypes
from flask_app.models.User import User
from flask_app.models.Pizza import Pizza
from flask_app.models.PizzaIngredients import PizzaIngredients
from flask_app.models.Ingredient import Ingredient
from flask_app.models.UserFavedPizzas import UserFavedPizzas

import json
bcrypt = Bcrypt(app)

class Shared:
    
    db = 'PizzaF'
    
    def __init__(self, data):
        self.ID = data['ID']
        self.FirstName = data['FirstName']
        self.LastName = data['LastName']
        self.Email = data['Email']
        self.PassWordHash = data['PassWordHash']
        self.UserCreatedAt = data['user.CreatedAt']
        self.UserUpdateAt = data['user.UpdatedAt']
        
        

    
    @staticmethod
    def userToDic(auser):
        temp = {
        'ID': auser.ID,
        'FirstName': auser.FirstName,
        'LastName': auser.LastName,
        'Email': auser.Email
        }
        return temp
    
    @staticmethod
    def sessionSave(auser):
            session['ID'] = auser.ID
            session['FirstName'] = auser.FirstName
            session['LastName'] = auser.LastName
            session['Email'] = auser.Email

            
    @staticmethod
    def Logout():
            session['ID'] = None
            session['BuyerID'] = None
            session['SellerID'] = None
            session['CarID'] = None
            session['FirstName'] = None
            session['LastName'] = None
            session['Email'] = None
            
    @staticmethod
    def saveNewUserFromSession():
        newUser = {
            'FirstName': request.form['FirstName'],
            'LastName': request.form['LastName'],
            'Address': request.form['Address'],
            'City': request.form['City'],
            'State': request.form['State'],
            'ZIP': request.form['ZIP'],
            'Email': request.form['Email'],
            'Password': bcrypt.generate_password_hash(request.form['Password'])
        }
        return newUser 
            
    @staticmethod
    def UserUpdateFromSession():
        newUser = {
            'ID': session['ID'],
            'FirstName': request.form['FirstName'],
            'LastName': request.form['LastName'],
            'Address': request.form['Address'],
            'City': request.form['City'],
            'State': request.form['State'],
            'ZIP': request.form['ZIP'],
            'Email': request.form['Email'],
            'Password': bcrypt.generate_password_hash(request.form['Password'])
        }
        return newUser 
            
    @staticmethod
    def getNextComboid():
        cmbid = PizzaIngredients.getNextComboid()
        return cmbid
    
    @staticmethod
    def isStringEmptyOrNull(s):
        l = len(s)
        if (not(s.strip()) or l==0):
            return True
        else:
            return False
        
    @staticmethod
    def stringToDictionary(s,char1="'", char2='"'):
        s = s.replace(char1, char2)
        #print("S: ",s)
        s = json.loads(s)
        return s
    
    @staticmethod
    def saveNewPizzaFromRequest():
        cmbid = PizzaIngredients.getNextComboid()
        #ingredientsQty = request.form['ingredientsQty[]']
        siz = request.form['Size']
        siz = Shared.stringToDictionary(siz)
        siz = Sizes.getOneByName(siz);
        #print("siz: ",siz)
        crs = request.form['Crust']
        crs = Shared.stringToDictionary(crs)
        crs = CrustTypes.getOneByName(crs);
        immutdict = request.values
        #print("ingredientsQtyRaw: ", immutdict['Steak'])
        #print("ingredientsQty1: ", ingredientsQty)
        arry = Shared.obtainArrayOfDictionariesOfPizzaIngredients(immutdict, cmbid)
        Shared.saveAnArrayOfIngredientsToPizzaIngreditents(arry)
        
        aPizza = {
        'Size_ID': siz.SizeID,
        'Crust_ID': crs.CrustID,
        'Name': None,
        'Description': None,
        'Pi_CombinationID': cmbid
        }
        
        ds = request.form['DescP']
        nm = request.form['NameP']
        check = not(Shared.isStringEmptyOrNull(ds))
        if(check):
            aPizza['Description'] = ds
            
        check = not(Shared.isStringEmptyOrNull(nm))
        if(check):
            aPizza['Name'] = ds
            
        Pizza.save(aPizza)
        
        return aPizza
        
        
    @staticmethod
    def obtainArrayOfDictionariesOfPizzaIngredients(immutableDict, comboid=None):
        dic = immutableDict
        keyz = dic.keys()
        if(comboid==None):
            comboid = PizzaIngredients.getNextComboid()
        ingrds = Ingredient.getAll()
        farray= []
        
        for i in range(0, len(ingrds)):
            fDict = {}
            tName = ingrds[i].Name
            if(tName in keyz):
                fDict["Pi_IngredientID"] = ingrds[i].IngredientID
                fDict["CombinationID"] = comboid
                fDict["IQty"] = Shared.parse_string_to_int(dic[tName])
                ##print(dic[tName])
            #if(not(bool(fDict))):
                farray.append(fDict)
            
        return farray
    
    @staticmethod
    def saveAnArrayOfIngredientsToPizzaIngreditents(arry):
        for thing in arry:
            PizzaIngredients.save(thing)
        
    @staticmethod
    def parse_string_to_int(s):
        try:
            value = int(s)
        except ValueError:
            print(s + ' value is not an integer')
            value = s
        return value
    
    @staticmethod
    def getFavoritesFromRequest():
        array = Pizza.getAll()
        temp = []
        for i in array:
            temp.append(i.PizzaID)
        immutdict = request.values
        keyz = immutdict.keys()
        
        farray= []
        
        for i in range(0, len(array)):
            fDict = {}
            tName = "c" + (array[i].PizzaID).tostring()
            if(tName in keyz):
                fDict[("c" + (array[i].PizzaID).tostring())] = { "Pizza_ID": array[i].PizzaID, "Active": array[i].Active}
                #fDict["IQty"] = Shared.parse_string_to_int(dic[tName])
                farray.append(fDict)
    
    @staticmethod
    def obtainAndCompareAgainstRequstArray(immutableDict, array, arrayfield):
        dic = immutableDict
        keyz = dic.keys()

        farray= []
        
        for i in range(0, len(array)):
            fDict = {}
            tName = array[i].Name
            if(tName in keyz):
                fDict[arrayfield] = array[i].arrayfield
                fDict["IQty"] = Shared.parse_string_to_int(dic[tName])
                ##print(dic[tName])
            #if(not(bool(fDict))):
                farray.append(fDict)
