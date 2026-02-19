from flask import Flask, render_template
from config import Config
from extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access this page."
    
    # Import models for user_loader
    from models.student import Student
    
    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    
    # Home route
    @app.route("/")
    def home():
        return render_template("index.html")
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)