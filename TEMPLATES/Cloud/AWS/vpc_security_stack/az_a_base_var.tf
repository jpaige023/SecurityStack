variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_name" {}


variable "aws_region" {
  type = "string"
  description = "The AWS Region"
}

variable "aws_az_a" {
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

variable "ami_f5" {
  type = "map"
  description = "F5 by region"
  default = {
    us-east-1 = "ami-4c76185a"
    us-west-1 = "ami-e56d4b85"
    us-west-2 = "ami-a4bc27c4"
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

variable "f5_instance_type" {
	default = "t2.medium"
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
variable "vpc_cidr" {
    description = "CIDR for the whole VPC"
    default = "172.31.0.0/21"
}

variable "az_a_public" {
    description = "az_a_public"
    default = "172.31.0.0/24"
}

variable "az_a_management" {
    description = "az_a_management"
    default = "172.31.1.0/24"
}

variable "az_a_outside_csr_f5" {
    description = "az_a_outside_csr_f5"
    default = "172.31.2.0/24"
}

variable "az_a_outside_f5_asav" {
    description = "az_a_outside_f5_asav"
    default = "172.31.3.0/24"
}

variable "az_a_asav_ftd" {
    description = "az_a_asav_ftd"
    default = "172.31.4.0/24"
}

variable "az_a_inside_f5_ftd" {
    description = "az_a_inside_f5_ftd"
    default = "172.31.5.0/24"
}

variable "az_a_inside_csr_f5" {
    description = "az_a_inside_csr_f5"
    default = "172.31.6.0/24"
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

variable "az_a_f5_inside_e0" {
    default = "172.31.1.5"
}

variable "az_a_f5_inside_e1" {
    default = "172.31.6.5"
}

variable "az_a_f5_inside_e2" {
    default = "172.31.5.4"
}

variable "az_a_f5_outside_e0" {
    default = "172.31.1.6"
}

variable "az_a_f5_outside_e1" {
    default = "172.31.2.5"
}

variable "az_a_f5_outside_e2" {
    default = "172.31.3.4"
}
