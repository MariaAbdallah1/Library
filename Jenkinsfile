pipeline {
    agent any

    environment {
        registry = "maria0803/library"
        registryCredential = 'dockerhub_id'
        dockerImage = ''
    }

    stages {
        // stage('Checkout') {
        //     steps {
        //         git 'https://github.com/MariaAbdallah1/Library.git'
        //     }
        // }
        stage('Build Docker Image') {
            steps {
                script {
                    // dockerImage = docker.build("${registry}:${env.BUILD_NUMBER}")
                    sh 'docker build -t libraryapp .'
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
                sh "docker rmi ${registry}:${env.BUILD_NUMBER}"
                sh "docker rmi ${registry}:latest"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
