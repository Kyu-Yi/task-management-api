pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                // Create a virtual environment without system packages
                sh 'python3 -m venv venv || python -m venv venv'
                
                // Install packages in the virtual environment
                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ --cov=src/ || true
                '''
            }
        }

        stage('Code Quality') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pylint || true
                    pylint src/ || true
                '''
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
