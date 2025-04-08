# 🧠 TrackIt - Task Management API

TrackIt is a production-ready Flask-based Task Management API designed with modern DevOps practices. It supports user authentication, task tracking, caching, role-based access control, and background task processing.

🔗 **Live API**: [https://trackit-web.onrender.com](https://trackit-web.onrender.com)

---

## 📆 Tech Stack

- **Backend**: Flask, Flask-RESTful, SQLAlchemy, JWT
- **Database**: PostgreSQL (Hosted on Render)
- **Cache**: Redis (Hosted on Upstash)
- **Task Queue**: Celery + Redis
- **ORM Migrations**: Alembic
- **Containerization**: Docker, Docker Compose
- **Deployment**: Render (Web & DB), Upstash (Redis)

---

## ⚙️ Features

- 🔐 JWT-based Authentication (Login, Register)
- ✅ Role-Based Access Control (RBAC)
- 📌 Create, Update, Delete, Fetch Tasks
- 🢨 Redis Caching (Global & Per-user cache with invalidation)
- ⏰ Celery + Redis for background/scheduled jobs (task auto-archiving)
- 📄 Modular architecture using Blueprints & Services
- 🛣️ Dockerized for easy local & production setup

---

## 🚀 Deployment

- Web service is containerized and deployed to **Render**
- PostgreSQL DB is hosted on **Render PostgreSQL**
- Redis is hosted via **Upstash**
- Alembic handles DB migrations on startup

---

## 🛠️ Local Development Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/trackit-api.git
cd trackit-api
```

### 2. Create `.env.dev` and fill with your local DB, Redis, and JWT details.

### 3. Run using Docker Compose
```bash
docker-compose -f docker-compose.dev.yml up --build
```

---

## 💦 API Endpoints

| Endpoint              | Method | Description                    |
|-----------------------|--------|--------------------------------|
| `/auth/register`      | POST   | Register a new user            |
| `/auth/login`         | POST   | Login and get JWT              |
| `/tasks/`             | GET    | Get tasks (with caching)       |
| `/tasks/`             | POST   | Create new task (RBAC-secured) |
| `/tasks/<id>`         | PUT    | Update task (RBAC-secured)     |
| `/tasks/<id>`         | DELETE | Delete task (RBAC-secured)     |

---

## 📖 Project Structure

```
app/
🔹 api/
🔹 routes/
🔹 services/
🔹 ...
🔹 models/
🔹 extensions.py
🔹 config.py
🔹 celery_worker.py
migrations/
Dockerfile
docker-compose.prod.yml
.env
```

---

## 🙌 Author

Built with ❤️ by **Chittanshu Singh**  
Connect on [LinkedIn](https://www.linkedin.com/in/chittanshu-singh-a83944256)  
Email: chittanshusingh456@gmail.com

---

