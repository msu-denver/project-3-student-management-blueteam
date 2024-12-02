# Overview

Use this section to outline the vision for the product, including a **use case diagram** that illustrates the main user interactions. This will provide readers with a comprehensive overview of the project.

## The Vision

Managing student records is a often unecessarily difficult yet crucial task for educational institutions. Imagine a web app that tranfroms this process by innovating the way we store, search, and manage student information. Doing so more efficiently and providing an easy to use interface. This tool will be crucial in simplifying student management for educational institutions.

# Design

## User Stories

Describe the **user stories** for the project, ensuring each includes clear **acceptance criteria** and a **point estimate**. The **user stories** must align with the **use case diagram** and should be referred to as US#1, US#2, etc. 

## US#1: User Registration (sign up)

As a user, I want to register on the platform to search and view the database of students. When I provide all the required information (user ID, name, a short description, and password) and click 'submit', my account should be created. Additionally, some users will be configured as administrators offline.

```
TODO: estimate of effort in terms of user story points: 1
```

## US#2: User Authentication (Log in)

As a registered user, I want to log in to the platform. When I enter my user ID and password, the system should verify my credentials. If they match the records in the database, I should be granted access to navigate the app.

```
TODO: estimate of effort in terms of user story points: 1
```

## US#3: Search Student Information

As a registered user, I want to search for information by student name, student id, major, and academic year. When I enter my search parameters and click 'confirm', I should be redirected to a section of the application (see US#4) that display's the information by my criteria.

```
TODO: estimate of effort in terms of user story points: 3
```

## US#4: List Student Inforamtion

As a registered user, I want to view the details of all students. The table should display a limited number of student information to fit the screen. I should be able to navigate forward and backward through the filtered list of student information.

```
TODO: estimate of effort in terms of user story points: 3
```

## US#5: Create Student Information

As an administrator, I would like to create new student information. Each new student should have a unique ID and include at least the following information: Enrollment Date, student name, major, academic year. (Create and manage gpa and credit is the task of US#8 )

```
TODO: estimate of effort in terms of user story points: 5
```

## US#6: Delete a Students Information

As a user, I want to delete student information. When I provide the students ID and confirm, the information should be removed from the database.

```
TODO: estimate of effort in terms of user story points: 1
```

## US#7: Update Student Information

As an administrator, I want to update update student information. When I provide a student's ID, the information about the student should be retrieved from the database and displayed so that I can edit the information. After confirmation, the updated information should be saved.

```
TODO: estimate of effort in terms of user story points: 1
```

## US#8: Graduation

As an user, I would like to be able to confirm that a student satisfies the requirements for graduation.  When I provide a student's ID, it should be possible to view the student's transcript and manage grades. At the same time, I will be able to retrieve the student's grade information for each semester from the database and add it up. If the credit is greater than 120 and the GPA is greater than 2.0, the student has satisfied the graduation requirements and is approved for graduation.

```
TODO: estimate of effort in terms of user story points: 8
```


## Sequence Diagram

At least one **user story**, unrelated to user creation or authentication, must be detailed using a **sequence diagram**.

## Model 

Include a class diagram that clearly describes the model classes used in the project and their associations.

# Development Process 

This section should describe, in general terms, how Scrum was used in this project. Include a table summarizing the division of the project into sprints, the user story goals planned for each sprint, the user stories actually completed, and the start and end dates of each sprint. You may also add any relevant observations about the sprints as you see fit.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2, US#4, US#6|11/14/24|11/21/24|US#1, US#2, US#4, US#6|no observations|
|2|US#3, US#5, US#7|11/22/24|11/27/24|US#3, US#5, US#7|no observations|
|3|US#8, ...|mm/dd/23|mm/dd/23|US#1|...|

As in Project 2, you should take notes on the major sprint meetings: planning, daily scrums, review, and retrospective. Use the scrum folder and the shared templates to record your notes.

# Testing 

In this section, share the results of the tests performed to verify the quality of the developed product, including the test coverage in relation to the written code. There is no minimum code coverage requirement, but ensure there is at least some coverage through one white-box test and one black-box test.

# Deployment 

The final product must demonstrate the integrity of at least 5 out of the 6 planned user stories. It should be packaged as a Docker image and be deployable using:

```
docker compose up
```