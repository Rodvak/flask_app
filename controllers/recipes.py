from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

# ---------- Display Routes ----------

@app.route('/dashboard')
def success():
    if "user_id" not in session:
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    logged_in_user = User.get_by_id({ "id": session["user_id"] })
    return render_template("dash.html", user = logged_in_user, recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = User.get_by_id({ "id": session["user_id"] })
    return render_template("new_recipe.html", user = logged_in_user)

@app.route('/recipes/<int:id>')
def view_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    recipe = Recipe.get_one({ "id": id })
    return render_template("view_recipe.html", recipe = recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    recipe = Recipe.get_one({ "id": id })
    if session["user_id"] != recipe.user_id:
        return redirect('/')
    logged_in_user = User.get_by_id({ "id": session["user_id"] })
    return render_template("edit_recipe.html", recipe = recipe, user=logged_in_user)


# ---------- Action Routes ----------

@app.route('/recipes/create', methods = ["POST"])
def create_recipe():
    if Recipe.recipe_validator(request.form):
        recipe_id = Recipe.create(request.form)
        return redirect("/")
    return redirect("/recipes/new")

@app.route('/recipes/update', methods = ["POST"])
def update_recipe():
    if Recipe.recipe_validator(request.form):
        recipe_id = Recipe.update(request.form)
        return redirect(f"/recipes/{recipe_id}")
    recipe_id = request.form["id"]
    return redirect(f"/recipes/edit/{recipe_id}")

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    id_dict = { "id": id }
    recipe = Recipe.get_one(id_dict)
    if session["user_id"] == recipe.user_id:
        Recipe.delete(id_dict)
    return redirect("/")