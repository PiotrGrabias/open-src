pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask_app'
        DOCKER_TAG = 'latest'
        IMAGE_NAME = "flask-app"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/PiotrGrabias/open-src'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${DOCKER_TAG}")
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                script {
                    bat '''
                        docker-compose down  # Stop and remove containers
                        docker-compose up -d  # Rebuild and restart containers in detached mode
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
