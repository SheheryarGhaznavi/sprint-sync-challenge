
# Sprint Sync Challenge

Sprint Sync Challenge is a project management tool designed to help teams track tasks, manage users, and streamline sprint planning. It features a modern backend built with FastAPI, SQLModel, and OpenAI integration for smart task suggestions. The backend provides secure authentication, structured logging, and flexible configuration for development and production environments.

# Backend

This folder contains the complete backend for the Sprint Sync Challenge project. Below is a summary of its structure and main features:

## Overview
- **Frameworks & Libraries:** FastAPI, SQLModel, SQLAlchemy, Alembic, aiomysql, Pydantic, python-jose, passlib, httpx
- **Database:** MySQL (async)
- **Authentication:** JWT-based login and authorization
- **AI Integration:** OpenAI API for task description suggestions
- **Structured Logging:** Custom middleware for request/response logging
- **Seeding:** Script to seed demo admin user and tasks

## Structure
- `alembic.ini` / `app/alembic/`: Database migrations (Alembic)
- `requirements.txt`: Python dependencies
- `app/main.py`: FastAPI app entrypoint, router registration, logging middleware
- `app/run_seeder.py`: Seeder script for demo data
- `app/config/`: Configuration for app, database, OpenAI, and JWT tokens
- `app/core/`: Database session management and logging middleware
- `app/models/`: SQLModel definitions for `User` and `Task`
- `app/requests/`: Pydantic models for API requests (user, task, AI)
- `app/responses/`: Pydantic models for API responses (user, task)
- `app/routers/`: FastAPI routers for auth, users, tasks, and AI endpoints
- `app/seeds/`: Demo seed logic
- `app/services/`: Business logic for AI, auth, user, and task management
- `app/utils/`: Dependency injection and security utilities

## Key Features
- **User Management:** CRUD operations for users, admin-only access for some routes
- **Task Management:** CRUD operations for tasks, status updates, user association
- **Authentication:** Secure login with JWT, password hashing
- **AI Suggestions:** Endpoint to get task description suggestions using OpenAI
- **Database Migrations:** Alembic setup for schema changes
- **Seeding:** Script to create demo admin and tasks for development
- **Logging:** Middleware for structured request/response logging

## How to Run
- Install dependencies: `pip install -r backend/requirements.txt`
- Run the API: `uvicorn backend/app/main:app --reload`
- Seed demo data: `python3 backend/app/run_seeder.py`
- Run migrations: `alembic -c backend/alembic.ini upgrade head`

## Configuration
- Environment variables are loaded from `.env` (see `app/config/`)
- Database, OpenAI, and JWT settings are configurable

---
This README summarizes the backend implementation, its structure, and main features. For more details, see the source files in each subfolder.
