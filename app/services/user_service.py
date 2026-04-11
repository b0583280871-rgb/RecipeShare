from app.models import db
from flask_login import current_user

#region request_upgrade_service
def request_upgrade_service():
    if current_user.role == 'Admin' or current_user.role == 'Uploader' and current_user.is_approved_uploader:
        return {"message": "Admins don't need upgrades"}, 400

    current_user.role = 'Uploader'
    current_user.is_approved_uploader = False  # ממתין לאישור

    try:
        db.session.commit()
        return {"message": "Upgrade request submitted to Admin"}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error: {str(e)}"}, 500


#endregion