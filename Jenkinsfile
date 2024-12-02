pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "flask_app"
        DOCKER_TAG = "latest"
        DOCKERFILE_PATH = "."
    }

    stages {
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
            echo 'Build and Tests succeeded! The container is running.'
        }

        failure {
            echo 'Build or Tests failed!'
        }
    }
}
