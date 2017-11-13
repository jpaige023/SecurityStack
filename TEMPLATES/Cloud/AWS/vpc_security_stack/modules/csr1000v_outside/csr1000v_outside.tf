/*
  EIPs
*/
resource "aws_eip" "csr1000v_outside_e0" {
  #    instance = "${aws_instance.csr1000v_outside_egress_${var.device_number}.id}"
  network_interface = "${aws_instance.csr1000v_outside.network_interface_id}"
  vpc               = true
}

resource "aws_instance" "csr1000v_outside" {
  ami                         = "${lookup(var.ami_csr1000v, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.csr1000v_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${var.SG_SSH_IPSEC}"]
  subnet_id                   = "${var.subnet_public}"
  associate_public_ip_address = true
  private_ip                  = "${var.csr1000v_outside_e0}"
  source_dest_check           = true

  tags {
    Name = "${var.name}"
    VPC  = "${var.region}_${var.availability_zone}_security_stack"
  }
}

resource "aws_network_interface" "csr1000v_outside_egress_e1" {
  subnet_id         = "${var.subnet_outside_csr_fw}"
  private_ips       = ["${var.csr1000v_outside_e1}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.csr1000v_outside.id}"
    device_index = 1
  }
}

resource "aws_network_interface" "csr1000v_outside_e2" {
  subnet_id         = "${var.subnet_management}"
  private_ips       = ["${var.csr1000v_outside_e2}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = true

  attachment {
    instance     = "${aws_instance.csr1000v_outside.id}"
    device_index = 2
  }
}
