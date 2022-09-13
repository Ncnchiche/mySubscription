<h1 align="center">Ghost Expense</h1>
## What is this?

Not everyone has the time to track their subscriptions and see which category takes up the most of their monthly money. Here I created a Basic Web Application to be able to track your expenses and see analytically which category takes up the most of your budget
A Dashboard which includes :
-A List of subscriptions  
-A graph that addes the total of each category 

## What I Learned
* Using MVC design pattern to divide the related program logic into three elements
* Using Jinja for web template for python programming {{ }}
* Connecting Database to the webapp.....Used Flask-MySQL.
* Using BootStrap as FrontEnd
* Using Git
* JavaScript

## How to Run
Firstly clone the files and download all the dependencies
Then go to your terminal and cd into the file
```python
>from application import db, User, Category, Subscription
>db.create_all()
*Exit out of python and type
flask run


### Flask - Subscription tracker webapp 

### This Was Made using Flask as the framework, Python for the backend, Javascript for interactive graph, html & css (bootstrap) for frontend. 
