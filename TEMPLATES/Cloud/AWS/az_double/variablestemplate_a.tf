variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_name" {}

variable "IAM_Role" {
  default = "ChangeRouteRole"
}

variable "aws_region" {
  default = "cloud_provider_region"
}

#variable "amis" {
#    description = "AMIs by region"
#    default = {
#        us-east-1 = "ami-8a91ae9d" # CSR1000v
#    }
#}
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

variable "private_subnetA_cidr_users" {
  description = "CIDR for the Private Subnet"
  default     = "users_subnet_a"
}

variable "G2_static_private_ipA" {
  default = "router_a_address_g2"
}

variable "public_subnetB_cidr" {
  description = "CIDR for the Public Subnet"
  default     = "router_b_subnet_g1"
}

variable "G1_static_private_ipB" {
  default = "router_b_address_g1"
}

variable "private_subnetB_cidr" {
  description = "CIDR for the Private Subnet"
  default     = "router_b_subnet_g2"
}

variable "private_subnetB_cidr_users" {
  description = "CIDR for the Private Subnet"
  default     = "users_subnet_b"
}

variable "G2_static_private_ipB" {
  default = "router_b_address_g2"
}
