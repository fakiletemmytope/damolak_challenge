# Damolak Auth Challenge

A full-stack authentication service featuring a FastAPI backend, a vanilla HTML/JS frontend, and automated infrastructure deployment on AWS using Terraform and GitHub Actions.

## 🚀 Project Overview

This project demonstrates a complete DevOps lifecycle for a modern web application:
- **Frontend**: Responsive UI built with vanilla HTML5, CSS3, and JavaScript.
- **Backend**: High-performance REST API powered by FastAPI, SQLModel, and PostgreSQL.
- **Security**: JWT-based authentication with secure token blacklisting via Redis.
- **Infrastructure**: Infrastructure as Code (IaC) using Terraform for AWS provisioning.
- **CI/CD**: Fully automated testing, linting, and deployment pipelines via GitHub Actions.

## 🏗️ Architecture

- **Web Server**: Nginx (Frontend)
- **Application Server**: Uvicorn/FastAPI (Backend)
- **Database**: PostgreSQL (Persistent Storage)
- **Cache**: Redis (Session/Token Management)
- **Cloud Provider**: AWS (EC2, Route53, VPC)

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework.
- **SQLModel**: Interaction with PostgreSQL database.
- **Redis**: Asynchronous caching for token blacklisting.
- **PyJWT**: Secure JSON Web Token implementation.
- **Ruff**: High-performance Python linting and formatting.

### Frontend
- **Vanilla JS**: Lightweight, no-framework implementation.
- **Modern CSS**: Responsive design with CSS variables and modern layout techniques.
- **Fetch API**: Asynchronous communication with the backend.

### DevOps & Infrastructure
- **Terraform**: AWS resource orchestration (VPC, EC2, Route53, CloudWatch).
- **Docker & Docker Compose**: Containerization and local orchestration.
- **GitHub Actions**: Automated CI/CD (Testing, Linting, Building, Deploying).

## 🚦 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Terraform (for infrastructure changes)

### Local Development
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd damolak_challenge
   ```

2. **Configure Environment**:
   Create a `.env` file in the root (refer to `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. **Run with Docker Compose**:
   ```bash
   docker compose up --build
   ```
   - Frontend: `http://localhost`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

### Running Tests
To execute the backend test suite:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
python3 -m pytest backend/tests/
```

## 🚢 Deployment (CI/CD)

The project uses GitHub Actions for automated deployment.

### Workflows
- **Backend CI**: Runs Ruff linting and Pytest on every push to `main` or pull request to `dev`.
- **Frontend CI**: Validates HTML, CSS, and JS formatting.
- **Deployment**: Provisions AWS infrastructure via Terraform and deploys the application using Docker Compose on EC2.

### Required Secrets
Set the following secrets in your GitHub repository:
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`
- `DOCKERHUB_USERNAME` & `DOCKERHUB_TOKEN`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `SECRET_KEY` (for JWT)

## 🛡️ License
Distributed under the MIT License.
