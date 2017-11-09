variable "aws_key_name" {}
variable "SG_All_Traffic" {}
variable "SG_SSH" {}
variable "bastion_e0" {}
variable "bastion_e1" {}

variable "region" {
  type        = "string"
  description = "The AWS Region"
}

variable "availability_zone" {
  type        = "string"
  description = "availability zone"
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

variable "bastion_instance_type" {
  default = "t2.micro"
}

variable "cidr_block" {
  description = "CIDR for the whole VPC"
}

variable "subnet_public" {
  description = "Public Subnet"
}

variable "subnet_management" {
  description = "management subnet"
}
