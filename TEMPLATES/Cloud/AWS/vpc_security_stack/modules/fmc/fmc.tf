resource "aws_instance" "fmc" {
  ami                         = "${lookup(var.ami_fmc, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.fmc_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${var.SG_All_Traffic}"]
  subnet_id                   = "${var.subnet_management}"
  associate_public_ip_address = false
  private_ip                  = "${var.fmc_e0}"
  source_dest_check           = true

  tags {
    Name = "${var.name}"
    VPC  = "${var.region}_${var.availability_zone}_security_stack"
  }
}

