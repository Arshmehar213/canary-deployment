terraform {
  backend "s3" {
    # Replace bucket name via -backend-config="bucket=<STATE_BUCKET_NAME>" during `terraform init`
    bucket       = "REPLACE_WITH_BOOTSTRAP_BUCKET_NAME"
    key          = "environments/dev/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}