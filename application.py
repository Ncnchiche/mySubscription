from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

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
    #subdetails = db.relationship("Subdetail", backref="user")
    #categories = db.relationship("Category", backref="user")

    def __init__(self, fname, lname, age, email, username, password):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.email = email
        self.username = username
        self.password = password


class Subscription( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    description = db.Column(db.String(15))
    price = db.Column(db.Integer)
    #relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user, name, image, description, price):
        self.user = user
        self.name = name
        self.image = image
        self.description = description
        self.price = price




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
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/account")
def account():
    return render_template("account.html")

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
@login_required
def get_user(id):
    user = User.query.get( int(id) )
    return render_template("user.html", user = user)

@app.route("/users/<id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(id):
    user = User.query.get( int(id) )
    if request == "Post":
        user.fname = request.form.get('fname', "")
        user.lname = request.form.get('lname', "")
        user.age = request.form.get('age', "")
        user.email = request.form.get('email', "")
        user.password = request.form.get('password', "")
        db.session.commit()
        return render_template("user.html", user = user)
    else:
        return render_template("edit_user.html", user = user)

@app.route("/users/<id>/delete", methods=["POST"])
@login_required
def delete_user(id):
    user = User.query.get( int(id) )
    db.session.delete(user)
    db.session.commit()
    return redirect("users")

# -----------------------------------------------------------------------------
# CRUDI - UserSubscription Controller
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# CRUDI - Subscription Controller
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CRUDI - Category Controller
# -----------------------------------------------------------------------------



if __name__ == "__main__":
    app.run()