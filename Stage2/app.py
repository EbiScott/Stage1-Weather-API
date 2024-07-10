import os
import psycopg2
from flask import *
from dotenv  import load_dotenv

load_dotenv()
#I need to implement "all to do.txt" here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
connection = psycopg2.connect(os.getenv("DATABASE_URL"))

db = SQLALCHEMY(app)


# CREATE_USERS_TABLE  = (CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, firstName TEXT, LastNAME TEXT, email EMAIL, password PASSWORD))

class UserDataBase():
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=True)

    def __init__(self, firstname, lastname, email, password, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone


class OrganisationDataBase():
    __tablename__ = "organisation"
    orgId = db.column(db.string(100), nullable=False)
    name = db.column(db.string(100), nullable=False)
    description = db.column(db.string(500), nullable=False)

    def __init__(self, orgId, name, description):
        self.orgId = orgId
        self.name = name
        self.description = description


@app.route("/")
def home():
    return "Welcome to the home page"


@app.route("/auth/register", methods=["POST"])
def register():
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("********", validators=[DataRequired(), Password()])
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
        

    return render_template("register.html")


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