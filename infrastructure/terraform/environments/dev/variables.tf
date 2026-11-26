variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "canary-platform"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "dev"
}

# ------------------------------------------------------------------------------
# VPC Configuration
# ------------------------------------------------------------------------------
variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.20.0.0/16"
}

variable "availability_zones" {
  description = "Availability Zones to use in ap-south-1 (ap-south-1a = aps1-az1, ap-south-1b = aps1-az3)"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.20.1.0/24", "10.20.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.20.16.0/20", "10.20.32.0/20"]
}

# ------------------------------------------------------------------------------
# EKS Configuration
# ------------------------------------------------------------------------------
variable "kubernetes_version" {
  description = "EKS Kubernetes control plane version"
  type        = string
  default     = "1.36"
}

variable "allowed_public_cidrs" {
  description = "List of admin workstation/VPN public CIDRs allowed to reach the EKS API server (must not be 0.0.0.0/0)"
  type        = list(string)
}

variable "node_instance_types" {
  description = "EC2 instance types for EKS worker nodes"
  type        = list(string)
  default     = ["t3.large"]
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 4
}

# ------------------------------------------------------------------------------
# ECR Configuration
# ------------------------------------------------------------------------------
variable "ecr_repository_name" {
  description = "Name of the private ECR repository for the sample application"
  type        = string
  default     = "canary-sample-app"
}