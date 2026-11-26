variable "aws_region" {
  description = "AWS region for the Terraform state S3 bucket"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project prefix used for naming resources"
  type        = string
  default     = "canary-platform"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "state_bucket_name" {
  description = "Optional custom S3 bucket name. If empty, defaults to <project>-<env>-tfstate-<account_id>."
  type        = string
  default     = ""
}

variable "force_destroy" {
  description = "Allow bucket destruction even if state versions exist (set true only for ephemeral demo cleanup)"
  type        = bool
  default     = false
}