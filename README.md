# Library Management
## Application Development
![WhatsApp Image 2024-08-05 at 17 27 43_0e3b4c75](https://github.com/user-attachments/assets/0eb253ff-e673-4ad9-b3e5-2b21ea26fa48)
## Infrastructure Terraform for AWS EKS
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
