variable "region" {
  type        = "string"
  description = "The AWS Region"
}

variable "availability_zone" {
  type        = "string"
  description = "availability zone"
}

variable "vpc_security_stack" {
  default = "VPCSecurityStack"
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
