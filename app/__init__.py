from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flasgger import Swagger
from app.models import db, User
from .config import Config

# הגדרת Flask-Login מחוץ לפונקציה כדי שיהיה נגיש לשאר חלקי המערכת
login_manager = LoginManager()


def create_app():
    # region טעינה ראשונית
    app = Flask(__name__)

    # טעינת ההגדרות מקובץ ה-config
    app.config.from_object(Config)

    # אתחול מסד הנתונים והכלים הנוספים על האפליקציה
    db.init_app(app)
    Swagger(app)
    login_manager.init_app(app)

    # פונקציה שאומרת ל-Flask איך למצוא משתמש לפי ה-ID שלו
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # רישום ה-Blueprints (הנתיבים המפוצלים)
    from app.routes.auth_routes import auth_bp
    from app.routes.recipe_routes import recipe_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(admin_bp)

    # יצירת הטבלאות בתוך הקשר האפליקציה
    with app.app_context():
        db.create_all()

        # ייבוא ה-Service של המתכונים לצורך טעינת ה-Cache
        from app.services.recipy_service import load_recipes_to_cache

        # בכל טעינה מחודשת אנו מעכנים את הcache בכל המתכונים הקימים בdb
        load_recipes_to_cache()
        print("Database tables created/verified successfully!")

    # endregion

    return app