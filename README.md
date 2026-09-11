# CRUD App — Full-Stack Social Platform

A full-stack social media application built with **FastAPI and React**, designed to provide a foundation for a modern social networking platform.

The project focuses on backend API development, authentication, database management, media handling, messaging, notifications, search, caching, background tasks, and a responsive web frontend.

## 🚀 Live Demo

* **Backend API:** https://crud-api-0b8d.onrender.com
* **Frontend:** https://crud-api-1-s7wp.onrender.com

> The current production deployment runs the core web application on Render. Some infrastructure and experimental components in the repository are intended for future development and are not part of the current production deployment.

## ✨ Features

### Backend

* FastAPI REST API
* PostgreSQL database
* SQLAlchemy ORM
* Alembic database migrations
* OAuth2 / JWT authentication
* User accounts and permissions
* Posts, comments, votes and bookmarks
* Followers and social relationships
* Stories
* Direct messaging
* Notifications
* Media uploads with Cloudinary
* Redis caching and Pub/Sub
* Celery background tasks and scheduled jobs
* Elasticsearch search and indexing
* WebSocket infrastructure
* Nginx configuration
* Docker and Docker Compose support

### Frontend

* React + TypeScript
* Vite
* Responsive social-media interface
* Authentication
* User profiles
* Posts and interactions
* Comments, votes and bookmarks
* Followers
* Stories
* Messaging
* Notifications
* Media handling
* Search integration

## 🏗️ Architecture

```text
React + TypeScript
        │
        ▼
     FastAPI
        │
 ┌──────┼───────────────┐
 ▼      ▼               ▼
PostgreSQL Redis     Elasticsearch
        │
        ▼
     Celery
        │
        ▼
   Background Tasks

Media ───────────────► Cloudinary
```

## 🛠️ Technology Stack

**Backend:** Python, FastAPI, SQLAlchemy, Alembic
**Database:** PostgreSQL
**Frontend:** React, TypeScript, Vite
**Caching / Messaging:** Redis, Redis Pub/Sub
**Background Processing:** Celery, Celery Beat
**Search:** Elasticsearch
**Media:** Cloudinary
**Infrastructure:** Docker, Docker Compose, Nginx
**Deployment:** Render
**API Testing:** cURL, Postman, pytest

## 📁 Project Structure

```text
CRUD_cleaned/
├── alembic/
├── app/
│   ├── routers/
│   ├── tasks/
│   ├── uploads/
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── main.py
│   ├── celery_app.py
│   ├── redis_cache.py
│   ├── elastic.py
│   ├── livestream.py
│   └── ...
├── nginx/
├── react/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
└── start.sh
```

## 🧪 Testing

The API has been tested using multiple approaches, including:

* **cURL** for direct API testing
* **Postman** for endpoint and authentication testing
* **pytest** for automated backend tests

## 🎥 Livestreaming — Current Status

The repository also contains an **early livestreaming/RTMP implementation**, including livestream-related backend code and Nginx RTMP configuration.

However, **live streaming is not currently deployed or production-ready**.

The livestream functionality has **not yet been connected to OBS in the production environment**, and there is currently no live RTMP/HLS streaming service running on the Render deployment.

This is intentional for the current stage of the project because deploying a complete livestreaming infrastructure requires additional server resources and infrastructure beyond the current Render setup.

The livestreaming components remain in the project as a foundation for future development.

## 🔮 Future Development

The long-term goal is to evolve this project from a CRUD/social-media web application into a **complete production-grade social media platform**.

Planned improvements include:

* Complete and productionize livestreaming with **OBS + RTMP/HLS**
* Improve the React frontend and overall UI/UX
* Build dedicated mobile applications
* Support **Android and iOS**, with additional cross-platform support where practical
* Move production infrastructure to **AWS**
* Improve scalability and infrastructure architecture
* Introduce stronger monitoring and observability
* Improve real-time communication features
* Expand media processing and storage
* Improve search and recommendation capabilities
* Strengthen security and performance
* Add more automated testing and CI/CD
* Scale the platform toward a larger social-network architecture

The long-term vision is to turn this project into a **complete social media ecosystem** where users can create and interact with content, communicate with each other, share media, follow creators, receive notifications, search content, and eventually participate in live broadcasts across web and mobile platforms.

## 📌 Project Status

**Current:** Full-stack social-media-style web application with a deployed FastAPI backend and React frontend.

**In development:** Livestreaming, deeper real-time functionality, improved frontend experience, mobile applications, and cloud infrastructure.

**Future:** AWS-based production infrastructure and a scalable multi-platform social media application.

## 👨‍💻 Author

**Dieudonne Kindong**

Software Engineering | Backend Development | Python | FastAPI | Django 

GitHub: `https://github.com/dieudonne670`

