resource "aws_vpc" "default" {
    cidr_block = "${var.vpc_cidr}"
    enable_dns_hostnames = true
    tags {
        Name = "${var.vpc_security_stack}"
    }
}

resource "aws_internet_gateway" "default" {
    vpc_id = "${aws_vpc.default.id}"
}

/*
  Public Subnet
*/
resource "aws_subnet" "az_a_public" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_public}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_public"
    }
}

resource "aws_route_table" "public" {
    vpc_id = "${aws_vpc.default.id}"
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.default.id}"
    }
    tags {
        Name = "Public Subnets"
    }
}

resource "aws_route_table_association" "public_rt_az_a_public" {
    subnet_id = "${aws_subnet.az_a_public.id}"
    route_table_id = "${aws_route_table.public.id}"
}


/*
  Private Subnets
*/
resource "aws_route_table" "private" {
    vpc_id = "${aws_vpc.default.id}"
    tags {
        Name = "Private Subnets"
    }
}

resource "aws_subnet" "az_a_management" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_management}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_management"
    }
}

resource "aws_route_table_association" "private_rt_az_a_management" {
    subnet_id = "${aws_subnet.az_a_management.id}"
    route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "az_a_outside_csr_f5" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_outside_csr_f5}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_outside_csr_f5"
    }
}

resource "aws_route_table_association" "private_rt_az_a_outside_csr_f5" {
    subnet_id = "${aws_subnet.az_a_outside_csr_f5.id}"
    route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "az_a_outside_f5_asav" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_outside_f5_asav}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_outside_f5_asav"
    }
}

resource "aws_route_table_association" "private_rt_az_a_outside_f5_asav" {
    subnet_id = "${aws_subnet.az_a_outside_f5_asav.id}"
    route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "az_a_asav_ftd" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_asav_ftd}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_asav_ftd"
    }
}

resource "aws_route_table_association" "private_rt_az_a_asav_ftd" {
    subnet_id = "${aws_subnet.az_a_asav_ftd.id}"
    route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "az_a_inside_f5_ftd" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_inside_f5_ftd}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_inside_f5_ftd"
    }
}

resource "aws_route_table_association" "private_rt_az_a_inside_f5_ftd" {
    subnet_id = "${aws_subnet.az_a_inside_f5_ftd.id}"
    route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "az_a_inside_csr_f5" {
    vpc_id = "${aws_vpc.default.id}"
    cidr_block = "${var.az_a_inside_csr_f5}"
    availability_zone = "${var.aws_az_a}"
    tags {
        Name = "az_a_inside_csr_f5"
    }
}

resource "aws_route_table_association" "private_rt_az_a_inside_csr_f5" {
    subnet_id = "${aws_subnet.az_a_inside_csr_f5.id}"
    route_table_id = "${aws_route_table.private.id}"
}


/*
  Security Groups - SG_SSH_IPSEC, SG_SSH, SG_All_Traffic
*/
resource "aws_security_group" "SG_SSH_IPSEC" {
    name = "SG_SSH_IPSEC"
    description = "Allow Traffic into the CSR1000v"

    ingress {
        from_port = 4500
        to_port = 4500
        protocol = "udp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 0
        to_port = 0
        protocol = "50"
        cidr_blocks = ["${var.vpc_cidr}"]
    }
    ingress {
        from_port = 500
        to_port = 500
        protocol = "udp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = -1
        to_port = -1
        protocol = "icmp"
        cidr_blocks = ["0.0.0.0/0"]
    }
	egress {
		from_port = 0
		to_port = 0
		protocol = "-1"
		cidr_blocks = ["0.0.0.0/0"]
    }

    vpc_id = "${aws_vpc.default.id}"

    tags {
        Name = "SG_SSH_IPSEC"
    }
}

resource "aws_security_group" "SG_SSH" {
    name = "SG_SSH"
    description = "Only SSH incoming"


    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = -1
        to_port = -1
        protocol = "icmp"
        cidr_blocks = ["0.0.0.0/0"]
    }
	egress {
		from_port = 0
		to_port = 0
		protocol = "-1"
		cidr_blocks = ["0.0.0.0/0"]
    }

    vpc_id = "${aws_vpc.default.id}"

    tags {
        Name = "SG_SSH"
    }
}

resource "aws_security_group" "SG_All_Traffic" {
    name = "SG_All_Traffic"
    description = "Allow Traffic into the G2 CSR1000v"

    ingress {
        from_port = 0
        to_port = 0
        protocol = -1
        cidr_blocks = ["0.0.0.0/0"]
    }
	egress {
		from_port = 0
		to_port = 0
		protocol = "-1"
		cidr_blocks = ["0.0.0.0/0"]
    }

    vpc_id = "${aws_vpc.default.id}"

    tags {
        Name = "SG_All_Traffic"
    }
}

/*
  EIPs
*/
resource "aws_eip" "az_a_bastion_e0" {
#    instance = "${aws_instance.az_a_bastion.id}"
    network_interface = "${aws_instance.az_a_bastion.network_interface_id}"
    vpc = true
}

resource "aws_eip" "az_a_csr_inside_e0" {
#    instance = "${aws_instance.az_a_csr_inside.id}"
    network_interface = "${aws_instance.az_a_csr_inside.network_interface_id}"
    vpc = true
}

resource "aws_eip" "az_a_csr_outside_e0" {
#    instance = "${aws_instance.az_a_csr_outside.id}"
    network_interface = "${aws_instance.az_a_csr_inside.network_interface_id}"
    vpc = true
}


/*
  Instances
*/
resource "aws_instance" "az_a_bastion" {
    ami = "${lookup(var.ami_bastion, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.bastion_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_SSH.id}"]
    subnet_id = "${aws_subnet.az_a_public.id}"
    associate_public_ip_address = true
	private_ip = "${var.az_a_bastion_e0}"
    source_dest_check = true
    tags {
        Name = "az_a_bastion"
    }
}

resource "aws_instance" "az_a_csr_inside" {
    ami = "${lookup(var.ami_csr1000v, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.csr1000v_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_SSH_IPSEC.id}"]
    subnet_id = "${aws_subnet.az_a_public.id}"
    associate_public_ip_address = true
	private_ip = "${var.az_a_csr_inside_e0}"
    source_dest_check = true
    tags {
        Name = "az_a_csr_inside"
    }
}

resource "aws_instance" "az_a_csr_outside" {
    ami = "${lookup(var.ami_csr1000v, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.csr1000v_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_SSH_IPSEC.id}"]
    subnet_id = "${aws_subnet.az_a_public.id}"
    associate_public_ip_address = true
	private_ip = "${var.az_a_csr_outside_e0}"
    source_dest_check = true
    tags {
        Name = "az_a_csr_outside"
    }
}

resource "aws_instance" "az_a_f5_inside" {
    ami = "${lookup(var.ami_f5, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.f5_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_All_Traffic.id}"]
    subnet_id = "${aws_subnet.az_a_management.id}"
    associate_public_ip_address = false
	private_ip = "${var.az_a_f5_inside_e0}"
    source_dest_check = true
    tags {
        Name = "az_a_f5_inside"
    }
}

resource "aws_instance" "az_a_f5_outside" {
    ami = "${lookup(var.ami_f5, var.aws_region)}"
    availability_zone = "${var.aws_az_a}"
    instance_type = "${var.f5_instance_type}"
    key_name = "${var.aws_key_name}"
    vpc_security_group_ids = ["${aws_security_group.SG_All_Traffic.id}"]
    subnet_id = "${aws_subnet.az_a_management.id}"
    associate_public_ip_address = false
	private_ip = "${var.az_a_f5_outside_e0}"
    source_dest_check = true
    tags {
        Name = "az_a_f5_outside"
    }
}


/*
  ENI az_a_bastion
*/
resource "aws_network_interface" "az_a_bastion_e1" {
	subnet_id = "${aws_subnet.az_a_management.id}"
	private_ips = ["${var.az_a_bastion_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = true
	attachment {
		instance = "${aws_instance.az_a_bastion.id}"
		device_index = 1
	}
}

/*
  ENI az_a_csr_inside
*/
resource "aws_network_interface" "az_a_csr_inside_e1" {
	subnet_id = "${aws_subnet.az_a_inside_csr_f5.id}"
	private_ips = ["${var.az_a_csr_inside_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_csr_inside.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "az_a_csr_inside_e2" {
	subnet_id = "${aws_subnet.az_a_management.id}"
	private_ips = ["${var.az_a_csr_inside_e2}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = true
	attachment {
		instance = "${aws_instance.az_a_csr_inside.id}"
		device_index = 2
	}
}

/*
  ENI az_a_csr_outside
*/
resource "aws_network_interface" "az_a_csr_outside_e1" {
	subnet_id = "${aws_subnet.az_a_outside_csr_f5.id}"
	private_ips = ["${var.az_a_csr_outside_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_csr_outside.id}"
		device_index = 2
	}
}

resource "aws_network_interface" "az_a_csr_outside_e2" {
	subnet_id = "${aws_subnet.az_a_management.id}"
	private_ips = ["${var.az_a_csr_outside_e2}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = true
	attachment {
		instance = "${aws_instance.az_a_csr_outside.id}"
		device_index = 1
	}
}

/*
  ENI az_a_f5_inside
*/
resource "aws_network_interface" "az_a_f5_inside_e1" {
	subnet_id = "${aws_subnet.az_a_inside_csr_f5.id}"
	private_ips = ["${var.az_a_f5_inside_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_f5_inside.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "az_a_f5_inside_e2" {
	subnet_id = "${aws_subnet.az_a_inside_f5_ftd.id}"
	private_ips = ["${var.az_a_f5_inside_e2}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_f5_inside.id}"
		device_index = 2
	}
}

/*
  ENI az_a_f5_outside
*/
resource "aws_network_interface" "az_a_f5_outside_e1" {
	subnet_id = "${aws_subnet.az_a_outside_csr_f5.id}"
	private_ips = ["${var.az_a_f5_outside_e1}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_f5_outside.id}"
		device_index = 1
	}
}

resource "aws_network_interface" "az_a_f5_outside_e2" {
	subnet_id = "${aws_subnet.az_a_outside_f5_asav.id}"
	private_ips = ["${var.az_a_f5_outside_e2}"]
	security_groups = ["${aws_security_group.SG_All_Traffic.id}"]
	source_dest_check = false
	attachment {
		instance = "${aws_instance.az_a_f5_outside.id}"
		device_index = 2
	}
}
