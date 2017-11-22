from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Tech Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# Login Page
@app.route('/catalog/login')
def loginCatalog():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)

# Disconnect based on provider
@app.route('/catalog/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Create New User
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Get User Info
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get User ID
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show the Main Page
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Categories)
    items = session.query(Item).order_by(desc(Item.date_created)).limit(3)
    return render_template('index.html', categories=categories, latest_items=items)


# Show the items related to Category
@app.route('/catalog/<int:catalog_id>/items/')
def showCategoryItems(catalog_id):
    category = session.query(Categories).filter_by(ctg_id=catalog_id).first()
    items = session.query(Item).filter_by(ctg_id=category.ctg_id)
    return render_template('category.html', category=category, items=items)


# Show specific item info
@app.route('/catalog/<int:catalog_id>/<item_name>/')
def showCategoryItem(catalog_id, item_name):
    category = session.query(Categories).filter_by(ctg_id=catalog_id).first()
    #items = session.query(Item).filter_by(ctg_id=category.ctg_id)
    item = session.query(Item).filter_by(title=item_name).first()
    return render_template('item.html', category=category.ctg_id, item=item)

# Allow Creation of Item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategoryItem():
    if 'username' not in login_session:
        return redirect('/catalog/login')
    if request.method == 'POST':

        if request.form['name'] and \
           request.form['description'] and \
           request.form['price'] and \
           request.form['url'] and \
           request.form['optionsCategory']:

            newItem = Item(title=request.form['name'], description=request.form['description'],
                        price=request.form['price'], url=request.form['url'],
                        ctg_id=request.form['optionsCategory'], user_id=login_session['user_id'])
            session.add(newItem)
            flash('Item Successfully Created')
            session.commit()
            return redirect(url_for('showCategoryItem', catalog_id=newItem.ctg_id, item_name=newItem.title))
        else:
            flash('New Item could not be created due to missing field.')
            return redirect(url_for('newCategoryItem'))
    else:
        return render_template('newItem.html')



# Allow Editing of Item
@app.route('/catalog/<int:catalog_id>/<item_name>/edit/', methods=['GET', 'POST'])
def editCategoryItem(catalog_id, item_name):
    editedItem = session.query(Item).filter_by(title=item_name).first()
    if 'username' not in login_session:
        return redirect('/catalog/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.title = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['url']:
            editedItem.url = request.form['url']
        if request.form['optionsCategory']:
            editedItem.ctg_id = request.form['optionsCategory']
        session.commit()
        flash('%s Item Successfully Edited' % editedItem.title)
        return redirect(url_for('showCategoryItem', catalog_id=editedItem.ctg_id, item_name=editedItem.title))
    else:
        # Get Resquest
        return render_template('editItem.html', category=editedItem.ctg_id, item=editedItem)

# Allow Removal of Item
@app.route('/catalog/<int:catalog_id>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteCategoryItem(catalog_id, item_name):
    category = session.query(Categories).filter_by(ctg_id=catalog_id).first()
    deleteItem = session.query(Item).filter_by(title=item_name).first()
    if 'username' not in login_session:
        return redirect('/catalog/login')
    if deleteItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(deleteItem)
        flash('Item Successfully Deleted')
        session.commit()
        return redirect(url_for('showCategoryItems', catalog_id=category.ctg_id))
    else:
        return render_template('deleteItem.html', category=category, item=deleteItem)

# JSON endpoint for all items
@app.route('/catalog/JSON/')
def getCatalogJson():
    catalogItems = session.query(Item).all()
    return jsonify(catalogItems=[r.serialize for r in catalogItems])

# JSON endpoint for specific item
@app.route('/catalog/<int:catalog_id>/<item_name>/JSON/')
def getCatalogItemJson(catalog_id, item_name):
    category = session.query(Categories).filter_by(ctg_id=catalog_id).first()
    catalogItem = session.query(Item).filter_by(title=item_name).first()
    return jsonify(catalogItem=catalogItem.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
