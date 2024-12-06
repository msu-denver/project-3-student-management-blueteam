'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): Emily, Kayleen, Benjamin, Dennis, Nahum
Description: Project 3 - Student Management
'''

from app import app, db
from app.models import User, Student, Grade
from app.forms import SignUpForm, LoginForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import StudentForm, GradeForm, StudentSearchForm
from sqlalchemy import cast
from sqlalchemy.types import String
import bcrypt


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Check if user ID already exists
        id_exists = User.query.filter_by(id=form.id.data).first()
        if id_exists:
            return redirect(url_for('id_taken'))
        # Ensure passwords match
        if form.passwd.data == form.passwd_confirm.data:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.passwd.data.encode(), salt)
            # Create a new user
            user = User(id=form.id.data, name=form.name.data,
                        about=form.about.data, passwd=hashed_password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('signup.html', form=form)

# Route displayed when the user ID is already taken


@app.route('/users/useridtaken', methods=['GET', 'POST'])
def id_taken():
    return render_template('useridtaken.html')

# User login route


@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user:
            if user and bcrypt.checkpw(form.passwd.data.encode(), user.passwd):
                login_user(user)
                return redirect(url_for('list_student'))
            else:
                return redirect(url_for('login_error'))

    return render_template('login.html', form=form)

# Route displayed when login fails


@app.route('/users/login_error', methods=['GET', 'POST'])
def login_error():
    return render_template('login_error.html')

# User logout route


@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

# Route to list all students


@login_required
@app.route('/students')
def list_student():
    form = StudentForm()

    # Retrieve query parameters from the request
    student_id = request.args.get('student_id')
    student_name = request.args.get('student_name')
    academic_year = request.args.get('academic_year')
    major = request.args.get('major')
    total_gpa = request.args.get('total_gpa', type=float)
    total_credits = request.args.get('total_credits', type=int)
    enrollment_date = request.args.get('enrollment_date')

    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Build query
    query = Student.query

    if student_id:
        query = query.filter(
            cast(Student.student_id, String).like(f"%{student_id}%"))
    if student_name:
        query = query.filter(Student.student_name.like(f"%{student_name}%"))
    if academic_year:
        query = query.filter(Student.academic_year == academic_year)
    if major:
        query = query.filter(Student.major == major)
    if total_gpa is not None:
        query = query.filter(Student.total_gpa == total_gpa)
    if total_credits is not None:
        query = query.filter(Student.total_credits == total_credits)
    if enrollment_date:
        query = query.filter(Student.enrollment_date == enrollment_date)

    # Paginate results
    students = query.paginate(page=page, per_page=per_page)

    return render_template(
        'list_students.html',
        form=form,
        students=students,
        current_page=page,
        total_pages=students.pages,
    )


# Users classified as Admin //put your id to test create incident
admin_user_ids = ["111", '123', "admin_user3"]


# Route to create a new student
@login_required
@app.route('/students/create', methods=['GET', 'POST'])
def create_student():
    # Restrict access to administrators
    if current_user.id not in admin_user_ids:
        flash('Only Administrators can create student information.', 'error')
        return redirect(url_for('list_student'))

    form = StudentForm()

    if form.validate_on_submit():
        # Check if the student ID is unique
        existing_student = Student.query.filter_by(
            student_id=form.student_id.data).first()
        if existing_student:
            flash(
                f"Student ID {form.student_id.data} already exists. "
                "Please use a unique ID.",
                "error"
            )
            return render_template('create_student.html', form=form)

        # Create new student
        new_student = Student(
            student_id=form.student_id.data,
            student_name=form.student_name.data,
            academic_year=form.academic_year.data,
            major=form.major.data,
            enrollment_date=form.enrollment_date.data
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('list_student'))

    return render_template('create_student.html', form=form)

# Route to update an existing student's details


@login_required
@app.route('/students/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    # Restrict access to administrators
    if current_user.id not in admin_user_ids:
        flash('Only Administrators can update student.', 'error')
        return redirect(url_for('list_student'))

    student = Student.query.get_or_404(id)  # Get student by ID or return 404

    form = StudentForm(obj=student)  # Pre-fill form with student data

    if form.validate_on_submit():
        # Update student details
        student.student_name = form.student_name.data
        student.academic_year = form.academic_year.data
        student.major = form.major.data

        try:
            db.session.commit()
            flash("Student updated successfully!", "success")
            return redirect(url_for('list_student'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating student: {str(e)}", "error")

    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {field} field - {error}", "error")

    return render_template('update_student.html', form=form, student=student)

# Route to search for students based on various criteria


@login_required
@app.route('/students/search', methods=['GET', 'POST'])
def search_student():
    form = StudentSearchForm()

    if form.validate_on_submit():
        search_params = {}

        # Collect search parameters from the form
        if form.student_id.data:
            search_params['student_id'] = form.student_id.data.strip()
        if form.student_name.data:
            search_params['student_name'] = form.student_name.data.strip()
        if (
            form.academic_year.data
            and form.academic_year.data != '-- Select --'
        ):
            search_params['academic_year'] = form.academic_year.data
        if form.major.data and form.major.data != '-- Select --':
            search_params['major'] = form.major.data
        if form.total_gpa.data is not None:
            search_params['total_gpa'] = form.total_gpa.data
        if form.total_credits.data is not None:
            search_params['total_credits'] = form.total_credits.data

        # Redirect to list_students with the search parameters
        if search_params:
            return redirect(url_for('list_student', **search_params))
        else:
            flash("Please provide at least one search criterion.", "warning")

    return render_template('search_student.html', form=form)

# Route to delete a student


@login_required
@app.route('/students/<int:id>/delete', methods=['GET', 'POST'])
def delete_student(id):
    # Restrict access to administrators
    if current_user.id not in admin_user_ids:
        flash('Only Administrators can delete student.', 'error')
        return redirect(url_for('list_student'))

    student = Student.query.get_or_404(id)
    try:
        # Delete associated grades first
        Grade.query.filter_by(student_id=id).delete()

        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting student: {str(e)}", "error")

    return redirect(url_for('list_student'))

# All of the following functions are graduation parts
# Helper function to calculate total GPA and credits


def calculate_totals(grades):
    total_gpa = sum(grade.gpa for grade in grades) / len(grades)
    total_credits = sum(grade.credits for grade in grades)
    return total_gpa, total_credits

# Helper function to check graduation eligibility


def check_graduation_eligibility(total_gpa, total_credits):
    return total_gpa >= 2.0 and total_credits >= 120

# Route to manage grades for a specific student


@login_required
@app.route('/students/<int:student_id>/grades', methods=['GET', 'POST'])
def manage_grades(student_id):
    # Restrict access to administrators
    if current_user.id not in admin_user_ids:
        flash('Only Administrators can manage grades.', 'error')
        return redirect(url_for('list_student'))

    student = Student.query.get_or_404(student_id)
    form = GradeForm()

    all_semesters = ['Freshman', 'Sophomore', 'Junior', 'Senior']

    current_academic_year = student.academic_year.capitalize()

    grades = Grade.query.filter_by(student_id=student_id).all()

    if request.method == 'POST' and form.validate_on_submit():
        # Ensure the semester is within the student's academic year
        if form.semester.data not in all_semesters[:all_semesters.index(
                current_academic_year) + 1]:
            flash(
                f"You cannot add grades for {form.semester.data} it is beyond "
                "the student's academic year.",
                "error"
            )
            return render_template('manage_grades.html',
                                   student=student, grades=grades, form=form)

        # Check if the grade for this semester already exists
        grade = Grade.query.filter_by(
            student_id=student_id, semester=form.semester.data).first()
        if grade:
            grade.gpa = form.gpa.data
            grade.credits = form.credits.data
            flash(f"Updated grade for {form.semester.data}.", "success")
        else:
            # Add a new grade
            new_grade = Grade(
                student_id=student_id,
                semester=form.semester.data,
                gpa=form.gpa.data,
                credits=form.credits.data
            )
            db.session.add(new_grade)
            flash(f"Added new grade for {form.semester.data}.", "success")

        db.session.commit()
        return redirect(url_for('manage_grades', student_id=student_id))

    return render_template('manage_grades.html',
                           student=student, grades=grades, form=form)

# Route to view a student's transcript


@login_required
@app.route('/students/<int:student_id>/graduation', methods=['GET'])
def view_transcript(student_id):

    student = Student.query.get_or_404(student_id)

    grades = Grade.query.filter_by(student_id=student_id).all()

    # Add default grades for all semesters if grades are missing
    if not grades:
        grades = [
            Grade(
                student_id=student_id,
                semester='Freshman',
                gpa=0.0,
                credits=0),
            Grade(
                student_id=student_id,
                semester='Sophomore',
                gpa=0.0,
                credits=0),
            Grade(
                student_id=student_id,
                semester='Junior',
                gpa=0.0,
                credits=0),
            Grade(
                student_id=student_id,
                semester='Senior',
                gpa=0.0,
                credits=0),
        ]

    # Calculate total GPA and credits
    total_gpa = sum(grade.gpa for grade in grades) / len(grades)
    total_credits = sum(grade.credits for grade in grades)

    # Update student's total GPA and credits
    student.total_gpa = total_gpa
    student.total_credits = total_credits
    db.session.commit()

    return render_template('transcript.html', student=student,
                           grades=grades,
                           total_gpa=total_gpa,
                           total_credits=total_credits)


# Route to check graduation eligibility for a student
@login_required
@app.route('/students/<int:student_id>/graduation_check', methods=['POST'])
def graduation_check(student_id):

    student = Student.query.get_or_404(student_id)

    # Check eligibility criteria
    is_senior = student.academic_year == 'senior'
    meets_gpa = student.total_gpa >= 2.0
    meets_credits = student.total_credits >= 120

    eligible = is_senior and meets_gpa and meets_credits

    return {"eligible": eligible}, 200
