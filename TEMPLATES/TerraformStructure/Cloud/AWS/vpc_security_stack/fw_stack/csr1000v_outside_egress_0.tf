variable "csr1000v_outside_egress_0_e0" {}
variable "csr1000v_outside_egress_0_e1" {}
variable "csr1000v_outside_egress_0_e2" {}

module "csr1000v_outside_egress" {
  source                = "./modules/csr1000v_outside"
  region                = "${var.region}"
  subnet_public         = "${module.base.subnet_public}"
  subnet_management     = "${module.base.subnet_management}"
  subnet_outside_csr_fw = "${module.base.subnet_outside_csr_fw}"
  availability_zone     = "${var.availability_zone}"
  aws_key_name          = "${var.aws_key_name}"
  SG_SSH_IPSEC          = "${module.base.SG_SSH_IPSEC}"
  SG_All_Traffic        = "${module.base.SG_All_Traffic}"
  csr1000v_outside_e0   = "${var.csr1000v_outside_egress_0_e0}"
  csr1000v_outside_e1   = "${var.csr1000v_outside_egress_0_e1}"
  csr1000v_outside_e2   = "${var.csr1000v_outside_egress_0_e2}"
}
