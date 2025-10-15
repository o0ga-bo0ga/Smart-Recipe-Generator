from flask import Flask, request, render_template, jsonify, g, redirect, url_for, session
from dotenv import load_dotenv
import os
from llm_service import generate_recipes
from db_service import get_db, close_db, timestamp_to_date
from image_service import process_image
from recipe_parser import parse_recipes

# Flask will automatically find 'templates' and 'static' folders in the same directory
app = Flask(__name__)

load_dotenv()

# Config
# Use /tmp for temporary file storage on Vercel's read-only filesystem
UPLOAD_FOLDER = '/tmp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
# It's important to set this from an environment variable for security
app.secret_key = os.environ.get('SECRET_KEY', 'a-default-fallback-key-if-not-set')

# Register database teardown
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


# Register custom Jinja2 filter
app.jinja_env.filters['timestamp_to_date'] = timestamp_to_date

@app.route('/', methods=['GET', 'POST'])
def home():
    response_text = ""
    error = ""
    loading = False
    recipes = session.get('recipes', [])

    db, c = get_db()
    c.execute("SELECT * FROM favorites ORDER BY timestamp DESC")
    favorites = c.fetchall()

    if request.method == 'POST':
        action = request.form.get('action', 'generate')
        loading = True

        if action == 'generate':
            ingredients_text = request.form.get('ingredients', '').strip()
            dietary = ', '.join(request.form.getlist('dietary'))
            difficulty = request.form.get('difficulty', '')
            time = request.form.get('time', '')
            servings = request.form.get('servings', '4')

            recognized_ingredients = []
            if 'photo' in request.files:
                file = request.files['photo']
                if file and file.filename and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
                    recognized_ingredients = process_image(file, app.config['UPLOAD_FOLDER'])

            ingredients = ingredients_text or ', '.join(recognized_ingredients)
            if not ingredients:
                error = "No ingredients detected. Please upload a photo or enter text."
            else:
                # (Your query generation logic remains the same)
                query = f"Generate exactly 3 unique recipes using these ingredients: {ingredients}. For each recipe, provide a clear, descriptive title prefixed with 'Title: ', followed by 'Difficulty: ' (easy, medium, or hard), 'Cooking time: ' (in minutes or range, e.g., 25-30 minutes), detailed instructions, nutritional information (calories, protein, carbs, fats), and substitution suggestions, each on a new line. "
                if dietary: query += f"Dietary preferences: {dietary}. "
                if difficulty: query += f"Prefer recipes with a difficulty of {difficulty}. "
                if time: query += f"Prefer recipes with a cooking time of {time}. "
                query += f"For {servings} servings. "
                if favorites:
                    high_rated = [f[1] for f in favorites if f[2] >= 4]
                    if high_rated: query += f"Prioritize styles similar to these high-rated recipes: {', '.join(high_rated[:2])}. "
                
                try:
                    response_text = generate_recipes(query)
                except Exception as e:
                    error = f"Query failed: {str(e)}"

            recipes = parse_recipes(response_text) if response_text else []
            session['recipes'] = recipes
            if error:
                session.pop('recipes', None)
                return render_template('index.html', response=None, error=error, loading=False, favorites=favorites)
            return redirect(url_for('home'))

        elif action == 'save':
            recipe = request.form.get('recipe', '')
            rating = request.form.get('rating', '')
            if recipe and rating:
                try:
                    import time
                    c.execute("INSERT INTO favorites (recipe_text, rating, timestamp) VALUES (?, ?, ?)",
                            (recipe, int(rating), int(time.time())))
                    db.commit()
                except Exception as e:
                    error = f"Save error: {str(e)}"
            return redirect(url_for('home'))

    session.pop('recipes', None)
    return render_template('index.html', response=recipes, error=error, loading=loading, favorites=favorites)

# The handler for the API endpoint remains the same
@app.route('/api/query', methods=['POST'])
def query_endpoint():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Missing query'}), 400

    try:
        response = generate_recipes(query)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
