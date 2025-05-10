# Task Management API - Setup Guide

This README provides detailed instructions for setting up and running the Task Management API project with its complete CI/CD pipeline. This project demonstrates DevOps practices including containerization with Docker and CI/CD automation with Jenkins.

## Project Overview

The Task Management API is a RESTful service that allows users to create, read, update, and delete tasks. The project includes:

- Flask-based API
- Unit tests with pytest
- Docker containerization
- Jenkins CI/CD pipeline
- GitHub integration

## Repository

The complete code is available at: https://github.com/Kyu-Yi/task-management-api.git


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Kyu-Yi/task-management-api.git
cd task-management-api
```

### 2. Run the Application Locally (Optional)

```bash
# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.app
```

The application will be available at http://localhost:5000

You can test the API using curl or a tool like Postman:
```bash
# Test the health endpoint
curl http://localhost:5000/

# Create a task
curl -X POST -H "Content-Type: application/json" -d '{"title":"Test Task","description":"Task Description"}' http://localhost:5000/tasks

# Get all tasks
curl http://localhost:5000/tasks
```

### 3. Set Up Docker Container

```bash
# Build the Docker image
docker build -t task-management-api:latest .

# Run the container
docker run -d -p 5000:5000 --name task-api task-management-api:latest
```

Verify the container is running:
```bash
docker ps
```

### 4. Set Up Jenkins for CI/CD

#### Start Jenkins Container

```bash
# Run Jenkins in a Docker container
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts
```

#### Access Jenkins UI

1. Open a web browser and go to http://localhost:8080
2. Retrieve the initial admin password:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Complete the Jenkins setup:
   - Install suggested plugins
   - Create an admin user
   - Configure the Jenkins URL (default is fine)

#### Set Up the Jenkins Environment

To run the pipeline properly, Jenkins needs Python and Docker CLI installed:

```bash
# Connect to the Jenkins container as root
docker exec -it -u root jenkins bash

# Install Python
apt-get update
apt-get install -y python3 python3-pip

# Create symlinks
ln -sf /usr/bin/python3 /usr/bin/python
ln -sf /usr/bin/pip3 /usr/bin/pip

# Install Docker CLI
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce-cli

# Fix permissions for Docker socket
chmod 666 /var/run/docker.sock

# Exit the container
exit
```

#### Create a Jenkins Pipeline

1. In Jenkins, click "New Item"
2. Enter a name (e.g., "task-api-pipeline")
3. Select "Pipeline" and click "OK"
4. Configure the pipeline:
   - Under "Pipeline" section, select "Pipeline script from SCM"
   - For SCM, select "Git"
   - Repository URL: https://github.com/Kyu-Yi/task-management-api.git
   - Branch Specifier: */main
   - Script Path: Jenkinsfile
5. Click "Save"

#### Run the Pipeline

1. Navigate to your pipeline job
2. Click "Build Now" to start the pipeline

The pipeline will:
- Check out the code from GitHub
- Display key files
- Build a Docker image
- Show current Docker containers
- Simulate deployment (to avoid conflicts with existing containers)

## Project Structure

```
task-management-api/
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker container configuration
├── Jenkinsfile             # Jenkins CI/CD pipeline
├── requirements.txt        # Python dependencies
├── src/                    # Source code
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   └── api/                # API modules
│       ├── __init__.py
│       └── tasks.py        # Tasks API implementation
└── tests/                  # Test files
    ├── __init__.py
    └── test_tasks.py       # Unit tests for tasks API
```

## CI/CD Pipeline Structure

The Jenkinsfile defines a pipeline with the following stages:

1. **Checkout**: Retrieves code from the GitHub repository
2. **Setup and Test**: Displays project files and simulates test execution
3. **Code Quality**: Shows project structure and simulates quality checks
4. **Build Docker Image**: Builds a Docker image for the application
5. **Deploy to Development**: Shows current containers and deployment commands

## Troubleshooting

### Docker Socket Permission Issues
If Jenkins cannot access Docker, run:
```bash
docker exec -it -u root jenkins bash
chmod 666 /var/run/docker.sock
```

### Python Environment Issues
If Python commands fail, verify installation:
```bash
docker exec jenkins python --version
docker exec jenkins pip --version
```

### Pipeline Fails on Docker Build
If the Docker build fails, check:
1. Docker service is running
2. Docker socket permissions are correct
3. Disk space is sufficient

### Port Conflicts
If ports 5000 or 8080 are already in use, modify the port mappings:
```bash
# For the API container
docker run -d -p 5001:5000 --name task-api task-management-api:latest

# For Jenkins
docker run -d -p 8081:8080 -p 50001:50000 --name jenkins -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts
```
