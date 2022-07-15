
import imp
from flask_app import app
from flask import Flask, render_template, session, redirect, flash, request
from flask_app.models.Ingredient import Ingredient
from flask_app.models.User import User
from flask_app.models.Shared import Shared
from flask_app.models.Sizes import Sizes
from flask_app.models.CrustTypes import CrustTypes
from flask_app.models.Shared import Shared
from flask_app.models.PizzaIngredients import PizzaIngredients
from flask_app.models.Pizza import Pizza


@app.route('/Dashboard')
def dashboard():
    Statuses = {'Status': ['For Sale', 'Bought']}
    if 'ID' not in session:
        flash("log in required")
        return redirect('/')
    data = {
        'ID': session['ID']
    }
    # theUser = User.getOne(data)
    #thepizzas = pizza.getAll()
    # thepizzas = pizza.getAllBySellerJoined()
    # print("the pizzas controler: ", thepizzas[0].PrintInfo() )
    #s=Statuses[0]
    return render_template('dashboard.html')

@app.route('/NewOrder', methods=['POST'])
def GoToAddApizza():
    #print('redirect CraftAPizza_normal')
    return redirect('/CraftAPizza_normal')

@app.route('/CraftAPizza_normal')
def Editpizza():
    sz = Sizes.getAll()
    crs = CrustTypes.getAll()
    indgs = Ingredient.getAll()
    x = len(indgs)
    empty = ([None] * x)
    #print(sz)
    return render_template('CraftAPizza_normal.html', Sizes=sz, Crusts=crs, li= indgs, rCount=x,  qt=empty)
    
@app.route('/OrderPizzaPost', methods=['POST'])
def EditpizzaPost():
    apizza = Shared.saveNewPizzaFromRequest()
    s= f'you\'ve created a pizza called {apizza["Name"]}: {apizza["Description"]}'
    print(apizza) 
    flash(s)
    return redirect('/awfeawg')
    
@app.route('/updateFavoritesPost', methods=['POST'])
def updateFavoritesPost():
    apizza = Shared.saveNewPizzaFromRequest()
    s= f'you\'ve created a pizza called {apizza["Name"]}: {apizza["Description"]}'
    print(apizza) 
    flash(s)
    return redirect('/awfeawg')



# @app.route('/BuyApizza')
# def PurchaseVehicle():
#     data = {
#         'BuyerID': session['ID'], 
#         'PizzaID': session['PizzaID'], 
#         'Status': 'Purchased'
#         }
#     pizza.purchasepizza(data)
#     flash('Vehicle Purchased')

# @app.route('/AddApizza')
# def AddApizza():
#     return render_template('NewVehicleToList.html')

# @app.route('/logout')
# def logoutP():
#     Shared.logout()
#     return render_template('Login.html')

# @app.route('/AddANewpizza/', methods=['POST'])
# def AddApizzaPost():
#     apizza = {
#         'Price': request.form['Price'],
#         'Model': request.form['Model'],
#         'Make': request.form['Make'],
#         'Year': request.form['Year'],
#         'Description': request.form['Description'],
#         'SellerID': session['ID'],
#         'Status': 'For Sale',
#         'BuyerID': None
#     }
#     check = pizza.validate(apizza)
#     if(check==False):
#         return render_template('NewVehicleToList.html')
#     pizza.save(apizza)
#     s= f'{apizza["Year"]} {apizza["Model"]} has been listed!'
#     flash(s)
#     return redirect('/Dashboard')
    

