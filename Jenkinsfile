pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = "ilyass07"
        REGISTRY_CREDENTIALS_ID = 'docker-hub-credentials'
        COMPOSE_PROJECT_NAME = "todo-app"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Static Code Analysis') {
            steps {
                script {
                    echo 'Running Hadolint on Dockerfiles...'
                    sh 'docker run --rm -i hadolint/hadolint < client/Dockerfile || true'
                    sh 'docker run --rm -i hadolint/hadolint < backend/Dockerfile || true'

                    echo 'Running Bandit on Backend...'
                    sh '''
                        docker run --rm \
                          -v $PWD/backend:/app \
                          -w /app \
                          python:3.8-slim \
                          sh -c "pip install bandit -q && bandit -r ."
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        sh 'docker compose up -d'

                        sleep 30

                        sh '''
                            docker run --rm \
                              --network todo-app_backend \
                              curlimages/curl --fail http://api:5000/api/tasks

                            docker logs todo-app-api-1
                        '''

                        echo "API Test Passed"
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Test failed: ${e.message}")
                    } finally {
                        sh 'docker compose down -v'
                    }
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    docker.withRegistry(
                        'https://index.docker.io/v1/',
                        REGISTRY_CREDENTIALS_ID
                    ) {
                        sh "docker tag todo-app-api ${DOCKER_HUB_USER}/todo-app-api:latest"
                        sh "docker push ${DOCKER_HUB_USER}/todo-app-api:latest"

                        sh "docker tag todo-app-client ${DOCKER_HUB_USER}/todo-app-client:latest"
                        sh "docker push ${DOCKER_HUB_USER}/todo-app-client:latest"
                    }
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
