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
### purpose
This CI/CD pipeline is to automate the process of building, pushing, and deploying Docker images for a continuous integration and continuous deployment workflow. This pipeline helps ensure that code changes are automatically tested and deployed to the production environment, reducing the risk of manual errors and speeding up the release process.

### Pipeline configuration (Environment Variables)
**registry:** Docker Hub registry name.__
**registryCredential:** Jenkins credentials ID for Docker Hub.__
**dockerImage:** Docker image name (dynamically set during the build stage).
**kubeconfig:** Jenkins credentials ID for the Kubernetes configuration file.
```script
  environment {
        registry = "veles3/library"
        registryCredential = 'dockerhub'
        dockerImage = ''
        kubeconfig = credentials('kubeconfig') // Jenkins credentials with your kubeconfig file
    }
```
### Build Docker Image
- Purpose: To build a Docker image from the source code present in the repository.
- Steps:
    ..1. Set the Docker image name with the build number.
    ..2. Execute the Docker build command to create the image.
  ```script
    stage('Build Docker Image') {
      steps {
          script {
              dockerImage = "${registry}:${env.BUILD_NUMBER}"
              sh "docker build -t ${dockerImage} ."
          }
        }
      }
  ```
