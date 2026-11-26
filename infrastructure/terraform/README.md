# Canary Deployment & Progressive Delivery Platform — AWS Terraform Infrastructure

Production-conscious, cost-optimized AWS infrastructure in `ap-south-1` for running an EKS-based Progressive Delivery stack (Argo Rollouts, Istio, ArgoCD, Prometheus, and Grafana).

## Prerequisites
- AWS CLI v2 configured with default profile (`aws sts get-caller-identity`)
- Terraform CLI `1.14.4` (`terraform version`)
- `kubectl` compatible with Kubernetes `1.36`

---

## Step 1: Bootstrap the S3 Remote State Bucket
Run the bootstrap configuration first to create the encrypted, versioned S3 state bucket with native S3 lockfile support (`use_lockfile = true`).

```bash
cd terraform/bootstrap
terraform init
terraform fmt -check
terraform validate
terraform plan -out=bootstrap.tfplan
terraform apply bootstrap.tfplan