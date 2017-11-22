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
    #category = session.query(Categories).filter_by(ctg_id=catalog_id).first()
    if request.method == 'POST':

        if request.form['name'] and \
           request.form['description'] and \
           request.form['price'] and \
           request.form['url'] and \
           request.form['optionsCategory']:

            newItem = Item(title=request.form['name'], description=request.form['description'],
                        price=request.form['price'], url=request.form['url'],
                        ctg_id=request.form['optionsCategory'], user_id=1)
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
    deleteItem = session.query(Item).filter_by(title=item_name).first()

    if request.method == 'POST':
        print "ddd"
    else:
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
