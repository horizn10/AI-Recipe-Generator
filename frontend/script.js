document.getElementById('recipeForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const ingredientsInput = document.getElementById('ingredients').value.trim();
    const dietaryInput = document.getElementById('dietary').value.trim();

    if (!ingredientsInput) {
        alert('Please enter at least one ingredient.');
        return;
    }

    const ingredients = ingredientsInput.split(',').map(i => i.trim()).filter(i => i.length > 0);
    const dietary_restrictions = dietaryInput ? dietaryInput.split(',').map(i => i.trim()).filter(i => i.length > 0) : null;

    const payload = {
        ingredients: ingredients,
        dietary_restrictions: dietary_restrictions
    };

    try {
        const response = await fetch('http://localhost:5000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert('Error: ' + (errorData.error || 'Failed to get recommendations'));
            return;
        }

        const recommendations = await response.json();
        displayResults(recommendations);
    } catch (error) {
        alert('Error connecting to the server: ' + error.message);
    }
});

function displayResults(recommendations) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    if (!recommendations || recommendations.length === 0) {
        resultsDiv.textContent = 'No recipes found.';
        return;
    }

    recommendations.forEach(recipe => {
        const recipeDiv = document.createElement('div');
        recipeDiv.className = 'recipe';

        const title = document.createElement('h3');
        title.textContent = recipe.name;
        recipeDiv.appendChild(title);

        const ingredientsList = document.createElement('ul');
        recipe.ingredients.forEach(ing => {
            const li = document.createElement('li');
            li.textContent = ing;
            ingredientsList.appendChild(li);
        });
        recipeDiv.appendChild(ingredientsList);

        resultsDiv.appendChild(recipeDiv);
    });
}
