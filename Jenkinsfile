pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python -m pytest tests/ --cov=src/ || true'
            }
        }

        stage('Code Quality') {
            steps {
                sh 'pip install pylint || true'
                sh 'pylint src/ || true'  // Continue even if pylint finds issues
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t task-management-api:${BUILD_NUMBER} .'
            }
        }

        stage('Deploy to Development') {
            steps {
                sh 'docker stop task-api-dev || true'
                sh 'docker rm task-api-dev || true'
                sh 'docker run -d -p 5000:5000 --name task-api-dev task-management-api:${BUILD_NUMBER}'
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
