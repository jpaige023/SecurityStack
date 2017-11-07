/*
  Instances
*/
resource "aws_instance" "az_a_asav_0" {
    ami = "${lookup(var.ami_asav, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.asav_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_All_Traffic.id}"]
    subnet_id = "${aws_subnet.az_a_management.id}"
    associate_public_ip_address = false
	private_ip = "${var.az_a_asav_e0_0}"
    source_dest_check = true
    tags {
        Name = "az_a_asav_0"
    }
}

resource "aws_instance" "az_a_ftd_0" {
    ami = "${lookup(var.ami_ftd, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.ftd_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_All_Traffic.id}"]
    subnet_id = "${aws_subnet.az_a_management.id}"
    associate_public_ip_address = false
	private_ip = "${var.az_a_ftd_e0_0}"
    source_dest_check = true
    user_data = "${file("ftd.conf")}"
    tags {
        Name = "az_a_ftd_0"
    }
}


/*
  ENI az_a_asav_0
*/
resource "aws_network_interface" "az_a_asav_e1_0" {
	subnet_id = "${aws_subnet.az_a_outside_f5_asav.id}"
	private_ips = ["${var.az_a_asav_e1_0}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_asav_0.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "az_a_asav_e2_0" {
	subnet_id = "${aws_subnet.az_a_asav_ftd.id}"
	private_ips = ["${var.az_a_asav_e2_0}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_asav_0.id}"
		device_index = 2
	}
}

/*
  ENI az_a_ftd
*/
resource "aws_network_interface" "az_a_ftd_e1_0" {
	subnet_id = "${aws_subnet.az_a_management.id}"
	private_ips = ["${var.az_a_ftd_e1_0}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = true
	attachment {
		instance = "${aws_instance.az_a_ftd_0.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "az_a_ftd_e2_0" {
	subnet_id = "${aws_subnet.az_a_asav_ftd.id}"
	private_ips = ["${var.az_a_ftd_e2_0}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_ftd_0.id}"
		device_index = 2
	}
}

resource "aws_network_interface" "az_a_ftd_e3_0" {
	subnet_id = "${aws_subnet.az_a_inside_f5_ftd.id}"
	private_ips = ["${var.az_a_ftd_e3_0}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_ftd_0.id}"
		device_index = 3
	}
}