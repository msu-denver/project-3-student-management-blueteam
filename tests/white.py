import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from app.models import Student
 
class StudentTestCase(unittest.TestCase):
 
    #pre-condition: information for a new student, Jane Doe, is created
    #post-condition: Jane Doe's information is in the database
    def test_create_student_information(self):
        s=Student(
            student_name="Jane Doe",
            academic_year="Freshman",
            total_gpa=3.5,
            total_credits=12,
            major="Computer Science"
            )
       
        self.assertEqual("Jane Doe",s.student_name)
        self.assertEqual("Freshman",s.academic_year)
        self.assertEqual(3.5,s.total_gpa)
        self.assertEqual(12,s.total_credits)
        self.assertEqual("Computer Science",s.major)
if __name__ == '__main__':
    unittest.main()