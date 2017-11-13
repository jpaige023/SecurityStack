resource "aws_vpc" "default" {
  cidr_block           = "${var.cidr_block}"
  enable_dns_hostnames = true

  tags {
    Name = "${var.vpc_number}"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

/*
  Public Subnet
*/
resource "aws_subnet" "router_a_subnet_g1" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.router_a_subnet_g1}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "Public SubnetA"
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

resource "aws_route_table_association" "router_a_subnet_g1c" {
  subnet_id      = "${aws_subnet.router_a_subnet_g1.id}"
  route_table_id = "${aws_route_table.public.id}"
}

/*
  Private Subnet
*/
resource "aws_subnet" "router_a_subnet_g2" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.router_a_subnet_g2}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "Private SubnetA"
  }
}

resource "aws_subnet" "users_subnet_a" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.users_subnet_a}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "${var.users_subnet_a}"
  }
}

resource "aws_route_table" "rt_private" {
  vpc_id = "${aws_vpc.default.id}"

  route {
    cidr_block           = "0.0.0.0/0"
    network_interface_id = "${aws_network_interface.G2A.id}"
  }

  tags {
    Name = "Private Subnets"
  }
}

resource "aws_route_table_association" "router_a_subnet_g2" {
  subnet_id      = "${aws_subnet.router_a_subnet_g2.id}"
  route_table_id = "${aws_route_table.rt_private.id}"
}

resource "aws_route_table_association" "users_subnet_a" {
  subnet_id      = "${aws_subnet.users_subnet_a.id}"
  route_table_id = "${aws_route_table.rt_private.id}"
}

/*
  CSR1000v Instance
*/
resource "aws_security_group" "SG_SSH_IPSEC" {
  name        = "SG_SSH_IPSECv"
  description = "Allow Traffic into the CSR1000v"

  ingress {
    from_port   = 4500
    to_port     = 4500
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "50"
    cidr_blocks = ["${var.cidr_block}"]
  }

  ingress {
    from_port   = 500
    to_port     = 500
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${aws_vpc.default.id}"

  tags {
    Name = "SG_G1_CSR1000v"
  }
}

resource "aws_security_group" "SG_All_Traffic" {
  name        = "SG_All_Traffic"
  description = "Allow Traffic into the G2 CSR1000v"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = "${aws_vpc.default.id}"

  tags {
    Name = "SG_G2_CSR1000v"
  }
}

resource "aws_instance" "CSR1000vA" {
  ami                         = "${lookup(var.ami_csr1000v, var.region)}"
  availability_zone           = "${var.availability_zone}"
  instance_type               = "${var.csr1000v_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${aws_security_group.SG_SSH_IPSEC.id}"]
  subnet_id                   = "${aws_subnet.router_a_subnet_g1.id}"
  associate_public_ip_address = true
  private_ip                  = "${var.router_a_address_g1}"
  source_dest_check           = false
  iam_instance_profile        = "${var.IAM_Role}"

  tags {
    Name         = "${var.router_a_address_g1}"
    DMVPN_Role   = "${var.dmvpn_role}"
    DMVPN_Tunnel = "${var.dmvpn_tunnel}"
  }
}

resource "aws_eip" "CSR1000vA" {
  network_interface = "${aws_instance.CSR1000vA.network_interface_id}"
  vpc               = true
}

resource "aws_network_interface" "G2A" {
  subnet_id         = "${aws_subnet.router_a_subnet_g2.id}"
  private_ips       = ["${var.router_a_address_g2}"]
  security_groups   = ["${aws_security_group.SG_All_Traffic.id}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.CSR1000vA.id}"
    device_index = 1
  }
}
