<h1 align="center">Ghost Expense</h1>

## What is this?
Not everyone has the time to track their subscriptions and see which category takes up the most of their monthly budget. Here I created a Basic Web Application to be able to track your expenses and see analytically which category takes up the most of your budget.

This web application includes:
- A HomePage
- Register/Login Page
- A Dashboard where you can add, edit, remove Subscription
- A Interactive graph showing which category takes up most of your budget
- A page where you can edit your account information

### How Was it Made?
This Was Made using Flask as the framework, Python for the backend, Javascript for interactive graph, html & css (bootstrap) for frontend. 

## What I Learned
* Using MVC design pattern to divide the related program logic into three elements
* Using Jinja for web template for python programming {{ }}
* Connecting Database to the webapp.....Used Flask-MySQL.
* Using BootStrap as FrontEnd
* Using Git
* JavaScript

## How to Run
Firstly clone the files and download all the dependencies
Then go to your terminal and cd into the file and type python
```python
>from application import db, User, Category, Subscription
>db.create_all()
```
Exit out of python and type
```python
flask run
```
## HomePage Demo
<img src="https://github.com/Ncnchiche/mySubscription/blob/master/GhostExpense.gif" alt="demo" width="700">

## Dashboard Demo
<img src="https://github.com/Ncnchiche/mySubscription/blob/master/GhostExpense2.gif" alt="demo2" width="500">
