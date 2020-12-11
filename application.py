from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import json

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "82heduawbdhb3w73ajdnjwajs"
assets = Environment(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

js = Bundle(    './javascript/script.js',
            output='gen/scripts.js')
assets.register('js_all', js)

css = Bundle(   './css/styles.css',
                './css/register.css',
            output='gen/styles.css')
assets.register('css_all', css)
#--------------------------------------------------------
# DATABASE MODELS
# 1. User
# 2. Subscription
# 3. Subscription
# 4. Category
#--------------------------------------------------------


class User( UserMixin, db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    username = db.Column(db.String(10))
    password = db.Column(db.String(20))
    #relationships
    subscriptions = db.relationship("Subscription", backref="user")

    def __init__(self, fname, lname, age, email, username, password):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.email = email
        self.username = username
        self.password = password

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #relationship
    subscriptions = db.relationship("Subscription", backref="category")

    def __init__(self, name, user):
        self.name = name
        self.user = user


class Subscription( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(15))
    price = db.Column(db.Integer)
    #relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, name, description, price, category, user):
        self.name = name
        self.description = description
        self.price = price
        self.user = user
        self.category = category


# -----------------------------------------------------------------------------
# MAIN ROUTES
# -----------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = User.query.filter_by( username = username, password = password ).first()

        if user is not None:
            login_user(user)
            return redirect("/welcome")
        else:
            return redirect("/login")

    else:
        return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/welcome")
@login_required
def welcome():
    return render_template("welcome.html")

@app.route("/dashboard")
@login_required
def dashboard():
    categories = Category.query.all()
    return render_template("dashboard.html", categories = categories)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/account")
@login_required
def account():
    return render_template("account.html")

category_data = { }


colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route("/bar")
@login_required
def bar():
    subscriptions = Subscription.query.all()
    for subscription in subscriptions:
        if subscription.category.name not in category_data:
            category_data[subscription.category.name ] = 0
        category_data[subscription.category.name ]+= subscription.price
    return render_template('bar_chart.html', title='Bar Chart', max = max(list(category_data.values())), labels=json.dumps(list(category_data.keys())), values=json.dumps(list(category_data.values())))

# -----------------------------------------------------------------------------
# CRUDI - Users Controller
# -----------------------------------------------------------------------------

@app.route("/users")
@login_required
def all_users():
    allUsers = User.query.all()
    return render_template("users.html", users = allUsers)

@app.route("/users/create", methods=["POST"])
def create_user():
    fname = request.form.get('fname', "")
    lname = request.form.get('lname', "")
    age = request.form.get('age', "")
    email = request.form.get('email', "")
    username = request.form.get('username', "")
    password = request.form.get('password', "")

    newUser = User( fname, lname, age, email, username, password)
    db.session.add(newUser)
    db.session.commit()

    return redirect("/login")

@app.route("/users/<id>")
def get_user(id):
    user = User.query.get( int(id) )
    return render_template("user.html", user = user)

@app.route("/users/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(id):
    user = User.query.get( int(id) )
    if request.method == "POST":
        user.fname = request.form.get('fname', "")
        user.lname = request.form.get('lname', "")
        user.age = request.form.get('age', "")
        user.email = request.form.get('email', "")
        user.username = request.form.get('username', "")
        user.password = request.form.get('password', "")

        db.session.commit()
        return redirect("/account")
    else:
        return redirect("/account")

@app.route("/users/<id>/delete", methods=["POST"])
@login_required
def delete_user(id):
    user = User.query.get( int(id) )
    db.session.delete(user)
    db.session.commit()
    return redirect("users")

# -----------------------------------------------------------------------------
# CRUDI - Subscription Controller
# -----------------------------------------------------------------------------
@app.route("/subscriptions")
def all_subscriptions():
    allSubscriptions = Subscription.query.all()
    return render_template("subscriptions.html")

@app.route("/subscriptions/create", methods=["POST"])
@login_required
def create_subscription():
    name = request.form.get('name', "")
    description = request.form.get('description', "")
    price = request.form.get('price', "")
    category_id = request.form.get('category', "")
    category = Category.query.get( int( category_id ))

    newSubscription = Subscription( name, description, price, category, current_user)

    db.session.add(newSubscription)
    db.session.commit()

    return redirect("/dashboard")

@app.route("/subscriptions/<id>/edit", methods=["GET", "POST"])
def edit_subscription(id):
    subscription = Subscription.query.get( int(id) )
    if request == "POST":
        subscription.name = request.form.get('name', "")
        subscription.description = request.form.get('description', "")
        subscription.price = request.form.get('price', "")
        db.session.commit()
        return render_template("subscription.html")
    else:
        return render_template("edit_subscription.html")

@app.route("/subscriptions/<id>/delete")
@login_required
def delete_subscription(id):
    subscription = Subscription.query.get( int(id) )
    db.session.delete(subscription)
    db.session.commit()
    return redirect("/dashboard")


# -----------------------------------------------------------------------------
# CRUDI - Category Controller
# -----------------------------------------------------------------------------
@app.route("/categories")
def all_categories():
    allCategories = Category.query.all()
    return render_template("categories.html")

@app.route("/categories/create", methods=["POST"])
@login_required
def create_category():
    name = request.form.get('name', "")

    newCategory = Category( name, current_user)

    db.session.add(newCategory)
    db.session.commit()

    return redirect("/dashboard")

@app.route("/categories/<id>/edit", methods=["GET", "POST"])
def edit_category(id):
    category = Category.query.get( int(id) )
    if request == "POST":
        category.name = request.form.get('name', "")
        db.session.commit()
        return render_template("category.html")
    else:
        return render_template("edit_category.html")

@app.route("/categories/<id>/delete")
@login_required
def delete_category(id):
    category = Category.query.get( int(id) )
    db.session.delete(category)
    db.session.commit()
    return redirect("/dashboard")



if __name__ == "__main__":
    app.run()