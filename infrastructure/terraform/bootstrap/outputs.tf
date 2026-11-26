output "state_bucket_name" {
  description = "Name of the S3 bucket created for Terraform state"
  value       = aws_s3_bucket.terraform_state.bucket
}

output "state_bucket_arn" {
  description = "ARN of the S3 bucket created for Terraform state"
  value       = aws_s3_bucket.terraform_state.arn
}

output "aws_region" {
  description = "Region of the state bucket"
  value       = var.aws_region
}