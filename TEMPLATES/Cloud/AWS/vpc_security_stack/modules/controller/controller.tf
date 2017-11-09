resource "aws_instance" "controller" {
  ami                         = "${lookup(var.ami_controller, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.controller_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${var.SG_SSH}"]
  subnet_id                   = "${var.subnet_management}"
  associate_public_ip_address = true
  private_ip                  = "${var.controller_e0}"
  source_dest_check           = true

  tags {
    Name = "${var.name}"
    VPC  = "${var.region}_${var.availability_zone}_security_stack"
  }
}

resource "aws_network_interface" "controller_e1" {
  subnet_id         = "${var.subnet_inside_csr_fw}"
  private_ips       = ["${var.controller_e1}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = true

  attachment {
    instance     = "${aws_instance.controller.id}"
    device_index = 1
  }
}
