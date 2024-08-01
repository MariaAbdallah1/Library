pipeline {
    agent any

    environment {
        registry = "maria0803/library"
        registryCredential = 'docker-c'
        dockerImage = ''
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${registry}:${env.BUILD_NUMBER}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Cleanup') {
            steps {
                script {
                    sh "docker rmi ${registry}:${env.BUILD_NUMBER}"
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
