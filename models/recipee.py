from flask import flash, request, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user


class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.under30 = data["under30"]
        self.date_made = data["date_made"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def create(cls, data):
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "under30": int(request.form["under30"]),
            "date_made": request.form["date_made"],
            "user_id": session["user_id"]
        }
        query = "INSERT INTO recipes (name, description, instructions, under30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(date_made)s, %(user_id)s );"
        return connectToMySQL("recipes_db").query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL("recipes_db").query_db(query)
        recipes = []
        if results:
            for row in results:
                temp_recipe = cls(row)
                user_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                temp_recipe.creator = user.User(user_data)
                recipes.append(temp_recipe)
        return recipes

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL("recipes_db").query_db(query, data)
        if results:
            temp_recipe = cls(results[0])
            temp_recipe.creator = user.User(results[0])
            return temp_recipe

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s;"
        connectToMySQL("recipes_db").query_db(query, data)
        return data["id"]

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL("recipes_db").query_db(query, data)

    @staticmethod
    def recipe_validator(data):
        is_valid = True

        if len(data["name"]) <= 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False

        if len(data["description"]) <= 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False

        if len(data["instructions"]) <= 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False

        if data["date_made"] == "":
            flash("Please enter a date.")
            is_valid = False

        return is_valid