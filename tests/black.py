import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
 
class CreateStudentTest(unittest.TestCase):
 
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:5000/users/login')
 
    def test_create_student_success(self):
        """Testing that an admin can create a student."""
        self.login_as_admin()
        create_student_button = self.browser.find_element(By.XPATH, "//button[text()='Create Student']")
        create_student_button.click()
 
        random_student_id = self.generate_random_id()
        student_id = self.browser.find_element(By.ID, "student_id")
        student_id.send_keys(random_student_id)
 
        student_name = self.browser.find_element(By.ID, "student_name")
        student_name.send_keys("Test")
 
        academic_year = self.browser.find_element(By.ID, "academic_year")
        academic_year.send_keys("Junior")
 
        major = self.browser.find_element(By.ID, "major")
        major.send_keys("Computer Science")
 
        enrollment_date = self.browser.find_element(By.ID, "enrollment_date")
        self.browser.execute_script("arguments[0].value = '2022-08-01';", enrollment_date)
        self.assertEqual(enrollment_date.get_attribute('value'), "2022-08-01")
 
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.click()
 
        time.sleep(2)
        page = self.browser.current_url
        self.assertEqual('http://localhost:5000/students', page)
 
        students_list = self.browser.page_source
        self.assertIn("Test", students_list)
 
    def login_as_admin(self):
        """Helper function to log in as an admin user."""
        self.browser.get('http://localhost:5000/users/login')
 
        id_input = self.browser.find_element(By.ID, 'id')
        id_input.send_keys('123')
 
        password_input = self.browser.find_element(By.ID, 'passwd')
        password_input.send_keys('123')
 
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.click()
 
        time.sleep(2)
        page = self.browser.current_url
        self.assertEqual('http://localhost:5000/students', page)
 
    def generate_random_id(self):
        """Generate a random student ID."""
        return str(random.randint(1000, 9999))
 
if __name__ == '__main__':
    unittest.main()