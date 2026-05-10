# Generate the key pair
resource "tls_private_key" "main" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Register the public key with AWS
resource "aws_key_pair" "main" {
  key_name   = var.key_pair_name
  public_key = tls_private_key.main.public_key_openssh
}

resource "aws_ssm_parameter" "private_key" {
  name  = "/damolak/ec2-private-key"
  type  = "SecureString"
  value = tls_private_key.main.private_key_pem
}