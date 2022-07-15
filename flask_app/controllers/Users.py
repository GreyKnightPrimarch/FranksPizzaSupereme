from flask_app import app
from flask import Flask, render_template, session, redirect, flash, request
from flask_bcrypt import Bcrypt
from flask_app.models.User import User
from flask_app.models.Shared import Shared

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/LoginPost', methods=['POST'])
def Login():
    isValid = User.validateLogin(request.form)
    #print(isValid)
    if not isValid:
        flash("invalid login")
        return redirect('/')
    auser = User.getEmail(request.form)
    if not auser:
        print('Loginpost unknown error')
        return redirect('/')
    else:
        print(auser)
        Shared.sessionSave(auser)
    flash('Hey you logged in')
    return redirect('/Dashboard')

@app.route('/RegisterUser')
def startregister():
    return render_template('RegisterUser.html')

@app.route('/AccountEdit')
def AcctEdt():
    data = {
        'ID': session['ID']
    }
    thisuser = User.getOne(data)
    return render_template('AccountEdit.html', user=thisuser)

@app.route('/RegisterPost', methods=['POST'])
def registerpost():
    # print( "----- Start" )
    # print( request.form['ZIP'] )
    # print( "----- End" )
    isValid = User.validateRegister(request.form)
    if not isValid:
        return redirect('/RegisterUser')
    newUser = Shared.saveNewUserFromSession();
    ID = User.save(newUser)
    if not ID:
        print("Issue for dev")
        return redirect('/')
    session['ID'] = ID
    flash('Hey you logged in')
    return redirect('/')

@app.route('/UpdateAccountPost', methods=['POST'])
def UpdateAccountPost():
    # print( "----- Start" )
    # print( request.form['ZIP'] )
    # print( "----- End" )
    isValid = User.validateRegister(request.form)
    if not isValid:
        flash("Not a valid input")
        return redirect('/AccountEdit')
    newUser = Shared.UserUpdateFromSession();
    ID = User.save(newUser)
    if not ID:
        print("Issue for dev")
        return redirect('/')
    session['ID'] = ID
    flash('Account Updated')
    return redirect('/Dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')