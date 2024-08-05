output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

output "cluster_endpoint" {
  value = aws_eks_cluster.eks_cluster.endpoint
}

output "cluster_security_group_id" {
  value = aws_eks_cluster.eks_cluster.vpc_config[0].cluster_security_group_id
}

output "cluster_certificate_authority_data" {
  value = aws_eks_cluster.eks_cluster.certificate_authority[0].data
}
