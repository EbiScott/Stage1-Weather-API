import os
import psycopg2
from flask import *
from werkzeug.security import *
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import *
from dotenv  import load_dotenv

load_dotenv()
#I need to implement "all to do.txt" here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
connection = psycopg2.connect(os.getenv("DATABASE_URL"))
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
db = SQLALCHEMY(app)
jwt = JWTManager(app)


# CREATE_USERS_TABLE  = (CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, firstName TEXT, LastNAME TEXT, email EMAIL, password PASSWORD))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)




@app.route("/")
def home():
    return """
    <h1>Welcome to My Homepage</h1>
    <p><a href="/auth/register">Register</a></p>
    <p><a href="/auth/login">Login</a></p>
    """


@app.route("/auth/register", methods=["POST"])
def register():
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("********", validators=[
        DataRequired(), 
        Password()])
    phone_number = NumberField("Phone no with country code", validators=[Optional(), Number()])

    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        user = UserDataBase(firstname, lastname, email, password, phone)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("home"))
        
    

@app.route("/auth/login", methods=["POST"])
def login():
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("********", validators=[DataRequired(), Password()])

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = DataBase.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                return redirect(url_for("home"))
            else:
                return "Password is incorrect"
        else:
            return "User not found"

    return render_template("login.html")


@app.route("/api/users/<int:id>", methods=["GET"])
def get_user(id):
    user = DataBase.query.get(id)
    return user


@app.route("/api/organisations", methods=["GET", "POST"])
def organisations():
    if request.method == "GET":
        organisations = Organisation.query.all()
        return organisations

    if request.method == "POST":
        #create an organisation and provide the name and description
        name = StringField("Enter name of Organisation you want to create", validators=[DataRequired()])


@app.route("/api/organisations?<int:orgId>")
def organisation_Id(orgId):
    pass
    #get user pass word 





if __name__ == "__main__":
    app.run(debug=True)