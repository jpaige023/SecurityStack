resource "aws_eip" "bastion_e0" {
  instance          = "${aws_instance.bastion.id}"
  network_interface = "${aws_instance.bastion.network_interface_id}"
  vpc               = true
}

resource "aws_instance" "bastion" {
  ami                         = "${lookup(var.ami_bastion, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.bastion_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${var.SG_SSH}"]
  subnet_id                   = "${var.subnet_public}"
  associate_public_ip_address = true
  private_ip                  = "${var.bastion_e0}"
  source_dest_check           = true

  tags {
    Name = "${var.name}"
    VPC  = "${var.region}_${var.availability_zone}_security_stack"
  }
}

resource "aws_network_interface" "bastion_e1" {
  subnet_id         = "${var.subnet_management}"
  private_ips       = ["${var.bastion_e1}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = true

  attachment {
    instance     = "${aws_instance.bastion.id}"
    device_index = 1
  }
}
