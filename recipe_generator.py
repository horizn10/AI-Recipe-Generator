import pandas as pd
import numpy as np
import ast
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

#nltk.download('wordnet')

class RecipeGenerator:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.lemmatizer = WordNetLemmatizer()
        self.model = None
        self.preprocess_data()
        self.train_word2vec()

    def preprocess_data(self):
        # Drop rows with missing ingredients or names
        self.df.dropna(subset=['ingredients', 'name'], inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        # Convert string to list
        self.df['ingredients'] = self.df['ingredients'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Normalize and lemmatize ingredients
        self.df['ingredients'] = self.df['ingredients'].apply(self.lemmatize_ingredients)

        # Remove empty ingredient lists and duplicates
        self.df = self.df[self.df['ingredients'].map(len) > 0]
        self.df.drop_duplicates(subset=['name'], inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        # Create ingredients text for TF-IDF or other vectorizers if needed
        self.df['ingredients_text'] = self.df['ingredients'].apply(lambda x: ' '.join(x))

    def lemmatize_ingredients(self, ingredients):
        lemmatized = []
        for ing in ingredients:
            ing = ing.lower().strip()
            lemma = self.lemmatizer.lemmatize(ing)
            lemmatized.append(lemma)
        return lemmatized

    def train_word2vec(self):
        # Train Word2Vec model on ingredients lists
        ingredient_lists = self.df['ingredients'].tolist()
        self.model = Word2Vec(sentences=ingredient_lists, vector_size=100, window=5, min_count=1, workers=4)

        # Create recipe vectors by averaging ingredient vectors
        self.df['vector'] = self.df['ingredients'].apply(self.recipe_vector)

    def recipe_vector(self, ingredients):
        vectors = []
        for ing in ingredients:
            if ing in self.model.wv:
                vectors.append(self.model.wv[ing])
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(self.model.vector_size)

    def recommend_recipes(self, user_ingredients, top_n=5, dietary_restrictions=None):
        # Preprocess user ingredients
        user_ingredients = [self.lemmatizer.lemmatize(i.lower().strip()) for i in user_ingredients]

        # Filter recipes by dietary restrictions if provided
        filtered_df = self.df
        if dietary_restrictions:
            # Example: filter out recipes containing restricted ingredients
            for restriction in dietary_restrictions:
                filtered_df = filtered_df[~filtered_df['ingredients'].apply(lambda ings: restriction in ings)]

        # Compute user vector
        user_vecs = []
        for ing in user_ingredients:
            if ing in self.model.wv:
                user_vecs.append(self.model.wv[ing])
        if user_vecs:
            user_vector = np.mean(user_vecs, axis=0).reshape(1, -1)
        else:
            user_vector = np.zeros((1, self.model.vector_size))

        # Compute cosine similarity
        recipe_vectors = np.vstack(filtered_df['vector'].values)
        similarities = cosine_similarity(user_vector, recipe_vectors)[0]

        # Get top N recipes
        top_indices = similarities.argsort()[-top_n:][::-1]
        return filtered_df.iloc[top_indices][['name', 'ingredients']]

if __name__ == "__main__":
    # Example usage with user input
    generator = RecipeGenerator("RAW_recipes.csv")
    user_ingredients_input = input("Enter ingredients separated by commas: ")
    user_input = [item.strip() for item in user_ingredients_input.split(",") if item.strip()]
    dietary_restrictions_input = input("Enter dietary restrictions separated by commas (or leave blank): ")
    dietary_restrictions = [item.strip() for item in dietary_restrictions_input.split(",") if item.strip()] if dietary_restrictions_input else None
    recommendations = generator.recommend_recipes(user_input, top_n=5, dietary_restrictions=dietary_restrictions)
    print(recommendations)
