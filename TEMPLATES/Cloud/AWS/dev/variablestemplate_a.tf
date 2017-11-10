variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_name" {}

variable "aws_region" {
  default = "cloud_provider_region"
}

variable "vpc_NAME" {
  default = "VPC_XXX"
}

variable "CSR1000v_instance_type" {
  default = "cloud_instance_size"
}

variable "vpc_cidr" {
  description = "CIDR for the whole VPC"
  default     = "cidr_block"
}

variable "public_subnetA_cidr" {
  description = "CIDR for the Public Subnet"
  default     = "router_a_subnet_g1"
}

variable "G1_static_private_ipA" {
  default = "router_a_address_g1"
}

variable "private_subnetA_cidr" {
  description = "CIDR for the Private Subnet"
  default     = "router_a_subnet_g2"
}

variable "G2_static_private_ipA" {
  default = "router_a_address_g2"
}
