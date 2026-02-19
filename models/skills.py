from extensions import db

class StudentSkill(db.Model):
    __tablename__ = "student_skills"
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer, default=3)  # 1-5
    years_experience = db.Column(db.Float, default=0)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'skill_name', name='unique_student_skill'),)
    
    def __repr__(self):
        return f"<StudentSkill {self.skill_name}>"

class CompanySkill(db.Model):
    __tablename__ = "company_skills"
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    required_skill = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    
    __table_args__ = (db.UniqueConstraint('company_id', 'required_skill', name='unique_company_skill'),)
    
    def __repr__(self):
        return f"<CompanySkill {self.required_skill}>"