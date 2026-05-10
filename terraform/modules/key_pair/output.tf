output "key_name" {
  value = aws_key_pair.main.key_name
}

output "private_key" {
  value     = tls_private_key.main.private_key_pem
  sensitive = true
}

output "ssm_private_key_name" {
  value = aws_ssm_parameter.private_key.name
}
