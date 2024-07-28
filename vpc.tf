terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-north-1"
}

# Create a VPC
resource "aws_vpc" "maria" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "maria-vpc"
  }
}

# Create a Public Subnet
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.maria.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "eu-north-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet"
  }
}

# Create a Private Subnet
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.maria.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "eu-north-1a"
  tags = {
    Name = "private-subnet"
  }
}

# Create an Internet Gateway
resource "aws_internet_gateway" "maria" {
  vpc_id = aws_vpc.maria.id
  tags = {
    Name = "maria-igw"
  }
}

# Route Table for Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.maria.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.maria.id
  }

  tags = {
    Name = "public-route-table"
  }
}

# Associate Route Table with Public Subnet
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  vpc = true
}

# NAT Gateway
resource "aws_nat_gateway" "maria" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "maria-nat-gateway"
  }
}

# Route Table for Private Subnet
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.maria.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.maria.id
  }

  tags = {
    Name = "private-route-table"
  }
}

# Associate Route Table with Private Subnet
resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# Security Group for Public Instances
resource "aws_security_group" "public_sg" {
  vpc_id = aws_vpc.maria.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "public-sg"
  }
}

# Security Group for Private Instances
resource "aws_security_group" "private_sg" {
  vpc_id = aws_vpc.maria.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Allow SSH within the VPC
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "private-sg"
  }
}

# User Data Script for Apache2 Installation and Reverse Proxy Setup on Public Instance
data "template_file" "apache_user_data_public" {
  template = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y apache2
    sudo systemctl enable apache2
    sudo systemctl start apache2

    # Install Apache modules
    sudo apt install -y apache2-utils
    sudo a2enmod proxy
    sudo a2enmod proxy_http

    # Configure Apache as a reverse proxy
    echo '<VirtualHost *:80>
        ProxyPass / http://10.0.2.60:80/
        ProxyPassReverse / http://10.0.2.60:80/
    </VirtualHost>' | sudo tee /etc/apache2/sites-available/000-default.conf

    sudo systemctl restart apache2
  EOF

  vars = {
    private_instance_ip = aws_instance.private_instance.private_ip
  }
}

# User Data Script for Apache2 Installation on Private Instance
data "template_file" "apache_user_data_private" {
  template = <<-EOF
    #!/bin/bash
    sudo apt update -y
    sudo apt install -y apache2
    sudo systemctl enable apache2
    sudo systemctl start apache2

    # Create a simple index.html with the private IP address
    echo "hello from 10.0.2.60 | sudo tee /var/www/html/index.html
  EOF
}

# EC2 Instance in Public Subnet
resource "aws_instance" "public_instance" {
  ami           = "ami-07c8c1b18ca66bb07"  # Replace with your AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.public_sg.id]
  user_data     = data.template_file.apache_user_data_public.rendered

  tags = {
    Name = "public-instance"
  }
}

# EC2 Instance in Private Subnet
resource "aws_instance" "private_instance" {
  ami           = "ami-07c8c1b18ca66bb07"  # Replace with your AMI ID
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.private_sg.id]
  user_data     = data.template_file.apache_user_data_private.rendered

  tags = {
    Name = "private-instance"
  }
}

# Output the private IP address of the private instance
output "private_instance_ip" {
  value = aws_instance.private_instance.private_ip
}
