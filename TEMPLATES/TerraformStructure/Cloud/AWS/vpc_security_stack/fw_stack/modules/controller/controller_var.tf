variable "controller_instance_type" {
  default = "t2.micro"
}

variable "ami_controller" {
  type        = "map"
  description = "Controller by region"

  default = {
    us-east-1 = "ami-b391b9c8"
    us-west-1 = "ami-8edbf0ee"
    us-west-2 = "ami-9d04e4e5"
  }
}

variable "region" {}
variable "availability_zone" {}
variable "aws_key_name" {}

variable "SG_All_Traffic" {}
variable "SG_SSH" {}

variable "cidr_block" {}
variable "subnet_management" {}
variable "subnet_inside_csr_fw" {}

variable "controller_e0" {}
variable "controller_e1" {}
