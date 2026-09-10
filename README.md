CRUD API

A production-oriented FastAPI backend and React frontend demonstrating authentication, social features, background processing, caching, search, media management, notifications, messaging, and containerized deployment.

The project was built as a practical backend engineering project, with API functionality tested through cURL, Postman, and automated pytest tests.

🚀 Live Application
Frontend

https://crud-api-1-s7wp.onrender.com

Backend API

https://crud-api-0b8d.onrender.com

API Documentation

Once the backend is running, interactive API documentation is available through FastAPI:

/docs — Swagger UI
/redoc — ReDoc

Example:

https://crud-api-0b8d.onrender.com/docs
📌 Overview

CRUD API started as a CRUD application and was progressively expanded into a more complete backend system.

The application includes:

User registration and authentication
OAuth2/JWT authentication
User profiles
Posts
Comments
Voting
Bookmarks
Followers
Stories
Direct messaging
Notifications
Media uploads
Cloudinary integration
Redis caching
Celery background tasks
Celery Beat scheduled tasks
Redis Pub/Sub
Elasticsearch search
WebSocket infrastructure
PostgreSQL database
Alembic migrations
React frontend
Docker and Docker Compose
Nginx
Render deployment

The project focuses primarily on backend engineering, API design, database integration, asynchronous processing, caching, search, and deployment.

🏗️ Architecture
                         ┌──────────────────────┐
                         │      React Client    │
                         │      Vite + React    │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │      Nginx / API     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │      Application     │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌─────────────┐       ┌──────────────┐
      │ PostgreSQL  │       │    Redis    │       │ Elasticsearch│
      │  Database   │       │ Cache/PubSub│       │    Search    │
      └─────────────┘       └──────┬──────┘       └──────────────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │   Celery    │
                            │   Workers   │
                            └──────┬──────┘
                                   │
                                   ▼
                            ┌─────────────┐
                            │ Celery Beat │
                            │  Scheduler  │
                            └─────────────┘

                         ┌─────────────────┐
                         │    Cloudinary    │
                         │ Media Storage    │
                         └─────────────────┘
✨ Features
🔐 Authentication & Authorization
User registration
OAuth2 password authentication
JWT access tokens
Protected API endpoints
Permission handling
Authenticated user retrieval
User-specific resources
👤 User Management

Users can:

Register accounts
Authenticate
Retrieve their profile
Access other user profiles
Manage user relationships
Upload profile media
📝 Posts

The API supports complete post management:

Create posts
Retrieve posts
Update posts
Delete posts
Publish/unpublish posts
Retrieve post information
💬 Comments

Users can interact with posts through comments.

Supported operations include:

Creating comments
Associating comments with posts
Associating comments with users
Managing comment data
👍 Voting

The application provides a voting system for posts.

Users can:

Vote on posts
Remove votes
Change voting state
🔖 Bookmarks

Users can save posts for later access through the bookmark functionality.

👥 Followers

The application supports user relationships through:

Following users
Unfollowing users
Managing follower relationships
📖 Stories

The backend includes story functionality for temporary user-generated content.

📩 Messaging

The project includes direct user-to-user messaging functionality.

Messaging infrastructure is separated from the main application logic to keep the backend organized and maintainable.

🔔 Notifications

The notification system provides infrastructure for delivering user notifications based on application events.

Redis Pub/Sub and background processing can be used to support asynchronous notification workflows.

🖼️ Media Uploads

Media handling is integrated with Cloudinary.

The backend supports media-related functionality without requiring uploaded files to be stored directly on the application server.

This makes the application better suited for cloud deployment where local filesystem storage is limited or ephemeral.

⚡ Redis

Redis is used as an infrastructure component for:

Caching
Pub/Sub
Background-task communication
Application-level messaging

The project separates Redis functionality into dedicated modules such as:

app/redis.py
app/redis_cache.py
app/pubsub.py
🔄 Celery

Celery is integrated for asynchronous background processing.

The project includes:

app/celery_app.py
app/tasks.py
app/tasks/

Celery can be used for operations that should not block the main API request/response cycle.

Celery Beat is also included for scheduled background jobs.

🔎 Elasticsearch

Elasticsearch is integrated to provide search functionality.

The project contains dedicated modules for:

app/elastic.py
app/elastic_indices.py
app/elastic_sync.py
app/search.py
app/reindex.py
app/reindex_database.py

The reindexing utilities allow application data to be synchronized into Elasticsearch.

🔌 WebSocket Infrastructure

The project contains WebSocket infrastructure for real-time application functionality.

Relevant modules include:

app/websocket.py
app/websocket_manager.py

The architecture is designed so real-time communication can be handled separately from conventional REST API requests.

🗄️ Database

The project uses PostgreSQL as its primary relational database.

SQLAlchemy is used as the ORM layer.

Database-related functionality is organized around:

app/database.py
app/models.py
app/schemas.py
🔄 Database Migrations

Database schema changes are managed using Alembic.

alembic/
alembic.ini

Typical migration workflow:

alembic revision --autogenerate -m "describe change"
alembic upgrade head
🧪 API Testing

Testing was performed using multiple approaches rather than relying on a single testing method.

cURL

Direct HTTP requests were used to manually test API endpoints from the terminal.

Example:

curl http://localhost:8000/

Authenticated endpoints can also be tested by supplying the appropriate authorization header.

Postman

Postman was used for:

Endpoint testing
Authentication testing
Request/response inspection
CRUD workflows
Testing protected endpoints
Testing different request payloads
pytest

Automated backend tests are also included in:

tests/

This combination of manual API testing and automated tests helped verify the API from different perspectives.

🐳 Docker

The project includes Docker configuration for containerized development and deployment.

Main files:

Dockerfile
docker-compose.yml

Docker Compose is used to coordinate application services and their dependencies.

🌐 Nginx

Nginx configuration is included for reverse-proxy and web-serving infrastructure.

nginx/
├── Dockerfile
├── default.conf
└── nginx.conf
⚛️ React Frontend

The project includes a React frontend built with Vite.

react/
├── src/
├── index.html
├── package.json
├── package-lock.json
├── Dockerfile
├── nginx.conf
├── tsconfig.json
└── vite.config.ts

The frontend communicates with the FastAPI backend through HTTP APIs.

📁 Project Structure
CRUD_cleaned/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── oauth2.py
│   ├── permission.py
│   ├── utils.py
│   │
│   ├── celery_app.py
│   ├── tasks.py
│   ├── emails.py
│   ├── notifications.py
│   ├── messaging.py
│   │
│   ├── redis.py
│   ├── redis_cache.py
│   ├── pubsub.py
│   │
│   ├── elastic.py
│   ├── elastic_indices.py
│   ├── elastic_sync.py
│   ├── search.py
│   ├── reindex.py
│   ├── reindex_database.py
│   │
│   ├── cloudinary_client.py
│   ├── websocket.py
│   ├── websocket_manager.py
│   │
│   ├── livestream.py
│   ├── livestream_chat.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comments.py
│   │   ├── vote.py
│   │   ├── followers.py
│   │   ├── bookmarks.py
│   │   ├── media.py
│   │   ├── notifications.py
│   │   ├── message.py
│   │   ├── search.py
│   │   ├── stories.py
│   │   └── livestream.py
│   │
│   ├── tasks/
│   └── uploads/
│
├── alembic/
│
├── nginx/
│   ├── Dockerfile
│   ├── default.conf
│   └── nginx.conf
│
├── react/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── alembic.ini
└── start.sh
⚙️ Local Development
1. Clone the repository
git clone https://github.com/dieudonne670/CRUD_APP.git
cd CRUD_APP
2. Create a virtual environment
python3 -m venv env
source env/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file containing the required configuration for:

Database connection
JWT authentication
Redis
Elasticsearch
Cloudinary
Application settings

Do not commit .env to GitHub.

▶️ Run the FastAPI Backend

From the project root:

uvicorn app.main:app --reload

The API will normally be available at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs
🐳 Run with Docker Compose

From the project root:

docker compose up --build

To run the services in the background:

docker compose up -d --build

To stop them:

docker compose down
🔐 Environment Variables

The exact values depend on the deployment environment.

Typical configuration includes:

DATABASE_URL=

SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

REDIS_URL=

ELASTICSEARCH_URL=
ELASTICSEARCH_USERNAME=
ELASTICSEARCH_PASSWORD=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

Never commit production credentials, passwords, API keys, or secret tokens to the repository.

☁️ Deployment

The current application is deployed using Render.

The backend and frontend are deployed separately.

Backend
https://crud-api-0b8d.onrender.com
Frontend
https://crud-api-1-s7wp.onrender.com

Deployment configuration is included in:

render.yaml
⚠️ Deployment Scope

The current Render deployment focuses on the core application and available cloud resources.

Some infrastructure present in the repository is intended for local development, experimentation, or future expansion and is not represented as a production live-streaming deployment.

In particular, RTMP/live-streaming functionality is not part of the current Render production deployment.

This distinction is intentional: the repository contains infrastructure and experimental components beyond what is currently deployed.

🧠 Engineering Concepts Demonstrated

This project provided practical experience with:

REST API design
CRUD architecture
OAuth2
JWT authentication
Authorization
SQLAlchemy
PostgreSQL
Database migrations
Redis caching
Redis Pub/Sub
Celery
Background jobs
Scheduled tasks
Elasticsearch
Search indexing
WebSockets
Media storage
Cloudinary
Docker
Docker Compose
Nginx
React
API testing
cURL
Postman
pytest
Cloud deployment
🔒 Security Considerations

The project follows common application-security practices such as:

Environment-based configuration
JWT-based authentication
Protected endpoints
Permission checks
Separation of application secrets from source code
External media storage
Database migrations

For a production system, additional hardening would include:

Strong secret rotation policies
Rate limiting
Advanced monitoring
Centralized logging
Security headers
HTTPS enforcement
Dependency vulnerability scanning
Production-grade infrastructure configuration
📈 Future Improvements

Potential future improvements include:

More comprehensive automated test coverage
Improved API rate limiting
Advanced observability
Centralized logging
More sophisticated Elasticsearch queries
More background-processing workflows
Production-grade WebSocket scaling
CI/CD automation
Kubernetes deployment
Prometheus/Grafana monitoring
Additional cloud infrastructure

These are future improvements and are not presented as currently deployed features.

🎯 Project Goals

The goal of this project was not simply to implement basic CRUD operations.

The project was progressively expanded to explore how a backend application can evolve from a simple CRUD API into a more complete system involving:

CRUD
 ↓
Authentication
 ↓
Database Architecture
 ↓
Caching
 ↓
Background Processing
 ↓
Search
 ↓
Messaging & Notifications
 ↓
Media Storage
 ↓
Real-Time Infrastructure
 ↓
Containerization
 ↓
Cloud Deployment

This progression helped develop practical understanding of how different backend technologies fit together in a larger application.

👨‍💻 Author

Dieudonne Kindong

Software Engineering Graduate | Backend Developer

GitHub

https://github.com/dieudonne670

⭐ If you find this project useful

Feel free to explore the repository, review the API implementation, and experiment with the application.

FastAPI + PostgreSQL + Redis + Celery + Elasticsearch
                    +
              React + Docker
