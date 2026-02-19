from app import create_app
from extensions import db
from models.company import Company
from models.skills import CompanySkill
from datetime import datetime, date

app = create_app()
with app.app_context():
    # Sample companies
    companies = [
        {
            'name': 'Google',
            'description': 'Leading technology company specializing in internet services',
            'role': 'Software Engineer',
            'package': 45.0,
            'location': 'Bangalore',
            'eligibility_cgpa': 7.5,
            'eligible_branches': 'CSE,IT,ECE',
            'visit_date': date(2024, 3, 15),
            'last_date': date(2024, 3, 10),
            'skills': ['Python', 'Java', 'Data Structures', 'Algorithms', 'System Design']
        },
        {
            'name': 'Microsoft',
            'description': 'Global leader in software and cloud services',
            'role': 'Software Development Engineer',
            'package': 42.0,
            'location': 'Hyderabad',
            'eligibility_cgpa': 7.0,
            'eligible_branches': 'CSE,IT,ECE,EEE',
            'visit_date': date(2024, 3, 20),
            'last_date': date(2024, 3, 15),
            'skills': ['C++', 'C#', 'Python', 'Azure', 'SQL']
        },
        {
            'name': 'Amazon',
            'description': 'E-commerce and cloud computing giant',
            'role': 'SDE Intern',
            'package': 35.0,
            'location': 'Chennai',
            'eligibility_cgpa': 7.0,
            'eligible_branches': 'CSE,IT',
            'visit_date': date(2024, 3, 25),
            'last_date': date(2024, 3, 20),
            'skills': ['Java', 'Python', 'AWS', 'Django', 'JavaScript']
        },
        {
            'name': 'Goldman Sachs',
            'description': 'Global investment banking firm',
            'role': 'Analyst',
            'package': 38.0,
            'location': 'Bangalore',
            'eligibility_cgpa': 8.0,
            'eligible_branches': 'CSE,IT,ECE',
            'visit_date': date(2024, 4, 5),
            'last_date': date(2024, 3, 30),
            'skills': ['Python', 'SQL', 'Excel', 'Financial Modeling', 'Statistics']
        },
        {
            'name': 'Flipkart',
            'description': 'Leading e-commerce company',
            'role': 'Software Developer',
            'package': 28.0,
            'location': 'Bangalore',
            'eligibility_cgpa': 6.5,
            'eligible_branches': 'CSE,IT',
            'visit_date': date(2024, 4, 10),
            'last_date': date(2024, 4, 5),
            'skills': ['Java', 'Spring Boot', 'React', 'MySQL', 'Redis']
        }
    ]
    
    for comp_data in companies:
        skills = comp_data.pop('skills')
        
        # Check if company already exists
        existing = Company.query.filter_by(name=comp_data['name']).first()
        if existing:
            print(f"Company {comp_data['name']} already exists")
            continue
            
        company = Company(**comp_data)
        db.session.add(company)
        db.session.flush()  # Get company id
        
        # Add required skills
        for skill_name in skills:
            skill = CompanySkill(
                company_id=company.id,
                required_skill=skill_name,
                priority='High'
            )
            db.session.add(skill)
        
        print(f"Added company: {company.name}")
    
    db.session.commit()
    print("Sample companies added successfully!")