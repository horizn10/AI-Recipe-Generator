# 🧠🍽️ AI Recipe Generator

The **AI Recipe Generator** is a machine learning-powered tool that helps users discover delicious recipes based on the ingredients they already have. By combining NLP techniques like lemmatization with Word2Vec embeddings, the model suggests human-like recipes that match the input ingredients — optionally considering dietary restrictions.

---

## 🚀 Features

- ✅ Accepts user input of ingredients via CLI
- ✅ Filters recipes using dietary restrictions (optional)
- ✅ Lemmatizes and cleans ingredients for accurate NLP matching
- ✅ Trains a custom Word2Vec model on ingredient lists
- ✅ Generates vector embeddings for recipes and ingredients
- ✅ Recommends top-N recipes using cosine similarity
- ✅ Works entirely offline with a large recipe dataset

---

## 📂 Project Structure

```
AI-Recipe-Generator/
├── recipe_generator.py         # Main ML logic
├── RAW_recipes.csv             # Dataset of real recipes
├── README.md                   # Project overview
└── requirements.txt            # Python dependencies
```

---

## 📈 How It Works

1. **Data Preprocessing**:
   - Cleans the dataset by removing nulls and duplicate recipes.
   - Converts stringified ingredient lists to actual Python lists.
   - Applies **lemmatization** to normalize ingredient names.

2. **Word2Vec Model Training**:
   - Trains on all ingredient lists to learn relationships between ingredients.
   - Generates a vector for each recipe based on the average of its ingredient embeddings.

3. **User Interaction**:
   - User enters a list of ingredients and optional dietary restrictions.
   - The input is cleaned and lemmatized.
   - The model computes a vector for the user's ingredients.
   - Calculates cosine similarity between user input and all recipes.
   - Returns the top-N most relevant recipes.

---

## 🧠 Example Usage

```bash
$ python recipe_generator.py
Enter ingredients separated by commas: chicken, garlic, onion, bell pepper
Enter dietary restrictions separated by commas (or leave blank): peanuts
```

**Sample Output:**
```
                name                                   ingredients
123   Garlic Chicken Stir Fry   [chicken, garlic, onion, pepper, soy sauce]
456   Grilled Chicken Bowl      [chicken, rice, garlic, pepper, olive oil]
...
```

---

## 🧾 Dataset

- **Name:** RAW_recipes.csv
- **Source:** [Food.com Recipe Dataset on Kaggle](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-user-interactions)
- **Size:** 230K+ recipes with structured ingredients

---

## 🛠️ Tech Stack

| Tool          | Role                        |
|---------------|-----------------------------|
| Python        | Programming language        |
| Pandas        | Data handling & cleaning    |
| NLTK          | Lemmatization               |
| Gensim        | Word2Vec model training     |
| scikit-learn  | Cosine similarity           |
| NumPy         | Vector math                 |

---

## 📥 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Recipe-Generator.git
cd AI-Recipe-Generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download and Place Dataset
Download `RAW_recipes.csv` from [Kaggle](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-user-interactions) and place it in the root directory.

### 4. Run the App
```bash
python recipe_generator.py
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgments

- [Kaggle: Food.com Recipe Dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-user-interactions)
- Python NLP community for open-source tools

---

## 👤 Author

Built by **Kshitiz Boral** 👨‍💻  
Let’s connect: [GitHub](https://github.com/horizn10) | [LinkedIn](www.linkedin.com/in/kshitiz-boral-05ba551a8)
