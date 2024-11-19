# Learning Management System (Python/Django)

## Tech stack:
- Python
- Django
- Django rest framework
- Postgres
- Docker

## How to run:
- run `docker-compose up --build`
- visit `http://localhost:8000/api/`

## Notes:
- provide a `.env` file (there is a `.env.example` file for the required variables)
- docs available at `/api/`
- pagination available only for `/api/courses`

## Business Components:

### 1- Two types of users: Staff Members & Students

#### Staff Member: a teacher or manager

**Has the ability to**:

1- Create users in the admin panel

2- Create/Update/Delete/View Courses

3- Add/Remove/Update lessons in each course

4- Enrol students to specific courses

5- View all students' progress in each course

#### Student

**Has the ability to**:

1- View Courses

2- Mark lessons as completed

3- View own progress in each course

### 2- So the business flow can be:
1- Manager creates other managers and students in the admin

2- Manager creates Courses and create lessons for each course

3- Manager assigns courses to students based on the organisation policy

4- Student view courses

5- Student mark a course lesson as completed

6- Student views his/her progress

7- Manager views all students progress

### 3- Constraints:
1- Student can only mark a lesson completed if they are enrolled into its course

2- Student can not mark the same lesson as completed twice

3- Manager can not enrol the user on the same course twice


