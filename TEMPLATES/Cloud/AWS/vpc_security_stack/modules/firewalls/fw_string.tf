/*
  Instances
*/
resource "aws_instance" "asav_general" {
  ami                         = "${lookup(var.ami_asav, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.asav_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${var.SG_All_Traffic}"]
  subnet_id                   = "${var.subnet_management}"
  associate_public_ip_address = false
  private_ip                  = "${var.asav_general_e0}"
  source_dest_check           = true

  tags {
    Name = "asav_general"
  }
}

resource "aws_instance" "ftd_general" {
  ami                         = "${lookup(var.ami_ftd, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.ftd_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${var.SG_All_Traffic}"]
  subnet_id                   = "${var.subnet_management}"
  associate_public_ip_address = false
  private_ip                  = "${var.ftd_general_e0}"
  source_dest_check           = true

  #    user_data = "${file("ftd.conf")}"
  tags {
    Name = "ftd_general"
  }
}

/*
  ENIs asav
*/
resource "aws_network_interface" "asav_general_e1" {
  subnet_id         = "${var.subnet_outside_csr_fw}"
  private_ips       = ["${var.asav_general_e1}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.asav_general.id}"
    device_index = 1
  }
}

resource "aws_network_interface" "asav_general_e2" {
  subnet_id         = "${var.subnet_asav_ftd}"
  private_ips       = ["${var.asav_general_e2}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.asav_general.id}"
    device_index = 2
  }
}

/*
  ENIs ftd
*/
resource "aws_network_interface" "ftd_general_e1" {
  subnet_id         = "${var.subnet_management}"
  private_ips       = ["${var.ftd_general_e1}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = true

  attachment {
    instance     = "${aws_instance.ftd_general.id}"
    device_index = 1
  }
}

resource "aws_network_interface" "ftd_general_e2" {
  subnet_id         = "${var.subnet_inside_csr_fw}"
  private_ips       = ["${var.ftd_general_e2}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.ftd_general.id}"
    device_index = 2
  }
}

resource "aws_network_interface" "ftd_general_e3" {
  subnet_id         = "${var.subnet_asav_ftd}"
  private_ips       = ["${var.ftd_general_e3}"]
  security_groups   = ["${var.SG_All_Traffic}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.ftd_general.id}"
    device_index = 3
  }
}
