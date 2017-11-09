variable "csr1000v_inside_egress_0_e0" {}
variable "csr1000v_inside_egress_0_e1" {}
variable "csr1000v_inside_egress_0_e2" {}

module "csr1000v_inside_egress" {
  source               = "./modules/csr1000v_inside"
  region               = "${var.region}"
  subnet_public        = "${module.base.subnet_public}"
  subnet_management    = "${module.base.subnet_management}"
  subnet_inside_csr_fw = "${module.base.subnet_inside_csr_fw}"
  availability_zone    = "${var.availability_zone}"
  aws_key_name         = "${var.aws_key_name}"
  SG_SSH_IPSEC         = "${module.base.SG_SSH_IPSEC}"
  SG_All_Traffic       = "${module.base.SG_All_Traffic}"
  csr1000v_inside_e0   = "${var.csr1000v_inside_egress_0_e0}"
  csr1000v_inside_e1   = "${var.csr1000v_inside_egress_0_e1}"
  csr1000v_inside_e2   = "${var.csr1000v_inside_egress_0_e2}"
  name                 = "vdss_csr1000v_inside_egress_XXXXX"
}
