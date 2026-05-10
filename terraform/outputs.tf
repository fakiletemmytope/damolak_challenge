output "ec2_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.my_instance.public_ip
}

output "ec2_public_dns" {
  description = "Public IP address of the EC2 dns"
  value       = module.my_instance.public_dns
}

output "ec2_instance_id" {
  description = "ID of the EC2 instance"
  value       = module.my_instance.instance_id
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.my_networking.vpc_id
}

output "subnet_id" {
  description = "ID of the subnet"
  value       = module.my_networking.subnet_id
}

output "fqdn" {
  description = "Route53 record fqdn"
  value       = module.my_route53.fqdn
}

output "dns_name" {
  description = "Route53 record dns name"
  value       = module.my_route53.dns_name
}

output "private_key" {
  description = "The private key for SSH access"
  value       = module.key_pair.private_key
  sensitive   = true
}

output "ssm_private_key_name" {
  description = "The name of the SSM parameter storing the private key"
  value       = module.key_pair.ssm_private_key_name
}
