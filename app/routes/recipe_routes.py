from flask import Blueprint, request, jsonify
from flask_login import login_required
# ייבוא ה-Services הרלוונטיים (שימי לב לשם הקובץ recipy_service עם y)
from app.services.recipy_service import add_recipe_service, search_recipes_service

recipe_bp = Blueprint('recipe', __name__)

#region add_recipe
@recipe_bp.route('/recipes', methods=['POST'])
@login_required # רק משתמש מחובר יכול בכלל לנסות
def add_recipe():
    """
        הוספת מתכון חדש כולל העלאת תמונה
        ---
        parameters:
          - name: title
            in: formData
            type: string
            required: true
          - name: category
            in: formData
            type: string
          - name: type
            in: formData
            enum: [חלבי, בשרי, פרווה]
          - name: instructions
            in: formData
            type: string
          - name: ingredients
            in: formData
            type: string
            description: רשימת רכיבים בפורמט JSON (למשל [{"name":"קמח", "amount":"1 קילו"}])
          - name: image
            in: formData
            type: file
            required: true
        responses:
          201:
            description: המתכון נוסף בהצלחה
        """
    #data = request.get_json() א"א לשלוח את התמונה כ-json
    result, status_code = add_recipe_service()
    return jsonify(result), status_code
#endregion

#region smart_search
@recipe_bp.route('/recipes/search', methods=['GET'])
def search_recipes():
    """
        חיפוש מתכונים לפי רשימת רכיבים
        ---
        parameters:
          - name: ingredients
            in: query
            type: string
            required: true
            description: רשימת רכיבים מופרדת בפסיקים (למשל sugar,flour,eggs)
        responses:
          200:
            description: רשימת המתכונים שנמצאו
          400:
            description: לא סופקו רכיבים לחיפוש
        """
    # ב-GET, אנחנו מקבלים את הרכיבים דרך ה-URL (Query Parameters)
    # לדוגמה: /recipes/search?ingredients=sugar,flour,eggs
    ingredients_raw = request.args.get('ingredients', '')

    if not ingredients_raw:
        return jsonify({"message": "Please provide ingredients"}), 400

    user_ingredients_list = ingredients_raw.split(',')

    results, status_code = search_recipes_service(user_ingredients_list)

    return jsonify(results), status_code
#endregion