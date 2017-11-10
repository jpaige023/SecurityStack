resource "aws_vpc" "default" {
  cidr_block           = "${var.vpc_cidr}"
  enable_dns_hostnames = true

  tags {
    Name = "${var.vpc_NAME}"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

/*
  Public Subnet
*/
resource "aws_subnet" "high_availability_zone-public" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.public_subnetA_cidr}"
  availability_zone = "high_availability_zone"

  tags {
    Name = "Public SubnetA"
  }
}

resource "aws_route_table" "cloud_provider_region-public" {
  vpc_id = "${aws_vpc.default.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.default.id}"
  }

  tags {
    Name = "Public Subnets"
  }
}

resource "aws_route_table_association" "high_availability_zone-public" {
  subnet_id      = "${aws_subnet.high_availability_zone-public.id}"
  route_table_id = "${aws_route_table.cloud_provider_region-public.id}"
}

/*
  Private Subnet
*/
resource "aws_subnet" "high_availability_zone-private" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.private_subnetA_cidr}"
  availability_zone = "high_availability_zone"

  tags {
    Name = "Private SubnetA"
  }
}

resource "aws_subnet" "high_availability_zone-private_users" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.private_subnetA_cidr_users}"
  availability_zone = "high_availability_zone"

  tags {
    Name = "Private SubnetA_users"
  }
}

resource "aws_route_table" "cloud_provider_region-private" {
  vpc_id = "${aws_vpc.default.id}"

  route {
    cidr_block           = "0.0.0.0/0"
    network_interface_id = "${aws_network_interface.G2A.id}"
  }

  tags {
    Name = "Private Subnets"
  }
}

resource "aws_route_table_association" "high_availability_zone-private" {
  subnet_id      = "${aws_subnet.high_availability_zone-private.id}"
  route_table_id = "${aws_route_table.cloud_provider_region-private.id}"
}

resource "aws_route_table_association" "high_availability_zone-private_users" {
  subnet_id      = "${aws_subnet.high_availability_zone-private_users.id}"
  route_table_id = "${aws_route_table.cloud_provider_region-private.id}"
}

/*
  CSR1000v Instance
*/
resource "aws_security_group" "SG_G1_CSR1000v" {
  name        = "SG_G1_CSR1000v"
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
    cidr_blocks = ["${var.vpc_cidr}"]
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

resource "aws_security_group" "SG_G2_CSR1000v" {
  name        = "SG_G2_CSR1000v"
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
  ami                         = "image_id"
  availability_zone           = "high_availability_zone"
  instance_type               = "${var.CSR1000v_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${aws_security_group.SG_G1_CSR1000v.id}"]
  subnet_id                   = "${aws_subnet.high_availability_zone-public.id}"
  associate_public_ip_address = true
  private_ip                  = "${var.G1_static_private_ipA}"
  source_dest_check           = false
  iam_instance_profile        = "${var.IAM_Role}"

  tags {
    Name = "${var.G1_static_private_ipA}"
  }
}

resource "aws_eip" "CSR1000vA" {
  network_interface = "${aws_instance.CSR1000vA.network_interface_id}"
  vpc               = true
}

resource "aws_network_interface" "G2A" {
  subnet_id         = "${aws_subnet.high_availability_zone-private.id}"
  private_ips       = ["${var.G2_static_private_ipA}"]
  security_groups   = ["${aws_security_group.SG_G2_CSR1000v.id}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.CSR1000vA.id}"
    device_index = 1
  }
}
