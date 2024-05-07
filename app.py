from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import config

def get_openai_api_key():
    return config.OPENAI_API_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def parse_recipe(response):
    sections = response.strip().split('\n\n')
    parsed_recipe = {}
    for section in sections:
        parts = section.split('\n')
        key = parts[0]
        if key == "<INGREDIENTS>":
            ingredients = []
            for i in range(1, len(parts)):
                if parts[i].startswith("<"):
                    continue
                # ingredients.append("- " + parts[i])  # Add bulletpoint
            parsed_recipe[key] = "\n".join(ingredients)
        elif key == "<DIRECTIONS>":
            directions = []
            for i in range(1, len(parts)):
                if parts[i].startswith("<"):
                    continue
                # directions.append(f"{i}. " + parts[i])  # Add numbered list number
            parsed_recipe[key] = "\n".join(directions)
        else:
            parsed_recipe[key] = parts[1]
    return parsed_recipe

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # Retrieve the food input from the request
    data = request.json
    food = data['food']
    
    # Define the prompt using the given description
    prompt = f"""
    You are a cooking assistant. You will be given the name of a food/meal. When provided with it, you will return the following paragraph:
    A paragraph that contains a 4-5 sentence summary of the food, including details such as its origin, descriptive adjectives for the food's taste, and other interesting information.
    The second section should contain the ingredients needed for the food, with a new line for each ingredient.
    A line right after the list indicating the amount of people this recipe will serve. 
    The third section which should contain instructions on how to cook the food. Each instruction should be a new line and a complete sentence.
    Finally, include a sentence starting with the delimiter that positively concludes the instructions, using a phrase along the lines of 'Enjoy your delicious meal!' or something similar, having a positive concluding note.
    
    Use the following formatting and do not lead with a bulletpoint:
    <SUMMARY>
    [Summary paragraph of food]
    <INGREDIENTS>
    [List of ingredients]
    <SERVING SIZE>
    [number of people the recipe serves]
    <DIRECTIONS>
    [Numbered list of instructions]
    <CONCLUSION>
    [Conclusion]

    However, if the item submitted is not a food (ex: toilet paper, wood, pants), then return:
    "Sorry, I couldn't find a recipe"
    """

    prompt += f"{food}\n"

    client = OpenAI(api_key=get_openai_api_key())

    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)
    
    result = response.choices[0].message.content

    if "Sorry, I couldn't find a recipe" in result:
        # Return an error JSON response
        return jsonify(error="We couldn't find a recipe for this. Please try a different search.")
    
    # Split the recipe string into parts based on the delimiter '<'
    sections = result.split('<')
    # Initialize an empty dictionary to store sections
    recipe_dict = {}

    # Iterate over each section and split it into key-value pairs
    for section in sections:
        if section.strip():
            # Split each section into key and value
            key, value = section.split('>', 1)
            # Remove leading and trailing whitespace from key and value
            key = key.strip()
            value = value.strip()
            # Add key-value pair to the dictionary
            recipe_dict[key] = value

    # Print or send json_str to your website
    return jsonify(recipe=recipe_dict)

if __name__ == '__main__':
    app.run(debug=True)