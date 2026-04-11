from flask import Blueprint, request, jsonify
from flask_login import login_required
# ייבוא ה-Services הרלוונטיים מהתיקייה החדשה
from app.services.auth_service import register_user_service, login_user_service, logout_user_service
from app.services.user_service import request_upgrade_service

auth_bp = Blueprint('auth', __name__)

#region register
@auth_bp.route('/register', methods=['POST'])
def register():
    """
        רישום משתמש חדש
        ---
        tags:
          - Auth
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: UserRegistration
              required:
                - username
                - email
                - password
              properties:
                username:
                  type: string
                  example: user123
                email:
                  type: string
                  example: user@example.com
                password:
                  type: string
                  example: password123
                role:
                  type: string
                  enum: ['Reader', 'Uploader']
                  default: 'Reader'
        responses:
          201:
            description: משתמש נוצר בהצלחה
          400:
            description: חסרים נתונים
          409:
            description: המייל כבר קיים במערכת
        """
    data = request.get_json()
    result, status_code = register_user_service(data)
    return jsonify(result), status_code
#endregion

#region login
@auth_bp.route('/login', methods=['POST'])
def login():
    """
        התחברות למערכת
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              properties:
                email:
                  type: string
                  default: "admin@example.com"
                password:
                  type: string
                  default: "123456"
        responses:
          200:
            description: התחברות הצליחה
        """
    data = request.get_json()
    result, status_code = login_user_service(data)
    return jsonify(result), status_code
#endregion

#region logout
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
        התנתקות מהמערכת
        ---
        responses:
          200:
            description: התנתקת בהצלחה
          401:
            description: לא היית מחובר מלכתחילה
        """
    result, status_code = logout_user_service()
    return jsonify(result), status_code
#endregion

#region upgrade_request
@auth_bp.route('/upgrade-request', methods=['POST'])
@login_required
def upgrade_request():
    """
        בקשת משתמש להפוך ל-Uploader (מעלה מתכונים)
        ---
        responses:
          200:
            description: הבקשה נשלחה למנהל
          401:
            description: משתמש לא מחובר
        """
    # קריאה ל-Service שמבצע את בקשת השדרוג
    result, status_code = request_upgrade_service()
    return jsonify(result), status_code
#endregion