🏠 Airbnb Clone Backend – FastAPI

A production-style backend system inspired by Airbnb, built using FastAPI, PostgreSQL, and SQLAlchemy.
This project implements authentication, role-based access control, booking logic with date validation, listing moderation, and advanced querying features.

🚀 Tech Stack

FastAPI
PostgreSQL
SQLAlchemy (ORM)
Alembic (Database migrations)
JWT Authentication
Passlib (bcrypt hashing)
Pydantic
Uvicorn

📌 Features

🔐 Authentication & Authorization

User signup & login
JWT-based authentication
Protected routes
Current user extraction
Role-based access control (User / Admin)

👤 User System

Default role: user
Admin role with elevated privileges
Admin can:
    View all users
    Approve or reject listings
    Moderate platform content

🏡 Listings

Create listing (authenticated users only)
Update/delete listing (owner only)
Admin moderation system

🔎 Advanced Querying

Pagination (skip, limit)
Price filtering (min_price, max_price)
Search by title
Sorting (price ascending/descending)

📅 Booking System

Users can book listings
Owner cannot book own listing
Date validation (start < end)
Overlapping booking prevention
Stores booking date range

🗄 Database Management

Alembic migrations for schema versioning
No manual table dropping
Proper schema tracking

📂 Project Structure

airbnb_backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── routers/
│   │     ├── users.py
│   │     ├── listings.py
│   │     ├── bookings.py
│
├── alembic/
├── requirements.txt
└── .env

⚙️ Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd airbnb_backend
2️⃣ Create virtual environment
python -m venv venv
Activate:

    Windows: venv\Scripts\activate
    Mac/Linux: source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt
🗄 Setup PostgreSQL

Create database:

CREATE DATABASE airbnb_db;
🔑 Environment Variables

Create .env file:

DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/airbnb_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
🧱 Run Migrations
alembic upgrade head
▶️ Run Server
uvicorn app.main:app --reload

Swagger Docs:

http://127.0.0.1:8000/docs
🔐 Authentication Flow

Signup → /users/signup
Login → /users/login
Click Authorize in Swagger

Enter:

username = email
password = password
Access protected routes

🛠 Example API Usage
Create Listing
POST /listings
Get Listings (with filters)
GET /listings?search=beach&min_price=1000&sort_by=price_desc
Create Booking
POST /bookings
Admin Approve Listing
PUT /listings/admin/status/{listing_id}?status=approved

🧠 Business Logic Highlights :

Owner-only listing modification
Admin-only moderation endpoints

Booking overlap prevention logic:
    Two bookings overlap if:
                            existing_end > new_start
                            AND
                            existing_start < new_end

Clean dependency-based authorization system

📈 What This Project Demonstrates

RESTful API design
JWT authentication
Role-based access control
Relational database modeling
Schema migrations
Business rule enforcement
Pagination, filtering, sorting
Real-world backend architecture thinking

🔮 Possible Future Improvements

Dockerization (FastAPI + Postgres containers)
Redis caching for listing queries
Unit testing with Pytest
Async SQLAlchemy
Rate limiting
Logging & monitoring
Cloud deployment (AWS / Render / Railway)

👨‍💻 Author

Rahul
Backend-focused developer building production-style systems using FastAPI.
