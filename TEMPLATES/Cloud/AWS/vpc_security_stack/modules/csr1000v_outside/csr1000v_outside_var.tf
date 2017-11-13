variable "csr1000v_instance_type" {
  default = "c4.large"
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

variable "aws_key_name" {}
variable "region" {}
variable "availability_zone" {}
variable "name" {}

variable "SG_All_Traffic" {}
variable "SG_SSH_IPSEC" {}

variable "subnet_public" {}
variable "subnet_management" {}
variable "subnet_outside_csr_fw" {}

variable "csr1000v_outside_e0" {}
variable "csr1000v_outside_e1" {}
variable "csr1000v_outside_e2" {}
