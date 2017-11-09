/*
  EIPs
*/
resource "aws_eip" "csr1000v_inside_egress_${var.device_number}_e0" {
  #    instance = "${aws_instance.csr1000v_inside_egress_${var.device_number}.id}"
  network_interface = "${aws_instance.csr1000v_inside_egress_${var.device_number}.network_interface_id}"
  vpc               = true
}

resource "aws_instance" "csr1000v_inside_egress_${var.device_number}" {
  ami                         = "${lookup(var.ami_csr1000v, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.csr1000v_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${aws_security_group.SG_SSH_IPSEC.id}"]
  subnet_id                   = "${aws_subnet.subnet_public.id}"
  associate_public_ip_address = true
  private_ip                  = "${var.csr1000v_inside_egress_${var.device_number}_e0}"
  source_dest_check           = true

  tags {
    Name = "csr1000v_inside_egress_${var.device_number}"
  }
}

/*
  ENI csr_inside_ingress
*/
resource "aws_network_interface" "csr1000v_inside_egress_${var.device_number}_e1" {
  subnet_id         = "${aws_subnet.subnet_inside_csr_fw.id}"
  private_ips       = ["${var.csr1000v_inside_egress_${var.device_number}_e1}"]
  security_groups   = ["${aws_security_group.SG_All_Traffic.id}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.csr1000v_inside_egress_${var.device_number}.id}"
    device_index = 1
  }
}

resource "aws_network_interface" "csr1000v_inside_egress_${var.device_number}_e2" {
  subnet_id         = "${aws_subnet.subnet_management.id}"
  private_ips       = ["${var.csr1000v_inside_egress_${var.device_number}_e2}"]
  security_groups   = ["${aws_security_group.SG_All_Traffic.id}"]
  source_dest_check = true

  attachment {
    instance     = "${aws_instance.csr1000v_inside_egress_${var.device_number}.id}"
    device_index = 2
  }
}
