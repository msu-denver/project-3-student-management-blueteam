# Sprint Planning

Date/Time: 11/14/24--08:00pm

Participants: Emily, Kayleen, Benjamin, Dennis, Nahum

Goal Statement: The Goal For sprint 1 is to develop a good understanding of our project through completion of all user story descriptions and uml diagrams, making adjustments as we solidify our vision for the project. US#1, US#2, US#4, and US#6 are expected to be achieved during this sprint.

US#1 User Registration (sign up):
To enable users to interact with the platform, the first feature to implement is user registration. In this user story, we will implement a registration form where users can create an account by providing a user ID, name, a short description, and a password. Upon submitting the form, the information will be saved in the database, creating a unique profile for each user. This feature is foundational for ensuring secure access to the platform and will be thoroughly tested for valid input, error handling, and proper data storage.

US#2 User Authentication (Log in):
The next critical functionality is user authentication, which allows registered users to access the platform. This story will focus on implementing a login form that verifies the user’s credentials (user ID and password) against the records stored in the database. Successful login will grant users access to explore and interact with the app, while failed attempts will be handled with appropriate error messages.

US#4 List Student Inforamtioon:
In this user story, we will implement a listing table where users can view student information filtered by their search criteria. The table will display a limited number of students per page, with pagination controls. This setup enables users to efficiently review data without overwhelming the interface.

US#6 Delete a Students Information:
Maintaining data accuracy sometimes requires the removal of outdated or incorrect entries. In this user story, administrators will be able to delete incidents by specifying the incident’s unique ID. A confirmation prompt will ensure that deletions are intentional, preventing accidental loss of data. This feature is essential for effective database management and keeping the repository clean and reliable. Testing will ensure that deletions work as expected and maintain data integrity across the platform.