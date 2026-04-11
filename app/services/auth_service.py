from app.models import db, User
from flask_login import login_user, logout_user

#region register

def register_user_service(data):
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return {"message": "Missing username, email or password"}, 400

    username = data['username']
    password = data['password']
    email = data['email'] # <--- שינוי: שליפת המייל מהנתונים

    # Whitelist לתפקידים - מונע הרשמת Admin
    requested_role = data.get('role', 'Reader')
    role = requested_role if requested_role in ['Reader', 'Uploader'] else 'Reader'

    # 2. שינוי השאילתה: בודקים ייחודיות לפי מייל במקום לפי שם משתמש
    if User.query.filter_by(email=email).first():
        return {"message": "Email already registered"}, 409

    # 3. יצירת האובייקט: הוספת שדה ה-email לתוך בניית המשתמש החדש
    new_user = User(
        username = username,
        email = email,       # <--- שינוי: הוספת המייל לאובייקט
        role = role,
        is_approved_uploader = False
    )
    new_user.set_password(password)

    try:
        new_user.save()
        # עדכון הודעת ההצלחה שתכלול גם את המייל
        return {"message": f"User {username} registered successfully with email {email}"}, 201
    except Exception as e:
        return {"message": f"Error: {str(e)}"}, 500

#endregion

#region login

def login_user_service(data):
    email = data.get('email')
    password = data.get('password')

    # אימות לוגי
    # איך נעשית השוואת הסיסמאות אם אין דרך חזור מסיסמה מגובבת?
    # שולח לפונקצית chack המקומית את הערך הנקי ומשווה את הסיסמאות ע"י אלגוריתם  של פרוק המלח מהמגובב ושילובו עם החדש, אם יוצא אותו דבר אזי הסיסמה נכונה
    # בשביל לעלות על הסיסמאות צריך גם לשלוף מה-db את הסיסמה המגובבת לאותו משתמש וגם לדעת מה היתה הסיסמה המקורית שלו וגם לדעת את נוסחת הגיבוב
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user)

        if user.role == 'Uploader' and not user.is_approved_uploader:
            display_role = 'Reader'
        else:
            display_role = user.role

        return {
            "message": f"Welcome back, {user.username}!",
            "role": display_role  # מחזירים את התפקיד המאושר בלבד
        }, 200

    return {"message": "Invalid email or password"}, 401


#endregion

#region logout
def logout_user_service():
    logout_user()
    return {"message": "Logged out successfully"}, 200


#endregion
