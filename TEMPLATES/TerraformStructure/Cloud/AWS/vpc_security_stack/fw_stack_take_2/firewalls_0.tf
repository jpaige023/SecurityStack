variable "device_number" {
  default = "0"
}

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
  asav_general_e0       = "asav_general_${var.device_number}_e0"
  asav_general_e1       = "asav_general_${var.device_number}_e1"
  asav_general_e2       = "asav_general_${var.device_number}_e2"
  ftd_general_e0        = "ftd_general_${var.device_number}_e0"
  ftd_general_e1        = "ftd_general_${var.device_number}_e1"
  ftd_general_e2        = "ftd_general_${var.device_number}_e2"
  ftd_general_e3        = "ftd_general_${var.device_number}_e3"
}
