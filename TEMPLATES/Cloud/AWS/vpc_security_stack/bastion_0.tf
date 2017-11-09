variable "bastion_e0" {}
variable "bastion_e1" {}

module "bastion" {
  source            = "./modules/bastion"
  bastion_e0        = "${var.bastion_e0}"
  bastion_e1        = "${var.bastion_e1}"
  cidr_block        = "${var.cidr_block}"
  region            = "${var.region}"
  subnet_public     = "${module.base.subnet_public}"
  subnet_management = "${module.base.subnet_management}"
  availability_zone = "${var.availability_zone}"
  aws_key_name      = "${var.aws_key_name}"
  SG_SSH            = "${module.base.SG_SSH}"
  SG_All_Traffic    = "${module.base.SG_All_Traffic}"
  name              = "vdss_bastion"
}
