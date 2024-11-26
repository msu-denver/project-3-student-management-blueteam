'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): Emily, Kayleen, Benjamin, Dennis, Nahum
Description: Project 3 - Student Management
'''

from flask_login import UserMixin
from app import db
from datetime import date

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    about = db.Column(db.String)
    passwd = db.Column(db.LargeBinary)

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Major(id={self.id}, name='{self.name}')>"

class Student(db.Model):  
    __tablename__ = 'students' 
    enrollment_date = db.Column(db.Date, nullable=False, default=date.today)
    student_id = db.Column(db.String, primary_key=True)  
    student_name = db.Column(db.String, nullable=False)  
    academic_year = db.Column(db.String)  
    total_gpa = db.Column(db.Float, default=0.0)  
    total_credits = db.Column(db.Integer, default=0)  
    major = db.Column(db.String, nullable=False)  

    def __str__(self):
        return f'<Student(id={self.student_id}, name={self.student_name}, gpa={self.gpa}, credits={self.credits}, major={self.major})>'
    
class Grade(db.Model):
    __tablename__ = 'grades'

    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False, primary_key=True)
    semester= db.Column(db.String, nullable=False, primary_key=True)
    gpa = db.Column(db.Float, default=0.0)
    credits = db.Column(db.Integer, default=0)

    student = db.relationship('Student', backref=db.backref('grades', lazy=True))

    def __str__(self):
        return f"<Grade(student_id={self.student_id}, term='{self.semester}', gpa={self.gpa}, credits={self.credits})>"
