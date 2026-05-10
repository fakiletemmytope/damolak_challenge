module "my_networking" {
  source      = "./modules/network"
  vpc_cidr    = "10.0.0.0/16"
  vpc_name    = "damolak-vpc"
  subnet_cidr = "10.0.1.0/24"
  subnet_name = "damolak-subnet"
  az          = "us-east-1a"
  igw_name    = "damolak-igw"
  rt_name     = "damolak-rt"
}


module "my_instance" {
  source        = "./modules/ec2"
  ami           = "ami-0360c520857e3138f"
  instance_type = "t2.micro"
  ec2_name      = "damolak-instance"
  subnet_id     = module.my_networking.subnet_id
  key_name      = module.key_pair.key_name
  vpc_id        = module.my_networking.vpc_id
  domain_name   = "temmytope.online"
}


module "my_cloudwatch" {
  source           = "./modules/cloudwatch"
  cw_name          = "damolak_instance_cw"
  cw_agent_profile = "damolak_cw_agent"
  instance_id      = module.my_instance.instance_id
}

module "my_route53" {
  source        = "./modules/route"
  subdomain     = "damolak"
  domain_name   = "temmytope.online"
  ec2_public_ip = module.my_instance.public_ip
}

module "key_pair" {
  source = "./modules/key_pair"
  key_pair_name = "damolak_key"
}
