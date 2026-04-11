import os


class Config:
    # ה-config מילון הגדרות הפרויקט הוא מחזיק במיקום של ה-db
    # הגדרות בסיס נתונים ומפתח סודי (חובה עבור Flask-Login)

    # שימוש ב-OS כדי למצוא את הנתיב המוחלט של הפרויקט
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'recipes.db')

  #כרגע לא נתתי מפתח במשתני הסביבה אך רעיונית ספרית OS היתה מאפשרת לי לשפר את רמת האבטחה
  #כך שהמפתח לא יהיה גלוי לכל בתוך הקוד,
  # בפיתוח מוצר אמיתי שעולה לפפרודקשין  האם מקובל ליצור מפתח רנדומלי ומסובך במשתנה מחוץ לקוד ולנהל אותו עם ספרית OS?
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'

    # מניעת התראות מיותרות של SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False