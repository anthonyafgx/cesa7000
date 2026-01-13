pipeline {
    agent any
    
    triggers {
        pollSCM('H/5 * * * *')
    }
    
    environment {
        DOCKER_IMAGE = 'anthonyafgx/cesa7000'
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONARQUBE_URL = 'http://sonarqube:9000'
        // Credentials from .env file (passed via docker-compose.yml)
        DOCKER_USER = "${env.DOCKERHUB_USERNAME}"
        DOCKER_PASS = "${env.DOCKERHUB_TOKEN}"
        SONAR_TOKEN = "${env.SONARQUBE_TOKEN}"
        // Host workspace path for Docker-in-Docker volume mounts
        WORKSPACE_HOST = "${env.WORKSPACE_HOST}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                sh """
                    docker run --rm \
                        --network cesa7000_cicd-network \
                        -v "${WORKSPACE_HOST}/${JOB_NAME}:/usr/src" \
                        -w /usr/src \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=cesa7000 \
                        -Dsonar.sources=src \
                        -Dsonar.host.url=${SONARQUBE_URL} \
                        -Dsonar.login=${SONAR_TOKEN} \
                        -Dsonar.python.version=3.11
                """
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -t ${DOCKER_IMAGE}:latest ."
            }
        }
        
        stage('Trivy Security Scan') {
            steps {
                sh """
                    trivy image --exit-code 0 --severity LOW,MEDIUM ${DOCKER_IMAGE}:${DOCKER_TAG}
                    trivy image --exit-code 1 --severity HIGH,CRITICAL ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                """
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                sh '''
                    echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                    docker logout
                '''
            }
        }
    }
    
    post {
        always {
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
