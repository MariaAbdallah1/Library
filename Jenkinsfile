pipeline {
    agent any
    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS-ACCESS-KEY-ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS-KEY')
        AWS_DEFAULT_REGION = 'eu-north-1'
        
    }
    stages{
        stage('Checkout SCM'){
            steps{
                
                git branch: 'main', url: 'https://github.com/MariaAbdallah1/Library.git'
            }
        }
        
          stage('Dockerbuild and push') {
            steps {
                script{
                    withDockerRegistry(credentialsId: 'dockerhub') {
                         bat 'docker build -t sarahassan11/myflask:latest .'
                          bat 'docker push sarahassan11/myflask:latest'
                    }
                }
            }
        } 
        
        
        
        
        
        
         stage('Initializing Terraform'){
            steps{
                 bat 'terraform init'
            }
             
         }
         
         stage('Validating Terraform'){
            steps{
                 bat 'terraform validate'
            }
             
         }
         
         
          stage('Previewing the infrastructure'){
            steps{
                
                bat 'terraform plan -out=tfplan'
               
                
            }
             
         }
         
         
          stage('Approval') {
            steps {
                input message: "Approve the Terraform plan?", ok: "Apply"
            }
        }
        
         stage('Applying the infrastructure') {
            steps {
                bat 'terraform apply tfplan'
            }
        }
        
        
        stage('Update Kubeconfig') {
            steps {
                script {
                    // Ensure AWS CLI is installed and configured
                    bat 'aws --version'
                    
                    // Update kubeconfig for EKS
                    bat 'aws eks --region eu-north-1 update-kubeconfig --name my-cluster'
                }
            }
        }
        
        
        
        
         stage('deploy') {
            steps {
    
                kubernetesDeploy(configs: "app.yaml", kubeconfigId: "kubernetes")
                
            }
        }
         
         
         
         
         
         
         
         
         
         
    }
}
