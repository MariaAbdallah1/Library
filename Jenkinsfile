pipeline {
    agent any

    environment {
        registry = "veles3/library"
        registryCredential = 'dockerhub'
        dockerImage = ''
        kubeconfig = credentials('kubeconfig') // Jenkins credentials with your kubeconfig file
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
        stage('Deploy to EKS') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG'),
                                     usernamePassword(credentialsId: 'aws-credentials', passwordVariable: 'AWS_SECRET_ACCESS_KEY', usernameVariable: 'AWS_ACCESS_KEY_ID')]) {
                        // Echo the KUBECONFIG path for debugging
                        sh "echo KUBECONFIG=$KUBECONFIG"
                        // Configure AWS CLI with provided credentials
                        sh """
                        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                        aws configure set region eu-central-1
                        """
                        // Update Kubernetes deployment with the new image
                        sh """
                        kubectl set image deployment/coredns coredns=${dockerImage} --namespace=kube-system --kubeconfig $KUBECONFIG
                        """
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
            script {
                cleanWs()
            }
        }
    }
}
