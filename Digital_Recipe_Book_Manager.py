recipes = {
    "RCP001" : {
        "name" : "Pasta",
        "ingredients" : [("Pasta", 200, "g")],
        "time" : "00:30",
        "category" : "LUNCH",
        "tags" : {"Italian", "Vegetarian"}

    }

}

ALLOWED_CATEGORIES = ["BREAKFAST", "LUNCH", "DINNER", "DESSERT", "SNACK", "BEVERAGE"]
ALLOWED_UNITS = ["g", "kg", "ml", "l", "cup", "tbsp", "tsp", "piece"]
 
next_recipe_id = 2 


def generate_recipe_id():
    global next_recipe_id
    current_id = f"RCP{next_recipe_id:03d}"
    next_recipe_id += 1
    return current_id  

def validate_recipe_name(name):
    
    # Check length (3-50 )
    if not (3 <= len(name) <= 50):
        return False

    # Check at least one letter exists
    if not any(c.isalpha() for c in name):
        return False

    # Check not empty/spaces only
    if not name.strip():
        return False

    # Check allowed characters only (letters, numbers, hyphen, apostrophe, space)
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-' ")
    if not all(c in allowed_chars for c in name):
        return False
    
    return True


def validate_ingredient_name(name):
    """
    Validates ingredient name.
    Must be 3-30 characters.
   
    """
    return 3 <= len(name) <= 30


def validate_quantity(quantity_str):
    
    try:
        quantity = float(quantity_str)
        if quantity <= 0:
            return False
        return True
    except ValueError:
        return False

    
def validate_unit(unit):

    return unit.lower() in ALLOWED_UNITS





#  Cooking Time Validation
def validate_cooking_time(time_str):
 
    # Split by colon
    parts = time_str.split(":")
    
    if len(parts) != 2:
        return False
    # Convert to integers
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        return False
    # Check ranges
    if not (0 <= hours <= 12 and 0 <= minutes <= 59):
        return False
    
    total_minutes = hours * 60 + minutes
    if not (5 <= total_minutes <= 720):
        return False

    return True


# Category Validation
def validate_category(category_input):
    
    return category_input.upper() in ALLOWED_CATEGORIES





# ========================================
# TASK 2: INPUT COLLECTION FUNCTIONS
# ========================================

def get_recipe_name_input():
    while True:
        name = input("Enter recipe name: ")
        if validate_recipe_name(name):
            return name
        else:
            print("Invalid recipe name. Please try again.")

def get_cooking_time_input():
    while True:
        time_str = input("Enter cooking time (HH:MM): ")
        if validate_cooking_time(time_str):
            return time_str
        else:
            print("Invalid cooking time. Please try again.")

def get_category_input():
    print("\nAvailable categories:") 
    for i, cat in enumerate(ALLOWED_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    
    while True:
        category = input("Enter recipe category: ")
        if validate_category(category):
            return category.upper()  # Return uppercase for consistency
        else:
            print(f"Invalid category. Choose from: {', '.join(ALLOWED_CATEGORIES)}")


def get_ingredients_input():
 
    ingredients = []
    
    while True:
        print(f"\nIngredient {len(ingredients) + 1}:")
        ingredient_str = input("Enter Name, Quantity, Unit (example: parata, 100, piece) or 'done': ")
        
        if ingredient_str.lower() == "done":
            if len(ingredients) < 3:
                print("Must have at least 3 ingredients!")
                continue
            return ingredients
        
        # Parse the ingredient string
        parts = ingredient_str.split(",")
        if len(parts) != 3:
            print("Format: Name, Quantity, Unit")
            continue
        
        name = parts[0].strip()
        qty_str = parts[1].strip()
        unit = parts[2].strip()
        
        # Validate each part
        if not validate_ingredient_name(name):
            print("Name must be 3-30 characters")
            continue
        if not validate_quantity(qty_str):
            print("Quantity must be a positive number")
            continue
        if not validate_unit(unit):
            print(f"Unit must be one of: {', '.join(ALLOWED_UNITS)}")
            continue
        
        # Convert quantity to float and store as tuple
        ingredients.append((name, float(qty_str), unit.lower()))
        print(f"Added: {name}")




# ========================================
# TASK 2: DISPLAY FUNCTIONS
# ========================================

def display_single_recipe(recipe_id):
    
    if recipe_id not in recipes:
        print(f"Recipe {recipe_id} not found!")
        return
    
    recipe = recipes[recipe_id]
    
    print("\n" + "="*40)
    print(f"Recipe ID: {recipe_id}")
    print(f"Name: {recipe['name']}")
    print(f"Category: {recipe['category']}")
    print(f"Cooking Time: {recipe['time']}")
    print("-"*40)
    print("Ingredients:")
    for i, (name, qty, unit) in enumerate(recipe['ingredients'], 1):
        print(f"  {i}. {name} - {qty} {unit}")
    print("-"*40)
    tags_str = ", ".join(recipe['tags']) if recipe['tags'] else "None"
    print(f"Tags: {tags_str}")
    print("="*40 + "\n")




def display_all_recipes():
  
    if not recipes:
        print("No recipes in the book yet!")
        return
    
    print(f"\nTotal Recipes: {len(recipes)}")
    print("-"*50)
    for recipe_id, recipe in recipes.items():
        print(f"{recipe_id} | {recipe['name']} | {recipe['category']} | {recipe['time']}")
    print()



def display_recipes_by_category(category):
    
    # Displays recipes matching a specific category.
    
    matching_recipes = {rid: r for rid, r in recipes.items() if r['category'] == category.upper()}
    
    if not matching_recipes:
        print(f"No recipes found in {category}")
        return
    
    print(f"\nFound {len(matching_recipes)} {category.upper()} recipes:")
    print("-"*50)
    for recipe_id, recipe in matching_recipes.items():
        print(f"{recipe_id} | {recipe['name']} | {recipe['category']} | {recipe['time']}")
    print()








def add_recipe():
   
    print("\n" + "="*50)
    print("ADD NEW RECIPE")
    print("="*50)
    
    # Get inputs using TASK 2 input functions
    name = get_recipe_name_input()
    ingredients = get_ingredients_input()
    time = get_cooking_time_input()
    category = get_category_input()
    
    # Generate ID
    recipe_id = generate_recipe_id()
    
    # Create recipe dictionary
    recipe = {
        "name": name,
        "ingredients": ingredients,
        "time": time,
        "category": category,
        "tags": set()  # User can add tags later (optional)
    }
    
    # Store in recipes
    recipes[recipe_id] = recipe
    
    # Display confirmation
    print("\n" + "="*50)
    print("RECIPE ADDED SUCCESSFULLY")
    print("="*50)
    print(f"Recipe ID: {recipe_id}")
    print(f"Name: {name}")
    print(f"Ingredients: {len(ingredients)}")
    print(f"Category: {category}")
    print(f"Cooking Time: {time}")
    print("="*50 + "\n")
    
    return recipe_id





def save_recipes():

    try:
        with open("recipes.txt", "w") as file:
            for recipe_id, recipe in recipes.items():
                # Write recipe header
                file.write("===RECIPE===\n")
                file.write(f"ID:{recipe_id}\n")
                file.write(f"NAME:{recipe['name']}\n")
                file.write(f"CATEGORY:{recipe['category']}\n")
                file.write(f"TIME:{recipe['time']}\n")
                
                
                ingredients_str = "|".join([f"{name},{qty},{unit}" for name, qty, unit in recipe['ingredients']])
                file.write(f"INGREDIENTS:{ingredients_str}\n")
                
                
                tags_str = ",".join(recipe['tags']) if recipe['tags'] else ""
                file.write(f"TAGS:{tags_str}\n")
                
                
                file.write("===END===\n\n")
        
        print("Recipes saved successfully to recipes.txt")
        return True
    
    except Exception as e:
        print(f"Error saving recipes: {e}")
        return False
    

def load_recipes():

    global next_recipe_id
    
    import os
    
    if not os.path.exists("recipes.txt"):
        print("No saved recipes found. Starting fresh.")
        return 0
    
    try:
        with open("recipes.txt", "r") as file:
            content = file.read()
        
        # Split by recipe blocks
        recipe_blocks = content.split("===RECIPE===")
        loaded_count = 0
        max_id_num = 1
        
        for block in recipe_blocks:
            if not block.strip() or "===END===" not in block:
                continue
            
            # Parse each line
            lines = block.strip().split("\n")
            recipe_data = {}
            
            for line in lines:
                if ":" not in line or line.startswith("==="):
                    continue
                
                key, value = line.split(":", 1)
                recipe_data[key] = value
            
            # Extract fields
            recipe_id = recipe_data.get("ID", "")
            name = recipe_data.get("NAME", "")
            category = recipe_data.get("CATEGORY", "")
            time = recipe_data.get("TIME", "")
            ingredients_str = recipe_data.get("INGREDIENTS", "")
            tags_str = recipe_data.get("TAGS", "")
            
            # Parse ingredients back to tuples
            ingredients = []
            if ingredients_str:
                for ing in ingredients_str.split("|"):
                    parts = ing.split(",")
                    if len(parts) == 3:
                        ingredients.append((parts[0], float(parts[1]), parts[2]))
            
            # Parse tags back to set
            tags = set(tag.strip() for tag in tags_str.split(",") if tag.strip())
            
            # Create recipe dictionary
            if recipe_id and name:
                recipes[recipe_id] = {
                    "name": name,
                    "ingredients": ingredients,
                    "time": time,
                    "category": category,
                    "tags": tags
                }
                loaded_count += 1
                
                # Track maximum ID number for next_recipe_id
                try:
                    id_num = int(recipe_id[3:])
                    if id_num > max_id_num:
                        max_id_num = id_num
                except:
                    pass
        
        # Update next_recipe_id to be higher than any loaded ID
        next_recipe_id = max_id_num + 1
        
        if loaded_count > 0:
            print(f"Loaded {loaded_count} recipes successfully")
        
        return loaded_count
    
    except Exception as e:
        print(f"Error loading recipes: {e}")
        return 0
    



def export_recipe():
   
    if not recipes:
        print("No recipes to export!")
        return
    
    # Show available recipes
    print("\nRecipes available for export:")
    recipe_ids = list(recipes.keys())
    for i, rid in enumerate(recipe_ids, 1):
        print(f"  {i}. {rid} - {recipes[rid]['name']}")
    
    # Get user choice
    try:
        choice = int(input("Select recipe number to export: ")) - 1
        if 0 <= choice < len(recipe_ids):
            recipe_id = recipe_ids[choice]
        else:
            print("Invalid choice!")
            return
    except ValueError:
        print("Invalid input!")
        return
    
    recipe = recipes[recipe_id]
    
    # Create filename (sanitize name for valid filename)
    safe_name = "".join(c for c in recipe['name'] if c.isalnum() or c in (' ', '-', '_')).replace(" ", "_")
    filename = f"recipe_{safe_name}.txt"
    
    try:
        with open(filename, "w") as file:
            file.write("="*50 + "\n")
            file.write(f"RECIPE: {recipe['name']}\n")
            file.write("="*50 + "\n\n")
            
            file.write(f"Category: {recipe['category']}\n")
            file.write(f"Cooking Time: {recipe['time']}\n\n")
            
            file.write("INGREDIENTS:\n")
            for name, qty, unit in recipe['ingredients']:
                file.write(f"  - {name}: {qty} {unit}\n")
            
            file.write("\n")
            tags_str = ", ".join(recipe['tags']) if recipe['tags'] else "None"
            file.write(f"TAGS: {tags_str}\n")
            file.write("="*50 + "\n")
        
        print(f"Recipe exported to {filename}")
    
    except Exception as e:
        print(f"Error exporting recipe: {e}")

# MENU  section  (Displays main menu options)


def display_menu():
    
    print("\n" + "="*50)
    print("DIGITAL RECIPE BOOK MANAGER")
    print("="*50)
    print("1. Add New Recipe")
    print("2. View All Recipes")
    print("3. View Recipe by ID")
    print("4. View Recipes by Category")
    print("5. Save Recipes to File")
    print("6. Export Single Recipe")
    print("7. Exit")
    print("="*50)


def main():
    
    print("\nWelcome to Digital Recipe Book Manager!")
    
    # Load saved recipes at startup
    load_recipes()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_recipe()
        
        elif choice == "2":
            display_all_recipes()
        
        elif choice == "3":
            recipe_id = input("Enter Recipe ID (e.g., RCP001): ").strip().upper()
            display_single_recipe(recipe_id)
        
        elif choice == "4":
            category = input("Enter category: ").strip()
            display_recipes_by_category(category)
        
        elif choice == "5":
            save_recipes()
        
        elif choice == "6":
            export_recipe()
        
        elif choice == "7":
            save_recipes()  # Auto-save before exit
            print("\nThank you for using Recipe Book Manager! Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter 1-7.")


# Program entry point
if __name__ == "__main__":
    main()




   










