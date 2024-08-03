variable "cluster_name" {
  description = "The name of the EKS cluster."
  type        = string
  default     = "my-cluster"
}

variable "region" {
  description = "The AWS region to create resources in."
  type        = string
  default = "eu-north-1"
}
