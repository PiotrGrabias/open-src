pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "flask_app"
        DOCKER_TAG = "latest"
        DOCKERFILE_PATH = "."
    }

    stages {
        stage('Stop Existing Container') {
            steps {
                script {
                    bat """
                    docker ps -q --filter "name=flask_app" | findstr . && docker stop flask_app && docker rm flask_app || echo "No running container to stop"
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_TAG} ${DOCKERFILE_PATH}"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    bat "docker run -d -p 5000:5000 --name flask_app ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo 'Build and deployment succeeded! The container is running with the latest image.'
        }

        failure {
            echo 'Build or deployment failed!'
        }
    }
}
