/*
  Instances
*/
resource "aws_instance" "asav_general_${var.device_number}" {
    ami = "${lookup(var.ami_asav, var.region)}"
    availability_zone = "${var.availability_zone}"
    instance_type = "${var.asav_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_All_Traffic.id}"]
    subnet_id = "${aws_subnet.subnet_management.id}"
    associate_public_ip_address = false
	private_ip = "${var.asav_general_${var.device_number}_e0}"
    source_dest_check = true
    tags {
        Name = "asav_general_${var.device_number}"
    }
}

resource "aws_instance" "ftd_general_${var.device_number}" {
    ami = "${lookup(var.ami_ftd, var.region)}"
    availability_zone = "${var.availability_zone}"
    instance_type = "${var.ftd_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_All_Traffic.id}"]
    subnet_id = "${aws_subnet.subnet_management.id}"
    associate_public_ip_address = false
	private_ip = "${var.ftd_general_${var.device_number}_e0}"
    source_dest_check = true
#    user_data = "${file("ftd.conf")}"
    tags {
        Name = "ftd_general_${var.device_number}"
    }
}


/*
  ENI az_a_asav_0
*/
resource "aws_network_interface" "asav_general_${var.device_number}_e1" {
	subnet_id = "${aws_subnet.subnet_outside_csr_fw.id}"
	private_ips = ["${var.asav_general_${var.device_number}_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.asav_general_${var.device_number}.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "asav_general_${var.device_number}_e2" {
	subnet_id = "${aws_subnet.subnet_asav_ftd.id}"
	private_ips = ["${var.asav_general_${var.device_number}_e2}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.asav_general_${var.device_number}.id}"
		device_index = 2
	}
}

/*
  ENI az_a_ftd
*/
resource "aws_network_interface" "ftd_general_${var.device_number}_e1" {
	subnet_id = "${aws_subnet.subnet_management}"
	private_ips = ["${var.ftd_general_${var.device_number}_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = true
	attachment {
		instance = "${aws_instance.ftd_general_${var.device_number}.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "ftd_general_${var.device_number}_e2" {
	subnet_id = "${aws_subnet.subnet_asav_ftd}"
	private_ips = ["${var.ftd_general_${var.device_number}_e2}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.ftd_general_${var.device_number}.id}"
		device_index = 2
	}
}

resource "aws_network_interface" "ftd_general_${var.device_number}_e3" {
	subnet_id = "${aws_subnet.subnet_inside_csr_fw}"
	private_ips = ["${var.ftd_general_${var.device_number}_e3}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.ftd_general_${var.device_number}.id}"
		device_index = 3
	}
}