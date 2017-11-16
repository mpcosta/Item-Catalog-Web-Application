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
    print " This is " , catalog_name
    category = session.query(Categories).filter_by(name=catalog_name).first()
    items = session.query(Item).filter_by(ctg_id=category.ctg_id)
    return render_template('category.html', category=category, items=items)


# Show specific item info
@app.route('/catalog/<catalog_name>/<item_name>/')
def showCategoryItem():
    return "This is catalog specific item !"


# Allow Edit of Item
@app.route('/catalog/<catalog_name>/<item_name>/edit/', methods=['GET', 'POST'])
def editCategoryItem():
    return "This is catalog edit item !"

# Allow Delete of Item
@app.route('/catalog/<catalog_name>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteCategoryItem():
    return "This is catalog delete item !"

# JSON endpoint
@app.route('/catalog.json/')
def getCatalogJson():
    return "This is catalog json return !"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
