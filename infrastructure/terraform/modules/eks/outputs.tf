output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.this.name
}

output "cluster_arn" {
  description = "EKS cluster ARN"
  value       = aws_eks_cluster.this.arn
}

output "cluster_endpoint" {
  description = "Endpoint URL for the Kubernetes API server"
  value       = aws_eks_cluster.this.endpoint
}

output "cluster_version" {
  description = "Running Kubernetes version of the cluster"
  value       = aws_eks_cluster.this.version
}

output "cluster_certificate_authority_data" {
  description = "Base64-encoded certificate authority data for the cluster"
  value       = aws_eks_cluster.this.certificate_authority[0].data
}

output "oidc_provider_arn" {
  description = "ARN of the IAM OIDC provider for IRSA"
  value       = aws_iam_openid_connect_provider.eks.arn
}

output "oidc_provider_url" {
  description = "URL of the IAM OIDC provider for IRSA"
  value       = aws_iam_openid_connect_provider.eks.url
}

output "node_group_role_arn" {
  description = "IAM Role ARN used by the managed worker nodes"
  value       = aws_iam_role.node.arn
}