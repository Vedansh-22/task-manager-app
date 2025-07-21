# 📝 Task Manager App - Backend API

A simple and secure Task Manager backend built using **FastAPI** and **MongoDB**. This app allows users to register, log in, and manage their personal tasks (create, view, update, delete). Authentication is handled via **JWT (JSON Web Tokens)**.

⚠️ **Frontend is not yet developed.** If you're passionate about frontend (especially with React, Vue, or Svelte), feel free to contribute!

---

## 🚀 Features

- 🔐 User Registration and Secure Login (with password hashing using `bcrypt`)
- 🛡️ JWT-based Authentication
- 📒 Task management:
  - Create new tasks
  - Retrieve user-specific tasks
  - (Planned) Update and delete tasks
- 🌐 MongoDB integration using `pymongo`

---

## 📦 Tech Stack

| Layer        | Technology      |
|--------------|-----------------|
| Language     | Python 3.12     |
| Backend      | FastAPI         |
| Database     | MongoDB (local or cloud via MongoDB Atlas) |
| Auth         | JWT (`python-jose`) |
| Passwords    | bcrypt          |
| Server       | Uvicorn         |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python ≥ 3.10
- MongoDB (local or hosted on Atlas)
- `pip` for package management

---

## ⚙️ Project Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/task-manager-backend.git
   cd task-manager-backend/backend

2. **Create Virtual Environment**
   ```bash 
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies**
   ```bash 
   pip install -r requirements.txt
4. **Set up your .env file**
    Create a .env file in the backend/ directory:
   ```ini 
   MONGO_URI=mongodb://localhost:27017
   DB_NAME=task_manager
   SECRET_KEY=your_super_secret_key
   ALGORITHM=HS256
5. **Run the App**
   ```bash 
   uvicorn main:app --reload
6. **Test the API**  
   http://127.0.0.1:8000/docs

**📂 Project Structure**
```
backend/
├── auth/
│   ├── auth_bearer.py       # Custom auth class for JWT bearer
│   └── utils.py             # Token creation, verification
├── models.py                # Pydantic models for user and task   
├── main.py                  # API routes
├── .env                     # (Ignored by Git)
└── requirements.txt
```
**🔒 Authentication**
  
  All task-related routes are protected. Use the /login endpoint to receive a JWT, and include it in the Authorization header:
  ```
  Bearer <your_token_here>
  ```



In Swagger UI:
	•	Click the Authorize button
	•	Paste your token as: Bearer eyJhbGci...

⸻

🧪 Example Routes
	•	POST /register → Register new user
	•	POST /login → Get JWT token
	•	GET /tasks → Get tasks for current user (requires token)
	•	POST /task → Add new task for current user (requires token)

⸻

🧱 To Do
	•	User Authentication
	•	Task Creation & Retrieval
	•	Task Update/Delete
	•	Frontend Integration

⸻

💡 Frontend Contribution Welcome!

Currently, this project does not have a Proper frontend. If you’re interested in building a modern frontend using React, Vue, or any framework of your choice, your contributions are welcome!

Suggested stack:
React + Tailwind + Axios or React Query

⸻

🛠️ Useful Dev Tips
	•	For base64 errors during JWT decoding, double-check your Authorization header format and make sure you’re using a valid token.
	•	Always use bcrypt for hashing passwords — never store raw passwords.

⸻

Feel free to fork, star ⭐, or raise a PR if you’d like to contribute!
