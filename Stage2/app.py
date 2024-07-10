import os
import psycopg2
from flask import Flask
from dotenv  import load_dotenv

load_dotenv()
#I need to implement "all to do.txt" here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db = SQLALCHEMY(app)

# CREATE_USERS_TABLE  = (CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, firstName TEXT, LastNAME TEXT, email EMAIL, password PASSWORD))

class DataBase():
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

    def __init__(self, firstname, lastname, email, password, phone):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.phone = phone


@app.route("/")
def home():
    return "Hello World"


@app.route("/auth/register", methods=["POST"])
def register():
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("********", validators=[DataRequired(), Password()])
    phone_number = NumberField("Phone no with country code", validators=[Optional(), Number()])




if __name__ == "__main__":
    app.run(debug=True)