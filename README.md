This web application leverages the OpenAI API (GPT 3.5-Turbo) to create recipes for the user.
Upon arrival, the user is greeted with a welcome and given a short description of how the application works.
![Default Page](https://drive.google.com/uc?export=view&id=1kvRNJH7WoF4M3TE-rgvXdjz1ZbdqzYka)

The user can then enter the name of a food/meal, and an API request will be sent to the GPT assistant.
Prompt engineering is used to direct the assistant to create its response following a list of guidelines. Additionally, it is instructed to return a specified response in case the user's query is not the name of a food (which is parsed later on to return an error message).
Once the OpenAPI returns its result, the data received is parsed and formatted. If an error occurs, the ouput is specified accordingly.
After entering the name of a food/meal and clicking 'Find Recipe', the user will be presented with the recipe as such:
![Part 1 of Recipe Result](https://drive.google.com/uc?export=view&id=1-2Y7CkDlt2h0BVeJwJQIJ1ciSSDrEnKA)
![Part 2 of Recipe Result](https://drive.google.com/uc?export=view&id=1SCHPEydGzW696fAnClU9_Pkn45c_hhxW)

The user can then follow the recipe, or enter a new term into the search bar and look for a new recipe.
