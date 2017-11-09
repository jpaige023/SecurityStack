variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_key_name" {}
variable "cidr_block" {}
variable "region" {}
variable "subnet_public" {}
variable "subnet_management" {}
variable "subnet_inside_csr_fw" {}
variable "subnet_outside_csr_fw" {}
variable "subnet_asav_ftd" {}
variable "availability_zone" {}

module "base" {
  source                = "./modules/base"
  cidr_block            = "${var.cidr_block}"
  region                = "${var.region}"
  subnet_public         = "${var.subnet_public}"
  subnet_management     = "${var.subnet_management}"
  subnet_inside_csr_fw  = "${var.subnet_inside_csr_fw}"
  subnet_outside_csr_fw = "${var.subnet_outside_csr_fw}"
  subnet_asav_ftd       = "${var.subnet_asav_ftd}"
  availability_zone     = "${var.availability_zone}"
}
