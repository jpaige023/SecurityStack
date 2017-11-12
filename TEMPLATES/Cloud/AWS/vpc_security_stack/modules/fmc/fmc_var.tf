variable "fmc_instance_type" {
  default = "c3.xlarge"
}

variable "ami_fmc" {
  type        = "map"
  description = "FMC by region"

  default = {
    us-east-1 = "ami-1df3080b"
    us-west-1 = "ami-4babf62b"
    us-west-2 = "ami-c5219aa5"
  }
}

variable "region" {}
variable "availability_zone" {}
variable "aws_key_name" {}
variable "name" {}

variable "SG_All_Traffic" {}

variable "cidr_block" {}
variable "subnet_management" {}

variable "fmc_e0" {}

