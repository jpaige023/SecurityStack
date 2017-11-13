variable "ami_csr1000v" {
  type        = "map"
  description = "CSR1000v by region"

  default = {
    us-east-1 = "ami-bcbfb9c7"
    us-west-1 = "ami-99e5d0f9"
    us-west-2 = "ami-e4d43d9c"
  }
}

variable "csr1000v_instance_type" {}

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_name" {}

variable "region" {}
variable "availability_zone" {}
variable "vpc_number" {}
variable "cidr_block" {}

variable "router_a_subnet_g1" {}
variable "router_a_address_g1" {}
variable "router_a_subnet_g2" {}
variable "router_a_address_g2" {}

variable "dmvpn_role" {}
variable "dmvpn_tunnel" {}
