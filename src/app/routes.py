
from app import app, db
from app.models import User, Student, Grade
from app.forms import SignUpForm, LoginForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
from app.forms import StudentForm, GradeForm
from sqlalchemy.orm import joinedload
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
        id_exists = User.query.filter_by(id=form.id.data).first()
        if id_exists:
            return redirect(url_for('id_taken'))
        if form.passwd.data == form.passwd_confirm.data:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(form.passwd.data.encode(), salt)
            user = User(id=form.id.data, name=form.name.data, about=form.about.data, passwd=hashed_password) 
            db.session.add(user)
            db.session.commit()
                        
            return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/users/useridtaken', methods=['GET', 'POST'])
def id_taken():
    return render_template('useridtaken.html')

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

@app.route('/users/login_error', methods=['GET', 'POST'])
def login_error():
    return render_template('login_error.html')

@login_required
@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()  
    return redirect(url_for('index'))

@login_required
@app.route('/students')
def list_student():
    form = StudentForm()

    student_id = request.args.get('student_id')
    student_name = request.args.get('student_name')
    academic_year = request.args.get('academic_year')
    total_gpa = request.args.get('total_gpa', type=float)
    total_credits = request.args.get('total_credits', type=int)
    major = request.args.get('major')

    page = request.args.get('page', 1, type=int)
    per_page = 10  

    query = Student.query

    if student_id:
        query = query.filter(Student.student_id.like(f"%{student_id}%"))
    if student_name:
        query = query.filter(Student.student_name.like(f"%{student_name}%"))
    if academic_year:
        query = query.filter(Student.academic_year == academic_year)
    if total_gpa is not None:
        query = query.filter(Student.total_gpa == total_gpa)
    if total_credits is not None:
        query = query.filter(Student.total_credits == total_credits)
    if major:
        query = query.filter(Student.major == major)

    students = query.paginate(page=page, per_page=per_page)

    total_pages = students.pages

    return render_template('list_students.html', form=form, students=students, current_page=page, total_pages=total_pages)

@login_required
@app.route('/students/create', methods=['GET', 'POST'])
def create_student():
    form = StudentForm()

    if form.validate_on_submit():
        existing_student = Student.query.filter_by(student_id=form.student_id.data).first()
        if existing_student:
            flash(f"Student ID {form.student_id.data} already exists. Please use a unique ID.", "error")
            return render_template('create_student.html', form=form)

        new_student = Student(
            student_id=form.student_id.data,
            student_name=form.student_name.data,
            academic_year=form.academic_year.data,
            major=form.major.data,
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('list_student'))

    return render_template('create_student.html', form=form)

@login_required
@app.route('/students/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    return "still working"

@login_required
@app.route('/students/search', methods=['GET', 'POST'])
def search_student():
    return "still working"

@login_required
@app.route('/students/<int:id>/delete', methods=['GET', 'POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)

    try:
        Grade.query.filter_by(student_id=id).delete()

        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting student: {str(e)}", "error")

    return redirect(url_for('list_student'))

#All of the following functions are graduation parts
@login_required
@app.route('/students/<int:student_id>/grades', methods=['GET', 'POST'])
def manage_grades(student_id):
    return "still working"

@login_required
@app.route('/students/<int:student_id>/graduation', methods=['GET'])
def view_transcript(student_id):
    return "still working"


@login_required
@app.route('/students/<int:student_id>/graduation_check', methods=['POST'])
def graduation_check(student_id):
    return "still working"
