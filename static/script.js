document.getElementById('searchButton').addEventListener('click', function() {
    var userInput = document.getElementById('food').value;

    fetch('/generate_recipe', {  // Updated endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ food: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const recipeDiv = document.getElementById('recipeResult');
        
        // Clear the div content only if it exists
        if (data.error) {
            recipeDiv.innerText = data.error;
        }
        else {
            recipeDiv.innerHTML = '';
        
            // Define the order of sections
            const sectionOrder = ['SUMMARY', 'INGREDIENTS', 'SERVING SIZE', 'DIRECTIONS', 'CONCLUSION'];
    
            // Iterate over the sections in the specified order
            sectionOrder.forEach(sectionKey => {
                const value = data.recipe[sectionKey];
                // Check if the section value exists and is not empty
                if (value && value.trim() !== '') {
                    const paragraph = document.createElement('p');
                    
                    if (sectionKey === 'CONCLUSION' || sectionKey === 'SUMMARY') {
                        paragraph.innerText = value;
                    } else {
                        paragraph.innerText = `\n${sectionKey}: \n${value}`;
                    }
                    
                    recipeDiv.appendChild(paragraph);
                }
            });

        } 
    })
    .catch(error => console.error('Error:', error));
});