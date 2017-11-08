resource "aws_eip" "bastion_e0" {
    instance = "${aws_instance.bastion.id}"
    network_interface = "${aws_instance.bastion.network_interface_id}"
    vpc = true
}

resource "aws_instance" "bastion" {
    ami = "${lookup(var.ami_bastion, var.region)}"
    availability_zone = "${var.availability_zone}"
    instance_type = "${var.bastion_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_SSH.id}"]
    subnet_id = "${aws_subnet.subnet_public.id}"
    associate_public_ip_address = true
	private_ip = "${var.bastion_e0}"
    source_dest_check = true
    tags {
        Name = "bastion"
    }
}
/*
  ENI az_a_bastion
*/
resource "aws_network_interface" "bastion_e1" {
	subnet_id = "${aws_subnet.subnet_management.id}"
	private_ips = ["${var.bastion_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = true
	attachment {
		instance = "${aws_instance.bastion.id}"
		device_index = 1
	}
}
