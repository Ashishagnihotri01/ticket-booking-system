# High-Concurrency Ticket Booking System

A scalable, async FastAPI ticket booking engine designed with robust data protection layers.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python 3.14)
* **Primary Database:** PostgreSQL (SQLAlchemy ORM)
* **Concurrency & Caching:** Redis Distributed Locking

## 🚀 Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Start the local infrastructure services (PostgreSQL & Redis)
3. Run the development server: `python -m uvicorn app.main:app --reload`
4. Access interactive docs: http://127.0.0.1:8000/docs
