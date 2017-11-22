# Catalog Web Application

Source code for a full web application where users can view and add items to the catalog itself.

## Features

- View different types of items inside each category;
- Add new Items to a specific category;
- Edit current Items to a specific category;
- Delete Items to a specific category;
- Login with Google OAuth2

## Code
In order to execute the following code, please clone this repository and add it to a vagrant set up virtual machine.
Execute python scripts in the following order:
1 - python database_setup.py
2 - python populate_catalog.py
3 - python project.py

After this you will have a running server where you can navigate by going to:
http://localhost:8000/

Frameworks Used:
- SQL Alchemy
- Flask

## Interface

Fully Responsive HTML Interface. 


![img](https://i.imgur.com/s0iWvIY.png)

