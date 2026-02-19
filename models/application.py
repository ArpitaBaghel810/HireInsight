from extensions import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = "applications"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    # Application Details
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Applied')  # Applied, Shortlisted, Rejected, Selected
    remarks = db.Column(db.Text)
    
    # Selection Details
    selection_date = db.Column(db.DateTime)
    interview_date = db.Column(db.DateTime)
    interview_mode = db.Column(db.String(50))
    interview_rounds = db.Column(db.Integer, default=1)
    current_round = db.Column(db.Integer, default=1)
    
    # Feedback
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5
    
    # Unique constraint to prevent duplicate applications
    __table_args__ = (db.UniqueConstraint('student_id', 'company_id', name='unique_application'),)
    
    def __repr__(self):
        return f"<Application {self.student_id} - {self.company_id}>"