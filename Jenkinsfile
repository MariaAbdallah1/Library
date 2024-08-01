pipeline {
    agent any

    environment {
        registry = "veles3/library"
        registryCredential = 'docker-c'
        dockerImage = ''
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = "${registry}:${env.BUILD_NUMBER}"
                    sh "docker build -t ${dockerImage} ."
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: registryCredential, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin"
                        sh "docker push ${dockerImage}"
                        sh "docker tag ${dockerImage} ${registry}:latest"
                        sh "docker push ${registry}:latest"
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh "docker rmi ${dockerImage}"
                    sh "docker rmi ${registry}:latest"
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
