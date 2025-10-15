def parse_recipes(response_text):
    recipes = []
    if not response_text:
        return recipes
    
    current_recipe = {"title": "", "details": [], "difficulty": "", "time": ""}
    lines = response_text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("**Recipe"):
            if current_recipe["title"]:  # Save the previous recipe if it has a title
                recipes.append(current_recipe)
            current_recipe = {"title": "", "details": [], "difficulty": "", "time": ""}  # Reset with new fields
        elif line.startswith("Title: "):
            current_recipe["title"] = line.replace("Title: ", "")
        elif line.startswith("Difficulty: ") and not current_recipe["difficulty"]:
            current_recipe["difficulty"] = line.replace("Difficulty: ", "")
        elif line.startswith("Cooking time: ") and not current_recipe["time"]:
            current_recipe["time"] = line.replace("Cooking time: ", "")
        elif current_recipe["title"] and line:  # Collect details after title
            current_recipe["details"].append(line)
    if current_recipe["title"]:  # Append the last recipe
        recipes.append(current_recipe)
    return recipes