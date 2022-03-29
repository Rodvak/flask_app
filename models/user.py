from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = ["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        hashes = bcrypt.generate_password_hash(data["password"])
        hashed_dict = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hashes
        }
        query = """INSERT INTO 
            users (
            first_name, 
            last_name, 
            email, 
            password) 
            VALUES (
                %(first_name)s, 
                %(last_name)s, 
                %(email)s, 
                %(password)s
                );"""
        return connectToMySQL("recipes_db").query_db(query, hashed_dict)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes_db").query_db(query, data)
        if result:
            return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("recipes_db").query_db(query, data)
        if result:
            return cls(result[0])

    @staticmethod
    def login_validator(data):
        user = User.get_by_email(data)
        if not user:
            return False
        if not bcrypt.check_password_hash(user.password, data["password"]):
            return False
        return True

    @staticmethod
    def registration_validator(data):
        is_valid = True

        if len(data["first_name"]) <= 1:
            flash("First name must be at least 2 characters!", "register")
            is_valid = False

        if len(data["last_name"]) <= 1:
            flash("Last name must be at least 2 characters!", "register")
            is_valid = False

        user = User.get_by_email(data)
        if user:
            flash("Email is already in use", "register")
            is_valid = False

        if len(data["email"]) <= 3:
            flash("Email must be at least 4 characters long!", "register")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False

        if len(data["password"]) <= 7:
            flash("Password must be 8 characters or more!", "register")
            is_valid = False

        if not any(char.isdigit() for char in data["password"]):
            flash("Password must contain at least one number!", "register")
            is_valid  = False

        if not any(char.isupper() for char in data["password"]):
            flash("Password must contain at least one uppercase letter!", "register")
            is_valid  = False

        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match!", "register")
            is_valid = False

        return is_valid