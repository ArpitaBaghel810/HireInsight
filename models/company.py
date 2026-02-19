from extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = "companies"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(500))
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    
    # Job Details
    role = db.Column(db.String(100), nullable=False)
    package = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(50))  # Full Time, Internship
    
    # Requirements
    eligibility_cgpa = db.Column(db.Float, default=0.0)
    eligible_branches = db.Column(db.String(500))  # Comma separated
    required_skills_text = db.Column(db.Text)
    
    # Visit Details
    visit_date = db.Column(db.Date)
    last_date = db.Column(db.Date)
    drive_mode = db.Column(db.String(50))  # Online/Offline
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    total_applications = db.Column(db.Integer, default=0)
    selected_students = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    required_skills = db.relationship('CompanySkill', backref='company', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Company {self.name}>"
    
    def is_eligible(self, student):
        """Check if student is eligible for this company"""
        if student.cgpa < self.eligibility_cgpa:
            return False
        
        if self.eligible_branches and student.branch:
            branches = [b.strip() for b in self.eligible_branches.split(',')]
            if student.branch not in branches:
                return False
        
        return True