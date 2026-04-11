from app import create_app

# יצירת האפליקציה דרך ה-Factory
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)