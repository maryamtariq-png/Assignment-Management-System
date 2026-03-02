# Assignment Management System (FastAPI)

A full featured backend API designed to streamline the management of courses, assignments, and student submissions. This system provides a secure and efficient way for teachers to create courses and assignments while allowing students to submit their work seamlessly. It emphasizes role-based access control and modern authentication standards to ensure data integrity and security.

## Features
* **Role-Based Access Control:** Separate permissions for Students and Teachers.
* **Authentication:** Secure JWT-based login and password hashing with Bcrypt.
* **Course Management:** Teachers can create courses and post assignments.
* **Submissions:** Students can submit content before deadlines.

## Tech Stack
* FastAPI, SQLAlchemy, SQLite, Pydantic, Python-Jose (JWT).

## How to Run
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file (see `.env.example`).
4. Run the server: `uvicorn main:app --reload`