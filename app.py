from flask import Flask, request, render_template, redirect, url_for
from models import db, SeasonalFlavor, Ingredient, CustomerSuggestion
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add_flavor', methods=['GET', 'POST'])
def add_flavor():
    if request.method == 'POST':
        new_flavor = request.form.get('flavor')
        print("New flavor received:", new_flavor)  # Log input

        if not new_flavor:
            print("Error: Flavor name is empty")  # Log error
            return render_template('add_flavor.html', error='Flavor name cannot be empty')

        # Check if flavor already exists in database
        existing_flavor = SeasonalFlavor.query.filter_by(flavor=new_flavor).first()
        if existing_flavor:
            print("Error: Flavor already exists")  # Log error
            return render_template('add_flavor.html', error='Flavor already exists')

        # Create and add the flavor to the session
        flavor = SeasonalFlavor(flavor=new_flavor)
        db.session.add(flavor)
        db.session.commit()
        print("Flavor added to database:", flavor.flavor)  # Log success

        return render_template('add_flavor.html', message='Flavor added successfully')

    return render_template('add_flavor.html')



@app.route('/list_flavors')
def list_flavors():
    flavors = SeasonalFlavor.query.all()
    print("Flavors:", flavors)
    return render_template('list_flavors.html', flavors=flavors)

@app.route('/add_ingredient', methods=['GET', 'POST'])
def add_ingredient():
    if request.method == 'POST':
        ingredient = request.form.get('ingredient')
        stock = request.form.get('stock')
        if not ingredient or stock is None:
            return render_template('add_ingredient.html', error='Ingredient name and stock are required')

        try:
            stock = int(stock)
        except ValueError:
            return render_template('add_ingredient.html', error='Stock must be a number')

        if stock < 0:
            return render_template('add_ingredient.html', error='Stock cannot be negative')

        if Ingredient.query.filter_by(ingredient=ingredient).first():
            return render_template('add_ingredient.html', error='Ingredient already exists')

        new_ingredient = Ingredient(ingredient=ingredient, stock=stock)
        db.session.add(new_ingredient)
        db.session.commit()
        return render_template('add_ingredient.html', message='Ingredient added successfully')

    return render_template('add_ingredient.html')

@app.route('/list_ingredients')
def list_ingredients():
    ingredients = Ingredient.query.all()
    return render_template('list_ingredients.html', ingredients=ingredients)

@app.route('/add_suggestion', methods=['GET', 'POST'])
def add_suggestion():
    if request.method == 'POST':
        name = request.form.get('name')
        flavor = request.form.get('flavor')
        allergy_concerns = request.form.get('allergy_concerns')
        if not name or not flavor:
            return render_template('add_suggestion.html', error='Name and flavor are required')

        suggestion = CustomerSuggestion(name=name, flavor=flavor, allergy_concerns=allergy_concerns)
        db.session.add(suggestion)
        db.session.commit()
        return render_template('add_suggestion.html', message='Suggestion added successfully')

    return render_template('add_suggestion.html')

@app.route('/list_suggestions')
def list_suggestions():
    suggestions = CustomerSuggestion.query.all()
    return render_template('list_suggestions.html', suggestions=suggestions)

@app.route('/delete_flavor/<int:flavor_id>', methods=['POST'])
def delete_flavor(flavor_id):
    flavor = SeasonalFlavor.query.get_or_404(flavor_id)
    db.session.delete(flavor)
    db.session.commit()
    return redirect(url_for('list_flavors'))

@app.route('/update_flavor/<int:flavor_id>', methods=['GET', 'POST'])
def update_flavor(flavor_id):
    flavor = SeasonalFlavor.query.get_or_404(flavor_id)
    if request.method == 'POST':
        new_flavor_name = request.form.get('flavor')
        if not new_flavor_name:
            return render_template('update_flavor.html', error='Flavor name cannot be empty', flavor_id=flavor_id)

        if SeasonalFlavor.query.filter_by(flavor=new_flavor_name).first():
            return render_template('update_flavor.html', error='Flavor already exists', flavor_id=flavor_id)

        flavor.flavor = new_flavor_name
        db.session.commit()
        return redirect(url_for('list_flavors'))

    return render_template('update_flavor.html', flavor=flavor.flavor, flavor_id=flavor_id)

@app.route('/delete_ingredient/<int:ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    return redirect(url_for('list_ingredients'))

@app.route('/update_ingredient/<int:ingredient_id>', methods=['GET', 'POST'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    if request.method == 'POST':
        new_ingredient_name = request.form.get('ingredient')
        new_stock = request.form.get('stock')
        if not new_ingredient_name or new_stock is None:
            return render_template('update_ingredient.html', error='Ingredient name and stock are required', ingredient_id=ingredient_id)

        try:
            new_stock = int(new_stock)
        except ValueError:
            return render_template('update_ingredient.html', error='Stock must be a number', ingredient_id=ingredient_id)

        if new_stock < 0:
            return render_template('update_ingredient.html', error='Stock cannot be negative', ingredient_id=ingredient_id)

        if Ingredient.query.filter_by(ingredient=new_ingredient_name).filter(Ingredient.id != ingredient_id).first():
            return render_template('update_ingredient.html', error='Ingredient already exists', ingredient_id=ingredient_id)

        ingredient.ingredient = new_ingredient_name
        ingredient.stock = new_stock
        db.session.commit()
        return redirect(url_for('list_ingredients'))

    return render_template('update_ingredient.html', ingredient=ingredient.ingredient, stock=ingredient.stock, ingredient_id=ingredient_id)

@app.route('/delete_suggestion/<int:suggestion_id>', methods=['POST'])
def delete_suggestion(suggestion_id):
    suggestion = CustomerSuggestion.query.get_or_404(suggestion_id)
    db.session.delete(suggestion)
    db.session.commit()
    return redirect(url_for('list_suggestions'))

if __name__ == '__main__':
    app.run(debug=True)