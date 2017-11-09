variable "controller_e0" {}
variable "controller_e1" {}

module "controller" {
  source               = "modules\/controller"
  controller_e0        = "${var.controller_e0}"
  controller_e1        = "${var.controller_e1}"
  cidr_block           = "${var.cidr_block}"
  region               = "${var.region}"
  subnet_inside_csr_fw = "${module.base.subnet_inside_csr_fw}"
  subnet_management    = "${module.base.subnet_management}"
  availability_zone    = "${var.availability_zone}"
  aws_key_name         = "${var.aws_key_name}"
  SG_SSH               = "${module.base.SG_SSH}"
  SG_All_Traffic       = "${module.base.SG_All_Traffic}"
}
