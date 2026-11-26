variable "name_prefix" {
  description = "Name prefix for VPC resources"
  type        = string
}

variable "cluster_name" {
  description = "EKS cluster name used for Kubernetes subnet discovery tags"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "availability_zones" {
  description = "List of Availability Zone names (e.g., ap-south-1a, ap-south-1b)"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]

  validation {
    condition     = length(var.availability_zones) == 2
    error_message = "Exactly 2 Availability Zones must be provided for the 2-AZ subnet layout."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the two public subnets"
  type        = list(string)
  default     = ["10.20.1.0/24", "10.20.2.0/24"]

  validation {
    condition     = length(var.public_subnet_cidrs) == 2
    error_message = "Exactly 2 public subnet CIDRs must be specified."
  }
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the two private subnets"
  type        = list(string)
  default     = ["10.20.16.0/20", "10.20.32.0/20"]

  validation {
    condition     = length(var.private_subnet_cidrs) == 2
    error_message = "Exactly 2 private subnet CIDRs must be specified."
  }
}

variable "tags" {
  description = "Common tags applied to VPC resources"
  type        = map(string)
  default     = {}
}