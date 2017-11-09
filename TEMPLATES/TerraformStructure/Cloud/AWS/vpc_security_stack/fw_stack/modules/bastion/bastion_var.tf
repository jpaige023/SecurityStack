variable "bastion_instance_type" {
  default = "t2.micro"
}

variable "ami_bastion" {
  type        = "map"
  description = "Bastion by region"

  default = {
    us-east-1 = "ami-8c1be5f6"
    us-west-1 = "ami-02eada62"
    us-west-2 = "ami-e689729e"
  }
}

variable "region" {}
variable "availability_zone" {}
variable "aws_key_name" {}

variable "SG_All_Traffic" {}
variable "SG_SSH" {}

variable "cidr_block" {}
variable "subnet_public" {}
variable "subnet_management" {}

variable "bastion_e0" {}
variable "bastion_e1" {}