from extensions import db
from datetime import datetime

class DuplicateLog(db.Model):
    __tablename__ = "duplicate_log"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    attempted_on = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    message = db.Column(db.String(255))
    
    def __repr__(self):
        return f"<DuplicateLog {self.student_id} - {self.company_id}>"