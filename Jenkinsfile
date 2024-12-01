pipeline {
    agent any  // Use any available agent

    environment {
        DOCKER_IMAGE = 'flask-app-image'
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

//         stage('Run Tests') {
//             steps {
//                 script {
//                     docker.image("${IMAGE_NAME}:${DOCKER_TAG}").inside {
//                         sh 'pytest --maxfail=1 --disable-warnings -q'  // Running tests
//                     }
//                 }
//             }
//         }

        stage('Deploy Locally') {
            steps {
                script {
                    sh '''
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
