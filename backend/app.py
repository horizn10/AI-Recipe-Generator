import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from recipe_generator import RecipeGenerator

app = Flask(__name__)
CORS(app)  # Allow frontend to access API

# Initialize RecipeGenerator
generator = RecipeGenerator("RAW_recipes.csv")

# API Route
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    user_ingredients = data.get("ingredients", [])
    dietary_restrictions = data.get("dietary_restrictions", None)

    if not user_ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    recommendations_df = generator.recommend_recipes(user_ingredients, top_n=5, dietary_restrictions=dietary_restrictions)
    recommendations = []
    for _, row in recommendations_df.iterrows():
        recommendations.append({
            "name": row["name"],
            "ingredients": row["ingredients"]
        })

    return jsonify(recommendations)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
