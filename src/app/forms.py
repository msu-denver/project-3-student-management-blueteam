'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): Emily, Kayleen, Benjamin, Dennis, Nahum
Description: Project 3 - Student Management
'''

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, InputRequired, NumberRange

MAJORS = [
    'Accounting Major, B.S.',
    'Advanced Manufacturing Sciences Major, B.S.',
    'Africana Studies Major, B.A.',
    'Aging Services Leadership Major, B.S.',
    'Anthropology Major, B.A.',
    'Applied Geology Major, B.S.',
    'Art Education Major, B.F.A.',
    'Art History, Theory, and Criticism Major, B.A.',
    'Art Major, B.A.',
    'Art Major, B.F.A.',
    'Aviation and Aerospace Management (AAM) Major, B.S.',
    'Aviation and Aerospace Science (ASC) Major, B.S.',
    'Banking Major, B.S.',
    'Biochemistry Major, B.S.',
    'Biology Major, B.A.',
    'Biology Major, B.S.',
    'Brewery Operations Major, B.S.',
    'Broadcast Journalism Major, B.A.',
    'Business Administration Major, B.S.',
    'Business Intelligence Major, B.S.',
    'Chemistry Major, B.A.',
    'Chemistry Major, B.S.',
    'Chemistry Major for ACS Certified B.S.',
    'Chicano Studies Major, B.A.',
    'Civil Engineering Technology Major, B.S.',
    'Communication Design Major, B.F.A.',
    'Communication Studies Major, B.A.',
    'Computer Engineering Major, B.S.',
    'Computer Information Systems Major, B.S.',
    'Computer Science Major, B.S.',
    'Construction Project Management Major, B.A.',
    'Criminal Justice and Criminology Major, B.S.',
    'Cybersecurity Major, B.S.',
    'Dance Major, B.A.',
    'Data Science and Machine Learning Major, B.S.',
    'Early Childhood Education Major, B.A.',
    'Economics Major, B.A.',
    'Economics Major, B.S.',
    'Electrical Engineering Technology Major, B.S.',
    'Elementary Education Major, B.A.',
    'English Major, B.A.',
    'Entrepreneurship Major, B.A.',
    'Environmental Engineering Major, B.S.',
    'Environmental Science Major, B.S.',
    'Event and Meeting Management Major, B.S.',
    'Exercise Science Major, B.S.',
    'Extended Major in Journalism and Media Production, B.S.',
    'Finance Major, B.S.',
    'Fire and Emergency Response Administration, B.S.',
    'Fire and Emergency Response Administration Extended Major, B.S.',
    'Gender, Women, and Sexualities Studies Major, B.A.',
    'Geography Major, B.A.',
    'Geology - See Applied Geology Major, B.S.',
    'Global Business Studies Major, B.A.',
    'Health Care Information Systems, B.S.',
    'Health Care Management Major, B.S.',
    'Health Care Professional Services Major, B.S.',
    'History Major, B.A.',
    'Hospitality Leadership Major, B.S.',
    'Hotel Management Major, B.S.',
    'Human Development and Family Studies Major, B.A.',
    'Human Resource Management Major, B.S.',
    'Human Services Major, B.S.',
    'Industrial Design Major, B.S.',
    'Integrative Health Care Major, B.S.',
    'International Business Major, B.S.',
    'Journalism Major, B.A.',
    'K-12 Physical Education Major, B.S.',
    'Lifestyle Medicine Major, B.S.',
    'Lifestyle Medicine Extended Major, B.S.',
    'Linguistics Major, B.A.',
    'Management Major, B.S.',
    'Marketing Major, B.S.',
    'Mathematics Major, B.S.',
    'Mechanical Engineering Technology Major, B.S.',
    'Media Production and Leadership Major, B.S.',
    'Meteorology Major, B.S.',
    'Music Education, B.M.E.',
    'Music Major, B.A.',
    'Music Major, B.M.',
    'Nursing Major - Accelerated Nursing Option, B.S.N.',
    'Nursing Major - Baccalaureate Registered Nurse Completion Option, B.S.N.',
    'Nursing Major - Traditional Nursing Option, B.S.N.',
    'Nutrition and Dietetics Major, B.S.',
    'Nutrition Science Major, B.S.',
    'Nutrition Studies Major, B.S.',
    'Operations Management Major, B.S.',
    'Philosophy Major, B.A.',
    'Physics Major, B.A.',
    'Physics Major, B.S.',
    'Political Science Major, B.A.',
    'Professional Selling Major, B.A.',
    'Psychology Major, B.S.',
    'Public Health Major, B.A.',
    'Public Relations Major, B.S.',
    'Real Estate Major, B.S.',
    'Social Work Major, B.S.',
    'Sociology Major, B.A.',
    'Special Education Major, B.A.',
    'Speech, Language, Hearing Sciences Major, B.A.',
    'Sport Management Major, B.A.',
    'Statistical Science Major, B.S.',
    'Technical Writing and Editing Major, B.S.',
    'Theatre Major, B.A.',
    'Theatre Major, B.F.A.',
    'Video Production Major, B.S.'
]

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('About')
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class StudentForm(FlaskForm):
    enrollment_date = DateField('Enrollment Date', format='%Y-%m-%d', validators=[])
    student_id = StringField('Id',validators=[DataRequired()])
    student_name = StringField('Name')
    academic_year = SelectField('Academic Year', choices=[('', '-- Select --'),('freshman', 'Freshman'), ('sophomore', 'Sophomore'),('junior', 'Junior'),('senior', 'Senior')])
    total_gpa = FloatField('Total GPA')
    total_credits = IntegerField('Total Credits')
    major = SelectField('Major', choices=[("", "")])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.major.choices = [('', '-- Select --')] + [(major, major) for major in MAJORS]

class GradeForm(FlaskForm):
    semester = SelectField('Semester',choices=[],  validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[NumberRange(min=0.0, max=4.0)])
    credits = IntegerField('Credits', validators=[NumberRange(min=0, max=40)])
    submit = SubmitField('Submit')

    def __init__(self, academic_year=None, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        all_semesters = ['Freshman', 'Sophomore', 'Junior', 'Senior']
        
        if academic_year:
            formatted_year = academic_year.capitalize()
            if formatted_year in all_semesters:
                max_index = all_semesters.index(formatted_year)
                self.semester.choices = [(sem, sem) for sem in all_semesters[:max_index + 1]]
            else:
                self.semester.choices = [(sem, sem) for sem in all_semesters]
        else:
            self.semester.choices = [(sem, sem) for sem in all_semesters]

class StudentSearchForm(FlaskForm):
    student_id = StringField('Id')  
    student_name = StringField('Name')
    academic_year = SelectField('Academic Year', choices=[('', '-- Select --'), ('freshman', 'Freshman'), ('sophomore', 'Sophomore'), ('junior', 'Junior'), ('senior', 'Senior')])
    total_gpa = FloatField('Total GPA')
    total_credits = IntegerField('Total Credits')
    major = SelectField('Major', choices=[("", "-- Select --")] + [(major, major) for major in MAJORS])
    submit = SubmitField('Search')
