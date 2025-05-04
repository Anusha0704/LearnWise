# LearnWise
LearnWise is a user-friendly web application that allows learners to explore, review, and manage online courses from various platforms. With features like user and admin login, course creation, advanced filtering, and rating submissions, LearnWise helps users personalize their learning journey.

**LearnWise** is a responsive web application that empowers users to:
- Search and filter online courses from various platforms.
- Submit and update course ratings.
- Create new course records.
- Perform full CRUD operations (admin only).

Techstack:
- Python (Flask)
- PostgreSQL
- SQLAlchemy
- Bootstrap 5
- HTML/CSS/JS
- Javascript
- HTML

---

## Features

- **User & Admin Authentication**
- **Search courses by title, platform, rating, and duration**
- **Add and update ratings**
- **Admin dashboard for full course management (create, update, delete)**
- **Consistent pastel-themed UI using Bootstrap**
- **Responsive design with animations and 3D Lottie integration**

---

## Follow the steps below to get the project up and running on your local machine.

1. Clone the Repository

git clone https://github.com/Anusha0704/LearnWise.git
cd LearnWise

2. Set Up Virtual Environment (Optional)

python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows

3. Install Required Python Packages

pip install -r requirements.txt

4. Create PostgreSQL Database

Ensure PostgreSQL is installed and running.
Open pgAdmin or psql.
Create a new database:

CREATE DATABASE learnwise_db; or Manually through PGAdmin

5. Set Up Database Tables and Import Data

Step 1: Run Schema SQL

Open the database (learnwise_db) in pgAdmin.
Open Query Tool, load the schema.sql file, and run the SQL commands to create all tables.

Step 2: Import Data into Tables

In pgAdmin, navigate to:
Databases > learnwise_db > Schemas > public > Tables > [Table Name]
Right-click the table → Select Import/Export Data.
Choose the provided .csv file for that table (e.g., courses.csv).
Format: CSV, Header: Checked, Delimiter: ,
Click OK to upload.

Note: No need to upload data to the users table. User data is inserted dynamically when users sign up.

6. Update app.py with Your Database Credentials

Open app.py and update this line:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/learnwise_db'
Replace your_username, your_password, and learnwise_db with your actual PostgreSQL credentials.

7. Run the Application

python app.py
Visit: http://localhost:5000

The web app will be available in http://localhost:5000
