variable "repository_name" {
  description = "Name of the private ECR repository for the sample canary application"
  type        = string
}

variable "image_tag_mutability" {
  description = "Tag mutability setting for the repository (MUTABLE or IMMUTABLE)"
  type        = string
  default     = "MUTABLE"
}

variable "scan_on_push" {
  description = "Enable automated vulnerability scanning on image push"
  type        = bool
  default     = true
}

variable "untagged_image_retention_days" {
  description = "Number of days to keep untagged images before expiring"
  type        = number
  default     = 7
}

variable "max_tagged_image_count" {
  description = "Maximum number of tagged images to retain"
  type        = number
  default     = 15
}

variable "force_delete" {
  description = "Allow deleting the repository even if it contains images (useful for dev/demo teardown)"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Common tags for the ECR repository"
  type        = map(string)
  default     = {}
}