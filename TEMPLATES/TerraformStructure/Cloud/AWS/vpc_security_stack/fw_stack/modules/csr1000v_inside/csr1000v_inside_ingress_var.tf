variable "csr1000v_inside_e0" {}

variable "csr1000v_inside_e1" {}

variable "csr1000v_inside_e2" {}
variable "aws_key_name" {}
variable "SG_All_Traffic" {}
variable "SG_SSH_IPSEC" {}
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


variable "csr1000v_instance_type" {
  default = "c4.large"
}

variable "subnet_public" {
  description = "Public Subnet"
}

variable "subnet_management" {
  description = "management subnet"
}

variable "subnet_inside_csr_fw" {
  description = "inside csr fw"
}