from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, models, admin, forms
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from sqlalchemy import func

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Recipe, db.session))

@app.route('/', endpoint='index')
@app.route('/all', endpoint='all')
def index():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('all.html', title='Recipe App', active_page='all', recipes=recipes, header="All Recipes")

@app.route('/login', endpoint='login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        user = db.session.query(models.User).filter_by(username=username).first()
        if forms.validate_user_credentials(username,password):
            login_user(user)
            return redirect(url_for('all'))
        else:
            flash('Wrong credentials entered')
    return render_template('login.html', title='login', active_page='login', form=form)

@app.route('/register', endpoint='register', methods=['GET', 'POST'])
def register():
    form = forms.LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        if forms.validate_user(username):
            hashed_password = generate_password_hash(password)#password is hashed for security measures
            new_user = models.User(username=username, hashed_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)#login using flask_login using cookies so that the session remains open for the user
            return redirect(url_for('all'))
    return render_template('register.html', title='register', active_page='register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('all'))

@app.route('/appetizers', endpoint='appetizers')
def appetizers():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'appetizers').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('appetizers.html', title='Recipe App', active_page='appetizers', recipes=recipes, header="Appetizers")

@app.route('/beverages', endpoint='beverages')
def beverages():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'beverages').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('beverages.html', title='Recipe App', active_page='beverages', recipes=recipes, header="Beverages")

@app.route('/breakfast', endpoint='breakfast')
def breakfast():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'breakfast').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('breakfast.html', title='Recipe App', active_page='breakfast', recipes=recipes, header="Breakfast")

@app.route('/dessert', endpoint='dessert')
def dessert():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'dessert').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('dessert.html', title='Recipe App', active_page='dessert', recipes=recipes, header="Dessert")

@app.route('/main_course', endpoint='main_course')
def main_course():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'main_course').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('main_course.html', title='Recipe App', active_page='main_course', recipes=recipes, header="Main Course")

@app.route('/salad', endpoint='salad')
def salad():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'salad').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('salad.html', title='Recipe App', active_page='salad', recipes=recipes, header="Salad")

@app.route('/sauces', endpoint='sauces')
def sauces():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'sauces').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('sauces.html', title='Recipe App', active_page='sauces', recipes=recipes, header="Sauces")

@app.route('/side_dish', endpoint='side_dish')
def side_dish():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'side_dish').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('side_dish.html', title='Recipe App', active_page='side_dish', recipes=recipes, header="Side Dish")

@app.route('/snacks', endpoint='snacks')
def snacks():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'snacks').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('snacks.html', title='Recipe App', active_page='snacks', recipes=recipes, header="Snacks")

@app.route('/soups', endpoint='soups')
def soups():
    recipes = db.session.query(models.Recipe).outerjoin(models.Likes).filter(models.Recipe.category == 'soups').group_by(models.Recipe.id).order_by(func.count(models.Likes.recipe_id).desc()).all()
    return render_template('soups.html', title='Recipe App', active_page='soups', recipes=recipes, header="Soups")

@app.route('/user', endpoint='user')
@login_required#in order to access this routes the user must be logged in
def user():
    liked_recipes = db.session.query(models.Recipe).join(models.Likes).filter(models.Likes.user_id == current_user.id).all()
    recipes = db.session.query(models.Recipe).filter(models.Recipe.user_id == current_user.id).all()
    return render_template('user.html', title='Recipe App', active_page='user', recipes=recipes,liked_recipes=liked_recipes, header="My Recipes")

@app.route('/new', endpoint='new', methods=['GET', 'POST'])
@login_required
def new():
    form = forms.RecipeForm()
    if form.validate_on_submit():
        new_recipe = models.Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            steps=form.steps.data,
            category=form.category.data,
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('all'))
    return render_template('new.html', title='New Recipe', form=form)

@app.route('/like/<int:recipe_id>', methods=['POST'])
@login_required
def like_recipe(recipe_id):
    like = models.Likes(user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(like)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/unlike/<int:recipe_id>', methods=['POST'])
@login_required
def unlike_recipe(recipe_id):
    like = db.session.query(models.Likes).filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = db.session.query(models.Recipe).filter_by(id=recipe_id, user_id=current_user.id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
    else:
        flash('You do not have permission to delete this recipe', 'danger')
    return redirect(request.referrer)