# Sprint Sync Challenge

Sprint Sync Challenge is a project management tool designed to help teams track tasks, manage users, and streamline sprint planning. It features a modern backend built with FastAPI, SQLModel, and OpenAI integration for smart task suggestions, and a responsive frontend built with React, Semantic UI, and Bootstrap. The backend provides secure authentication, structured logging, and flexible configuration for development and production environments.

---

## Live URLs
- **Production Backend:** https://sprintsync-backend-production.up.railway.app/
- **Production Frontend:** https://sprintsync-frontend-production.up.railway.app/
- **Backend Swagger Docs:** https://sprintsync-backend-production.up.railway.app/docs

---

# Backend

This folder contains the complete backend for the Sprint Sync Challenge project. Below is a detailed summary of its structure and main features:

## Overview
- **Frameworks & Libraries:** FastAPI, SQLModel, SQLAlchemy, Alembic, aiomysql, Pydantic, python-jose, passlib, httpx
- **Database:** MySQL (async)
- **Authentication:** JWT-based login and authorization
- **AI Integration:** OpenAI API for task description suggestions
- **Structured Logging:** Custom middleware for request/response logging
- **Seeding:** Script to seed demo admin user and tasks

## Packages & Libraries
- **Python:**
  - fastapi
  - sqlmodel
  - sqlalchemy
  - alembic
  - aiomysql
  - pydantic
  - pydantic-settings
  - python-jose[cryptography]
  - passlib[bcrypt]
  - httpx
  - python-multipart
  - uvicorn

## Structure & File Roles
- `alembic.ini`, `app/alembic/`, `app/alembic/versions/`: Alembic configuration and migration scripts for database schema management.
- `requirements.txt`: Python dependencies for backend.
- `app/main.py`: FastAPI app entrypoint, router registration, CORS, logging middleware.
- `app/run_seeder.py`: Seeder script to create demo admin and tasks for development.
- `app/config/`: Configuration for app, database, OpenAI, and JWT tokens.
  - `config.py`: App-level settings.
  - `database.py`: Database connection settings.
  - `open_ai.py`: OpenAI API settings.
  - `token.py`: JWT token settings.
- `app/core/`: Core utilities.
  - `database.py`: Async database session management.
  - `logging.py`: Structured logging middleware for FastAPI.
- `app/models/`: SQLModel definitions.
  - `user.py`: User model (id, email, hashed_password, is_admin).
  - `task.py`: Task model (id, title, description, status, total_minutes, user_id).
- `app/requests/`: Pydantic models for API requests.
  - `user.py`: User creation request (email, password, is_admin).
  - `task.py`: Task creation/update request (title, description, status, total_minutes).
  - `ai.py`: AI suggestion request (title).
- `app/responses/`: Pydantic models for API responses.
  - `user.py`: User response and list response.
  - `task.py`: Task response and list response.
- `app/routers/`: FastAPI routers for API endpoints.
  - `auth.py`: Login route.
  - `users.py`: User CRUD routes (admin only).
  - `tasks.py`: Task CRUD routes, status update.
  - `ai.py`: AI suggestion endpoint.
- `app/seeds/`: Demo seed logic.
  - `dev_seed.py`: Creates demo admin and tasks if not present.
- `app/services/`: Business logic for AI, auth, user, and task management.
  - `base_service.py`: Base service with error handling.
  - `auth_service.py`: Login logic, password verification, JWT creation.
  - `user_service.py`: User CRUD logic.
  - `task_service.py`: Task CRUD logic, status updates.
  - `ai_service.py`: OpenAI integration for task description suggestions.
- `app/utils/`: Dependency injection and security utilities.
  - `security.py`: Password hashing, JWT creation/verification.
  - `deps.py`: Dependency functions for current user/admin extraction.

## Key Features
- **User Management:** CRUD operations for users, admin-only access for some routes.
- **Task Management:** CRUD operations for tasks, status updates, user association.
- **Authentication:** Secure login with JWT, password hashing.
- **AI Suggestions:** Endpoint to get task description suggestions using OpenAI.
- **Database Migrations:** Alembic setup for schema changes.
- **Seeding:** Script to create demo admin and tasks for development.
- **Logging:** Middleware for structured request/response logging.
- **Configurable:** All settings (database, OpenAI, JWT) are loaded from `.env` and can be customized.

## API URLs & Routes
- **Base URL:** `http://localhost:8000` (default)
- **Production Backend URL:** https://sprintsync-backend-production.up.railway.app/
- **Production Frontend URL:** https://sprintsync-frontend-production.up.railway.app/
- **Backend Swagger Docs:** https://sprintsync-backend-production.up.railway.app/docs
- **Auth:**
  - `POST /auth/login` — Login with email and password
- **Users:**
  - `GET /users/` — List users (admin only)
  - `POST /users/` — Create user (admin only)
  - `GET /users/{user_id}` — Get user by ID (admin only)
  - `PUT /users/{user_id}` — Update user (admin only)
- **Tasks:**
  - `GET /tasks/` — List tasks
  - `POST /tasks/` — Create task
  - `GET /tasks/{task_id}` — Get task by ID
  - `PUT /tasks/{task_id}` — Update task
  - `DELETE /tasks/{task_id}` — Delete task
  - `POST /tasks/{task_id}/status?status={status}` — Update task status
- **AI:**
  - `POST /ai/suggest` — Get AI-generated task description

## Demo User Credentials
- **Email:** admin@gmail.com
- **Password:** admin123

## How to Run Locally
1. Install Python 3.10+ and MySQL server.
2. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run database migrations:
   ```bash
   alembic -c backend/alembic.ini upgrade head
   ```
4. Seed demo data:
   ```bash
   python3 backend/app/run_seeder.py
   ```
5. Start the API server:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

## How to Run on Server
1. Set up Python 3.10+ and MySQL on your server.
2. Clone the repository and install dependencies as above.
3. Set environment variables in `.env` for production (see `app/config/`).
4. Use a production ASGI server (e.g., gunicorn, uvicorn) and a process manager (e.g., systemd, supervisor).
5. Configure firewall and reverse proxy (e.g., Nginx) for HTTPS and routing.

## How to Run through Docker
1. Make sure Docker and Docker Compose are installed on your server.
2. Copy `.env.example` to `backend/app/.env` and fill in your secrets.
3. Build and start all services:
   ```bash
   docker compose up --build
   ```
4. Backend API will be available at `http://localhost:8000` (or your server IP).
5. Frontend will be available at `http://localhost:5173` (or your server IP).
6. For production, you can deploy to platforms like Railway using the provided URLs above.

---

# Frontend

This folder contains the complete frontend for Sprint Sync Challenge. Below is a summary of its structure and main features:

## Overview
- **Frameworks & Libraries:** React, Semantic UI React, Bootstrap, Axios, Vite
- **Routing:** React Router DOM
- **API Integration:** Axios for backend communication
- **Responsive Design:** Semantic UI and Bootstrap grid system

## Packages & Libraries
- **Node.js:**
  - react
  - react-dom
  - react-router-dom
  - semantic-ui-react
  - semantic-ui-css
  - axios
  - vite
  - @vitejs/plugin-react

## Structure & File Roles
- `index.html`: Main HTML entry point, loads Semantic UI and Bootstrap CSS.
- `package.json`: Frontend dependencies and scripts.
- `vite.config.js`: Vite configuration for dev/build/preview.
- `src/main.jsx`: App entrypoint, sets up routing and authentication.
- `src/pages/App.jsx`: Main dashboard, task management UI, modals, notifications, loader.
- `src/pages/Login.jsx`: Login page, authentication logic, notifications, loader.
- `src/services/api.js`: Axios instance for API calls, handles JWT token.

## Key Features
- **Login:** Secure login with JWT, notification and loader.
- **Task Management:** Create, edit, delete, and update status of tasks.
- **AI Suggestions:** Get smart task descriptions from backend AI endpoint.
- **Responsive UI:** Mobile-friendly, modern design using Semantic UI and Bootstrap.
- **Notifications & Loader:** User feedback for all API actions.

## Frontend URLs & Routes
- **Main App:** `/` — Dashboard (requires login)
- **Login:** `/login` — Login page
- **API Base URL:** Configurable in `src/services/api.js` (default: `http://localhost:8000`)

## Demo User Credentials
- **Email:** admin@gmail.com
- **Password:** admin123

## How to Run Locally
1. Install Node.js (v18+) and npm.
2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## How to Run on Server
1. Build the frontend for production:
   ```bash
   npm run build
   ```
2. Serve the `dist` folder using a static server (e.g., Nginx, Vercel, Netlify) or Vite preview:
   ```bash
   npm run preview
   ```
3. Configure your server to proxy API requests to the backend.

## How to Run through Docker
1. Build frontend image:
   ```bash
   docker build -t sprintsync-frontend -f Dockerfile.frontend .
   ```
2. Run frontend container:
   ```bash
   docker run -d -p 5173:5173 sprintsync-frontend
   ```

## Tools & Requirements
- **Backend:** Python 3.10+, MySQL
- **Frontend:** Node.js v18+, npm
- **Other:** Alembic (for migrations), Uvicorn (for API), Vite (for frontend)

---

# License

MIT License

Copyright (c) 2025 Sherry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
