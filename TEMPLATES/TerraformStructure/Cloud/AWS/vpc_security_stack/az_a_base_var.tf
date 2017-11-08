variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_name" {}


variable "region" {
  type = "string"
  description = "The AWS Region"
}

variable "availability_zone" {
  type = "string"
  description = "availability zone"
}

variable "ami_csr1000v" {
  type = "map"
  description = "CSR1000v by region"
  default = {
    us-east-1 = "ami-bcbfb9c7"
    us-west-1 = "ami-99e5d0f9"
    us-west-2 = "ami-e4d43d9c"
  }
}

variable "ami_ftd" {
  type = "map"
  description = "FTD by region"
  default = {
    us-east-1 = "ami-7ff93e69"
    us-west-1 = "ami-f7015d97"
    us-west-2 = "ami-afd550cf"
  }
}

variable "ami_asav" {
  type = "map"
  description = "ASAv by region"
  default = {
    us-east-1 = "ami-b5e0ada2"
    us-west-1 = "ami-2d79304d"
    us-west-2 = "ami-8e60b9ee"
  }
}

variable "ami_bastion" {
  type = "map"
  description = "Bastion by region"
  default = {
    us-east-1 = "ami-8c1be5f6"
    us-west-1 = "ami-02eada62"
    us-west-2 = "ami-e689729e"
  }
}

variable "vpc_security_stack" {
	default = "VPCSecurityStack"
}

variable "csr1000v_instance_type" {
	default = "c4.large"
}

variable "ftd_instance_type" {
	default = "c3.xlarge"
}

variable "asav_instance_type" {
	default = "c3.large"
}

variable "bastion_instance_type" {
	default = "t2.micro"
}


/*
  VPC CIDR and Subnets
*/
variable "cidr_block" {
    description = "CIDR for the whole VPC"
}

variable "subnet_public" {
    description = "Public Subnet"
}

variable "subnet_management" {
    description = "management subnet"
}

variable "subnet_outside_csr_fw" {
    description = "outside csr fw"
}

variable "subnet_inside_csr_fw" {
    description = "inside csr fw"
}

variable "subnet_asav_ftd" {
    description = "asav fw"
}

/*
  IP addresses
*/
variable "az_a_bastion_e0" {
    default = "172.31.0.50"
}

variable "az_a_bastion_e1" {
    default = "172.31.1.4"
}

variable "az_a_csr_inside_e0" {
    default = "172.31.0.10"
}

variable "az_a_csr_inside_e1" {
    default = "172.31.6.4"
}

variable "az_a_csr_inside_e2" {
    default = "172.31.1.7"
}

variable "az_a_csr_outside_e0" {
    default = "172.31.0.20"
}

variable "az_a_csr_outside_e1" {
    default = "172.31.2.4"
}

variable "az_a_csr_outside_e2" {
    default = "172.31.1.8"
}

