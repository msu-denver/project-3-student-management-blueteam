
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime

driver = webdriver.Edge()

try:
    driver.get("http://127.0.0.1:5000/users/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'id')))
    driver.find_element(By.NAME, 'id').send_keys("123")
    driver.find_element(By.NAME, 'passwd').send_keys("123")
    driver.find_element(By.NAME, 'submit').click()
    WebDriverWait(driver, 10).until(EC.url_contains("/students"))
    print("Login successful.")

    driver.get("http://127.0.0.1:5000/students/create")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'student_id')))
    print("Create Student page loaded successfully.")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'enrollment_date')))
    driver.execute_script("document.getElementById('enrollment_date').value = '2024-01-02';")
    print("Date field located and value set.")

    driver.find_element(By.NAME, 'student_id').send_keys("2024001")
    print("Student ID entered.")

    driver.find_element(By.NAME, 'student_name').send_keys("Test Student")
    print("Student Name entered.")

    academic_year_select = Select(driver.find_element(By.NAME, 'academic_year'))
    academic_year_select.select_by_visible_text("Freshman")
    print("Academic Year selected.")

    major_select = Select(driver.find_element(By.NAME, 'major'))
    major_select.select_by_visible_text("Computer Science Major, B.S.")
    print("Major selected.")

    submit_button = driver.find_element(By.NAME, 'submit')
    submit_button.click()
    print("Form submitted.")

except Exception as e:
    print(f"Test failed: {e}")
    print("Current URL:", driver.current_url)
    print("Page source at failure:")
    print(driver.page_source)

finally:
    driver.quit()