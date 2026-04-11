from app.models import db, User
from flask_login import current_user


#region מי מחכה לאישור
def get_pending_users_service():
    #  בדיקה שרק מנהל מבקש את הרשימה
    # אימות הכניסה נעשה בעבר טרם הכנת העוגיה ב-currentUser
    if current_user.role != 'Admin':
        return {"message": "Unauthorized"}, 403

    # שליפת כל המשתמשים שהם Uploader אבל is_approved_uploader הוא False
    pending_users = User.query.filter_by(role='Uploader', is_approved_uploader=False).all()

    # המרה לרשימת מילונים כדי שה-app יוכל להפוך אותם ל-JSON
    users_list = [
        {
            "id": u.id,
            "username": u.username,
            "role": u.role
        } for u in pending_users
    ]

    return users_list, 200


#endregion

#region admin_approve_user_service
def admin_approve_user_service(user_id):
    if current_user.role != 'Admin':
        return {"message": "Unauthorized. Admins only."}, 403

    user_to_approve = User.query.get(user_id)
    if not user_to_approve:
        return {"message": "User not found"}, 404

    if user_to_approve.role != 'Uploader':
        return {"message": "User did not request to be an Uploader"}, 400

    user_to_approve.is_approved_uploader = True

    try:
        db.session.commit()
        return {"message": f"User {user_to_approve.username} approved!"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error: {str(e)}"}, 500


#endregion