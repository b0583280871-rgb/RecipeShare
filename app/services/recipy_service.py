from app.models import db, Recipe, IngredientEntry
from flask_login import current_user
import json
import os
import uuid
from werkzeug.utils import secure_filename
from app.services.image_service import process_image_variations
from flask import request

#region add_recipe

#השתמשתי במטמון ע"מ לשמור את כל המתכונים המכילים רשימת רכיבים מומרת לSET בשביל לחסוך המרות חוזרות,
# כל רשימת רכיבים מומרת פעם אחת (בטעינת השרת או בהוספת המתכון
#region טעינת ה-cache
recipes_cache = []


def load_recipes_to_cache():
    global recipes_cache
    # שליפה חד פעמית והמרה לפורמט של סטים
    all_recipes = Recipe.query.all()
    recipes_cache = [
        {
            "id": r.id,
            "title": r.title,
            "ingredients_set": set(ing.name.lower().strip() for ing in r.ingredients),
            "image_path": r.image_path
        } for r in all_recipes
    ]


#endregion

def add_recipe_service():
    if current_user.role != 'Admin' and not current_user.is_approved_uploader:
        return {"message": "You do not have permission to upload recipes"}, 403

    # 1. חילוץ נתונים מ-request.form (בגלל שזה Form-Data עם תמונה)
    title = request.form.get('title')
    category = request.form.get('category')
    type_choice = request.form.get('type')
    instructions = request.form.get('instructions')

    # חילוץ רכיבים (נניח שהם נשלחים כסטרינג של JSON בתוך ה-form)
    ingredients_raw = request.form.get('ingredients', '[]')
    ingredients_list = json.loads(ingredients_raw)

    if not title or not category or 'image' not in request.files:
        return {"message": "Title, Category and Image are required"}, 400

    # 2. טיפול בתמונה המקורית
    file = request.files['image']
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    image_path = os.path.join('app/static/recipe_pics', unique_name)  # image_path לפי האפיון
    file.save(image_path)

    # 3. קריאה לפונקציית העזר ליצירת 3 וריאציות
    try:
        variations_dict = process_image_variations(image_path)
        # המרת המילון למחרוזת JSON עבור ה-DB
        variation_paths_json = json.dumps(variations_dict)

        # 4. יצירת המתכון (DAL)
        new_recipe = Recipe(
            title=title,
            category=category,
            type=type_choice,  # השדה מהאפיון
            instructions=instructions,
            image_path=image_path,  # נתיב מקורי
            variation_paths=variation_paths_json,  # JSON של הווריאציות
            user_id=current_user.id
        )

        db.session.add(new_recipe)
        db.session.flush()

        # 5. הוספת רכיבים
        for ing in ingredients_list:
            entry = IngredientEntry(
                recipe_id=new_recipe.id,
                name=ing.get('name'),
                amount=ing.get('amount')
            )
            db.session.add(entry)

        db.session.commit()

        new_cache_item = {
            "id": new_recipe.id,
            "title": new_recipe.title,
            "ingredients_set": set(ing.name.lower().strip() for ing in ingredients_list),
            "image_path": new_recipe.image_path
        }

        recipes_cache.append(new_cache_item)
        return {"message": f"Recipe '{title}' added successfully!"}, 201

    except Exception as e:
        db.session.rollback()
        # ניקוי קבצים אם נכשל
        if os.path.exists(image_path): os.remove(image_path)
        return {"message": f"Error: {str(e)}"}, 500


#endregion

#region smart_search
def search_recipes_service(user_ingredients):
    """
    מבצעת חיפוש חכם על ה-Cache ומחזירה את המתכונים המתאימים ביותר.
    """
    # 1. ניקוי והכנת ה-Set של המשתמש
    user_set = set(ing.lower().strip() for ing in user_ingredients if ing)

    if not user_set:
        return {"message": "No ingredients provided"}, 400

    results = []

    for recipe in recipes_cache:
        recipe_set = recipe["ingredients_set"]

        intersection = user_set & recipe_set
        score = len(intersection) / len(recipe_set) if len(recipe_set) > 0 else 0

        if score > 0:
            # יוצרים עותק של הנתונים ומוסיפים לו את הציון
            result_item = {
                "id": recipe["id"],
                "title": recipe["title"],
                "image_path": recipe["image_path"],
                "match_score": round(score * 100, 1)  # הופך ל-85.5% לדוגמה
            }
            results.append(result_item)

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return results[:10], 200

#endregion