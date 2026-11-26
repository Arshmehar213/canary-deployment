variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes minor version for the EKS control plane"
  type        = string
  default     = "1.36"
}

variable "vpc_id" {
  description = "VPC ID where the cluster will be deployed"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for control plane ENIs and worker nodes"
  type        = list(string)
}

variable "endpoint_private_access" {
  description = "Enable private API server endpoint access inside the VPC"
  type        = bool
  default     = true
}

variable "endpoint_public_access" {
  description = "Enable public API server endpoint access restricted by CIDR"
  type        = bool
  default     = true
}

variable "allowed_public_cidrs" {
  description = "List of CIDR blocks permitted to reach the public EKS API endpoint (0.0.0.0/0 is forbidden)"
  type        = list(string)

  validation {
    condition     = !contains(var.allowed_public_cidrs, "0.0.0.0/0")
    error_message = "Security policy violation: Public Kubernetes API access must not be open to 0.0.0.0/0. Specify your workstation/VPN CIDR (e.g., [\"203.0.113.10/32\"])."
  }
}

variable "cluster_enabled_log_types" {
  description = "Control plane log types to enable selectively"
  type        = list(string)
  default     = ["api", "audit", "authenticator"]
}

variable "log_retention_in_days" {
  description = "CloudWatch log retention in days for EKS control plane logs"
  type        = number
  default     = 7
}

variable "node_instance_types" {
  description = "EC2 instance types for the managed node group"
  type        = list(string)
  default     = ["t3.large"]
}

variable "node_ami_type" {
  description = "AMI type for EKS worker nodes"
  type        = string
  default     = "AL2023_x86_64_STANDARD"
}

variable "node_capacity_type" {
  description = "Capacity type (ON_DEMAND or SPOT)"
  type        = string
  default     = "ON_DEMAND"
}

variable "node_disk_size" {
  description = "Root EBS volume size in GiB for worker nodes"
  type        = number
  default     = 30
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

variable "tags" {
  description = "Common tags for all EKS resources"
  type        = map(string)
  default     = {}
}