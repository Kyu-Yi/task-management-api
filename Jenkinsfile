pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Successfully checked out code from Git repository'
            }
        }

        stage('Setup') {
            steps {
                echo 'Simulating: pip install -r requirements.txt'
                echo 'Would install Flask, pytest, pytest-cov, and gunicorn'
            }
        }

        stage('Test') {
            steps {
                echo 'Simulating: python -m pytest tests/ --cov=src/'
                echo 'Would run tests and report coverage'
            }
            post {
                always {
                    echo 'Would collect test results here'
                }
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Simulating: pip install pylint'
                echo 'Simulating: pylint src/'
                echo 'Would check code quality with pylint'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Simulating: docker build -t task-management-api:${BUILD_NUMBER} .'
                echo 'Would build Docker image with tag: task-management-api:${BUILD_NUMBER}'
            }
        }

        stage('Deploy to Development') {
            steps {
                echo 'Simulating: docker stop task-api-dev || true'
                echo 'Simulating: docker rm task-api-dev || true'
                echo 'Simulating: docker run -d -p 5000:5000 --name task-api-dev task-management-api:${BUILD_NUMBER}'
                echo 'Would deploy container to development environment'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed'
        }
        success {
            echo 'Pipeline completed successfully'
        }
    }
}
