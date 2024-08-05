# Library Management
## Application Development
![WhatsApp Image 2024-08-05 at 17 27 43_0e3b4c75](https://github.com/user-attachments/assets/0eb253ff-e673-4ad9-b3e5-2b21ea26fa48)
## Infrastructure Terraform for AWS EKS
This Terraform script automates the provisioning of an AWS EKS cluster along with the necessary infrastructure components. The setup includes the creation of a VPC, subnets, route tables, an internet gateway, a NAT gateway, security groups, and IAM roles and policies for both the EKS cluster and the node groups.
![eks drawio (1)](https://github.com/user-attachments/assets/ad58755c-9ebf-40d7-a245-dfb6f6fa716b)
```terraform
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags={
    Name="team5"
  }
}
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-north-1b"
  tags={
    Name="team5-public-subnet"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-north-1a"
   tags={
    Name="team5-private-subnet"
  }
}
resource "aws_eks_cluster" "eks_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids         = [aws_subnet.public.id, aws_subnet.private.id]
    security_group_ids = [aws_security_group.eks_sg.id]
  }
resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "my-node-group"
  node_role_arn   = aws_iam_role.eks_nodes_role.arn
  subnet_ids      = [aws_subnet.private.id]

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }
```
Apply terraform configuration
```sh
terraform init
terraform plan
terraform apply --auto-aprove
```
## app.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: new-flask-app-service
spec:
  type: LoadBalancer
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```
```sh
kubectl apply -f app.yaml
```
## CI/CD pipeline
### Prerequisites
..* Jenkins installed and configured.
..* AWS CLI installed and configured.
..* Docker installed.
..* Terraform installed.
..* AWS access key and secret access key.
..* Docker Hub credentials.
..* Kubernetes cluster and kubeconfig file.
Stages Overview
1. Checkout SCM
...Purpose: Check out the source code from the specified Git repository.
Steps:
Clone the repository from the main branch.
2. Docker Build and Push
...Purpose: Build the Docker image and push it to Docker Hub.
...Steps:
   ```git
   git branch: 'main', url: 'https://github.com/MariaAbdallah1/Library.git'
   ```
  ```script
   script {
                    withDockerRegistry(credentialsId: 'dockerhub') {
                        bat 'docker build -t sarahassan11/myflask:latest .'
                        bat 'docker push sarahassan11/myflask:latest'
                    }
```
4. Initialize Terraform
...Purpose: Initialize the Terraform configuration.
Steps:
Run terraform init to initialize the Terraform configuration.
5. Validate Terraform
...Purpose: Validate the Terraform configuration.
Steps:
Run terraform validate to ensure the configuration is correct.
6. Terraform Plan
...Purpose: Create an execution plan for Terraform.
Steps:
Run terraform plan -out=tfplan to create a plan and save it to tfplan.
7. Approval
...Purpose: Wait for manual approval before applying the Terraform plan.
Steps:
Prompt for manual approval to proceed with the Terraform apply.
8. Apply Terraform
...Purpose: Apply the Terraform plan to provision the infrastructure.
Steps:
Run terraform apply tfplan to apply the saved plan.
9. Update Kubeconfig
...Purpose: Update the kubeconfig file to connect to the EKS cluster.
Steps:
Run aws eks --region eu-north-1 update-kubeconfig --name my-cluster to update the kubeconfig file.
10. Deploy to Kubernetes
...Purpose: Deploy the application to the Kubernetes cluster.
Steps:
Use the Kubernetes plugin to deploy the application using the app.yaml configuration file.

