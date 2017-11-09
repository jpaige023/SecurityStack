variable "asav_general_0_e0" {}
variable "asav_general_0_e1" {}
variable "asav_general_0_e2" {}
variable "ftd_general_0_e0" {}
variable "ftd_general_0_e1" {}
variable "ftd_general_0_e2" {}
variable "ftd_general_0_e3" {}

module "firewalls" {
  source                = "./modules/firewalls"
  region                = "${var.region}"
  subnet_asav_ftd       = "${module.base.subnet_asav_ftd}"
  subnet_management     = "${module.base.subnet_management}"
  subnet_inside_csr_fw  = "${module.base.subnet_inside_csr_fw}"
  subnet_outside_csr_fw = "${module.base.subnet_outside_csr_fw}"
  availability_zone     = "${var.availability_zone}"
  aws_key_name          = "${var.aws_key_name}"
  SG_SSH                = "${module.base.SG_SSH}"
  SG_All_Traffic        = "${module.base.SG_All_Traffic}"
  asav_general_e0       = "${var.asav_general_0_e0}"
  asav_general_e1       = "${var.asav_general_0_e1}"
  asav_general_e2       = "${var.asav_general_0_e2}"
  ftd_general_e0        = "${var.ftd_general_0_e0}"
  ftd_general_e1        = "${var.ftd_general_0_e1}"
  ftd_general_e2        = "${var.ftd_general_0_e2}"
  ftd_general_e3        = "${var.ftd_general_0_e3}"
}
