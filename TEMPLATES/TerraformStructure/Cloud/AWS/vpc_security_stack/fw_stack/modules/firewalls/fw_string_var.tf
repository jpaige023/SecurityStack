variable "aws_key_name" {}
variable "SG_All_Traffic" {}
variable "SG_SSH" {}
variable "asav_general_e0" {}
variable "asav_general_e1" {}
variable "asav_general_e2" {}
variable "ftd_general_e0" {}
variable "ftd_general_e1" {}
variable "ftd_general_e2" {}
variable "ftd_general_e3" {}


variable "region" {
  type        = "string"
  description = "The AWS Region"
}

variable "availability_zone" {
  type        = "string"
  description = "availability zone"
}

variable "region" {
  type        = "string"
  description = "The AWS Region"
}

variable "availability_zone" {
  type        = "string"
  description = "availability zone"
}

variable "ami_ftd" {
  type        = "map"
  description = "FTD by region"

  default = {
    us-east-1 = "ami-7ff93e69"
    us-west-1 = "ami-f7015d97"
    us-west-2 = "ami-afd550cf"
  }
}

variable "ami_asav" {
  type        = "map"
  description = "ASAv by region"

  default = {
    us-east-1 = "ami-b5e0ada2"
    us-west-1 = "ami-2d79304d"
    us-west-2 = "ami-8e60b9ee"
  }
}

variable "ftd_instance_type" {
  default = "c3.xlarge"
}

variable "asav_instance_type" {
  default = "c3.large"
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
