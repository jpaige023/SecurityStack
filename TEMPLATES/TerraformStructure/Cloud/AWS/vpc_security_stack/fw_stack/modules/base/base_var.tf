variable "region" {
  type        = "string"
  description = "The AWS Region"
}

variable "availability_zone" {
  type        = "string"
  description = "availability zone"
}

variable "ami_csr1000v" {
  type        = "map"
  description = "CSR1000v by region"

  default = {
    us-east-1 = "ami-bcbfb9c7"
    us-west-1 = "ami-99e5d0f9"
    us-west-2 = "ami-e4d43d9c"
  }
}

variable "vpc_security_stack" {
  default = "VPCSecurityStack"
}

variable "csr1000v_instance_type" {
  default = "c4.large"
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
