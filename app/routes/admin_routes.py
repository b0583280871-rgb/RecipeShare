from flask import Blueprint, jsonify
from flask_login import login_required
# ייבוא ה-Services של המנהל
from app.services.admin_service import get_pending_users_service, admin_approve_user_service

# יצירת ה-Blueprint עבור פעולות מנהל
admin_bp = Blueprint('admin', __name__)

#region מי מחכה לאישור
@admin_bp.route('/admin/pending-users', methods=['GET'])
@login_required
def get_pending_users():
    """
        צפייה ברשימת המשתמשים הממתינים לאישור (למנהלים בלבד)
        ---
        responses:
          200:
            description: רשימת משתמשים
            schema:
              type: array
              items:
                properties:
                  id:
                    type: integer
                  username:
                    type: string
          403:
            description: אין הרשאת מנהל
        """
    # קריאה ל-Service וקבלת הרשימה
    result, status_code = get_pending_users_service()
    return jsonify(result), status_code
#endregion

#region approve_user
@admin_bp.route('/admin/approve/<int:user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    """
    אישור משתמש לפי ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ה-ID של המשתמש לאישור
    responses:
      200:
        description: הצלחה
    """
    # קריאה ל-Service שמבצע את אישור המנהל (העברת ה-ID ישירות מה-URL)
    result, status_code = admin_approve_user_service(user_id)
    return jsonify(result), status_code
#endregion