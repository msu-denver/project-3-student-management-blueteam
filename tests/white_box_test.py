import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app, db
from app.models import User, Major, Student, Grade


class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        user = User(id='1', name='Alice', about='Student', passwd=b'secret')
        db.session.add(user)
        db.session.commit()

        queried_user = User.query.filter_by(id='1').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.name, 'Alice')

    def test_major_model(self):
        major = Major(id=1, name='Computer Science')
        db.session.add(major)
        db.session.commit()

        queried_major = Major.query.filter_by(id=1).first()
        self.assertIsNotNone(queried_major)
        self.assertEqual(repr(queried_major), "<Major(id=1, name='Computer Science')>")

    def test_student_model(self):
        student = Student(
            student_id=101,
            student_name='Bob',
            academic_year='2023',
            total_gpa=3.5,
            total_credits=90,
            major='Computer Science'
        )
        db.session.add(student)
        db.session.commit()

        queried_student = Student.query.filter_by(student_id=101).first()
        self.assertIsNotNone(queried_student)
        self.assertEqual(queried_student.student_name, 'Bob')

    def test_grade_model(self):
        student = Student(
            student_id=102,
            student_name='Carol',
            academic_year='2024',
            total_gpa=3.8,
            total_credits=120,
            major='Mathematics'
        )
        db.session.add(student)
        db.session.commit()

        grade = Grade(
            student_id=102,
            semester='Fall 2023',
            gpa=3.9,
            credits=15
        )
        db.session.add(grade)
        db.session.commit()

        queried_grade = Grade.query.filter_by(student_id=102, semester='Fall 2023').first()
        self.assertIsNotNone(queried_grade)
        self.assertEqual(queried_grade.gpa, 3.9)
        self.assertEqual(queried_grade.credits, 15)


if __name__ == '__main__':
    unittest.main()