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


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show the Main Page
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Categories)
    items = session.query(Item).order_by(desc(Item.date_created)).limit(3)
    return render_template('index.html', categories=categories, latest_items=items)


# Show the items related to Category
@app.route('/catalog/<catalog_name>/items/')
def showCategoryItems(catalog_name):
    category = session.query(Categories).filter_by(name=catalog_name).first()
    items = session.query(Item).filter_by(ctg_id=category.ctg_id)
    return render_template('category.html', category=category, items=items)


# Show specific item info
@app.route('/catalog/<catalog_name>/<item_name>/')
def showCategoryItem(catalog_name, item_name):
    # If catalog_name is an ID translate it to item name
    if (len(catalog_name) == 1):
        category = session.query(Categories).filter_by(ctg_id=catalog_name).first()
    else:
        category = session.query(Categories).filter_by(name=catalog_name).first()
    #items = session.query(Item).filter_by(ctg_id=category.ctg_id)
    item = session.query(Item).filter_by(title=item_name).first()
    return render_template('item.html', category=category.name, item=item)


# Allow Edit of Item
@app.route('/catalog/<catalog_name>/<item_name>/edit/', methods=['GET', 'POST'])
def editCategoryItem(catalog_name, item_name):



    if request.method == 'POST':
        editedItem = session.query(Item).filter_by(title=item_name).first()

        if request.form['name']:
            editedItem.title = request.form['name']
        #if request.form['']
        #    editedItem.title = request.form['name']








            #flash('Item Successfully Edited %s' % editedItem.name)


        return redirect(url_for('showCatalog'))
    else:
        # Get Resquest
        category = session.query(Categories).filter_by(name=catalog_name).first()
        item = session.query(Item).filter_by(title=item_name).first()
        return render_template('editItem.html', category=category.name, item=item)

# Allow Delete of Item
#@app.route('/catalog/<catalog_name>/<item_name>/delete/', methods=['GET', 'POST'])
@app.route('/catalog/delete/', methods=['GET', 'POST'])
def deleteCategoryItem():
    return render_template('deleteItem.html')

# JSON endpoint
@app.route('/catalog/JSON/')
def getCatalogJson():
    catalogItems = session.query(Item).all()
    return jsonify(catalogItems=[r.serialize for r in catalogItems])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
