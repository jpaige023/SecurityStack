variable "fmc_e0" {}

module "fmc" {
  source               = "./modules/fmc"
  fmc_e0        = "${var.fmc_e0}"
  cidr_block           = "${var.cidr_block}"
  region               = "${var.region}"
  subnet_management    = "${module.base.subnet_management}"
  availability_zone    = "${var.availability_zone}"
  aws_key_name         = "${var.aws_key_name}"
  SG_All_Traffic       = "${module.base.SG_All_Traffic}"
  name                 = "vdss_fmc"
}
