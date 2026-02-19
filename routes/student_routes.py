from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.student import Student
from models.company import Company
from models.application import Application
from models.skills import StudentSkill, CompanySkill
from models.duplicate_log import DuplicateLog
from datetime import datetime
import json

student_bp = Blueprint("student", __name__)

@student_bp.route("/dashboard")
@login_required
def dashboard():
    # Get all active companies
    companies = Company.query.filter_by(is_active=True).all()
    
    # Get student's applications
    applications = Application.query.filter_by(student_id=current_user.id).all()
    
    # Get student's skills
    student_skills = StudentSkill.query.filter_by(student_id=current_user.id).all()
    
    # Calculate overall skill match percentage (average across all companies)
    total_match = 0
    count = 0
    for company in companies:
        match = current_user.get_skill_match_percentage(company.id)
        if match > 0:
            total_match += match
            count += 1
    skill_match_percentage = (total_match / count) if count > 0 else 0
    
    return render_template(
        "student/dashboard.html",
        companies=companies,
        applications=applications,
        student_skills=student_skills,
        skill_match_percentage=round(skill_match_percentage)
    )

@student_bp.route("/update-profile", methods=["POST"])
@login_required
def update_profile():
    try:
        # Update student profile with form data
        current_user.phone = request.form.get('phone')
        current_user.enrollment_no = request.form.get('enrollment_no')
        current_user.branch = request.form.get('branch')
        current_user.semester = request.form.get('semester', type=int)
        current_user.cgpa = request.form.get('cgpa', type=float)
        current_user.tenth_percentage = request.form.get('tenth_percentage', type=float)
        current_user.twelfth_percentage = request.form.get('twelfth_percentage', type=float)
        current_user.graduation_year = request.form.get('graduation_year', type=int)
        current_user.backlog = request.form.get('backlog', type=int, default=0)
        current_user.linkedin_url = request.form.get('linkedin_url')
        current_user.github_url = request.form.get('github_url')
        current_user.leetcode_url = request.form.get('leetcode_url')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
    except Exception as e:
        flash('Error updating profile: ' + str(e), 'danger')
    
    return redirect(url_for('student.dashboard'))

@student_bp.route("/add-skill", methods=["POST"])
@login_required
def add_skill():
    try:
        skill_name = request.form.get('skill_name')
        proficiency = request.form.get('proficiency', type=int, default=3)
        years_experience = request.form.get('years_experience', type=float, default=0)
        
        # Check if skill already exists
        existing = StudentSkill.query.filter_by(
            student_id=current_user.id,
            skill_name=skill_name
        ).first()
        
        if existing:
            flash('Skill already added!', 'warning')
        else:
            skill = StudentSkill(
                student_id=current_user.id,
                skill_name=skill_name,
                proficiency=proficiency,
                years_experience=years_experience
            )
            db.session.add(skill)
            db.session.commit()
            flash('Skill added successfully!', 'success')
    except Exception as e:
        flash('Error adding skill: ' + str(e), 'danger')
    
    return redirect(url_for('student.dashboard'))

@student_bp.route("/remove-skill", methods=["POST"])
@login_required
def remove_skill():
    try:
        data = request.get_json()
        skill_id = data.get('skill_id')
        
        skill = StudentSkill.query.filter_by(
            id=skill_id,
            student_id=current_user.id
        ).first()
        
        if skill:
            db.session.delete(skill)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Skill not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@student_bp.route("/apply", methods=["POST"])
@login_required
def apply_company():
    try:
        data = request.get_json()
        company_id = data.get('company_id')
        
        # Check if already applied
        existing = Application.query.filter_by(
            student_id=current_user.id,
            company_id=company_id
        ).first()
        
        if existing:
            # Log duplicate attempt
            log = DuplicateLog(
                student_id=current_user.id,
                company_id=company_id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent'),
                message='Duplicate application attempt'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'message': 'You have already applied for this company!'
            })
        
        # Check eligibility
        company = Company.query.get(company_id)
        if not company.is_eligible(current_user):
            return jsonify({
                'success': False,
                'message': 'You are not eligible for this company!'
            })
        
        # Create application
        application = Application(
            student_id=current_user.id,
            company_id=company_id,
            status='Applied'
        )
        db.session.add(application)
        
        # Update company applications count
        company.total_applications += 1
        
        db.session.commit()
        
        # Calculate skill match for feedback
        match_percentage = current_user.get_skill_match_percentage(company_id)
        missing_skills = current_user.get_missing_skills(company_id)
        
        message = f'Application submitted successfully!'
        if missing_skills:
            message += f' Consider improving: {", ".join(missing_skills[:3])}'
        
        return jsonify({
            'success': True,
            'message': message,
            'match_percentage': match_percentage
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@student_bp.route("/application/<int:application_id>")
@login_required
def view_application(application_id):
    application = Application.query.filter_by(
        id=application_id,
        student_id=current_user.id
    ).first_or_404()
    
    return render_template("student/application.html", application=application)