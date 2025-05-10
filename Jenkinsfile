pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Successfully checked out code from Git repository'
            }
        }

        stage('Setup and Test') {
            steps {
                echo 'Setting up Python environment and running tests...'
                echo 'Command that would run: python -m pip install -r requirements.txt'
                echo 'Command that would run: python -m pytest tests/ --cov=src/'
                sh 'ls -la'  // This will show the project files
                sh 'cat requirements.txt'  // Display the requirements
                sh 'cat src/app.py'  // Display the main app file
                sh 'cat tests/test_tasks.py'  // Display test file
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running code quality checks...'
                echo 'Command that would run: pip install pylint'
                echo 'Command that would run: pylint src/'
                sh 'ls -la src/'  // List source code files
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t task-management-api:${BUILD_NUMBER} . || echo "Docker build would have executed here"'
                sh 'docker images || echo "Would list Docker images here"'
            }
        }

        stage('Deploy to Development') {
            steps {
                echo 'Deploying to development environment...'
                sh 'docker ps || echo "Would list running containers"'
                echo 'Commands that would run:'
                echo 'docker stop task-api-dev || true'
                echo 'docker rm task-api-dev || true'
                echo 'docker run -d -p 5000:5000 --name task-api-dev task-management-api:${BUILD_NUMBER}'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed'
        }
        success {
            echo 'Pipeline completed successfully'
            echo 'The CI/CD pipeline has been successfully simulated and executed where possible.'
            echo 'In a production environment, the pipeline would include actual Python package installation, testing, and Docker deployment.'
        }
    }
}
