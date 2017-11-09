resource "aws_vpc" "default" {
  cidr_block           = "${var.cidr_block}"
  enable_dns_hostnames = true

  tags {
    Name = "${var.region}security_stack"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.default.id}"
}

/*
  Public Subnet
*/
resource "aws_subnet" "subnet_public" {
  vpc_id            = "${aws_vpc.default.id}"
  cidr_block        = "${var.subnet_public}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "subnet_public"
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

resource "aws_route_table_association" "public_rt_public" {
  subnet_id      = "${aws_subnet.subnet_public.id}"
  route_table_id = "${aws_route_table.public.id}"
}

/*
  Management Subnet
*/
resource "aws_subnet" "subnet_management" {
  vpc_id            = "${aws_vpc.default.id}"
  cidr_block        = "${var.cidr_block}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "subnet_management"
  }
}

resource "aws_route_table" "management" {
  vpc_id = "${aws_vpc.default.id}"

  tags {
    Name = "Management Subnet"
  }
}

resource "aws_route_table_association" "private_rt_management" {
  subnet_id      = "${aws_subnet.subnet_management.id}"
  route_table_id = "${aws_route_table.management.id}"
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

resource "aws_subnet" "subnet_asav_ftd" {
  vpc_id            = "${aws_vpc.default.id}"
  cidr_block        = "${var.subnet_asav_ftd}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "asav_ftd"
  }
}

resource "aws_route_table_association" "private_rt_az_a_asav_ftd" {
  subnet_id      = "${aws_subnet.subnet_asav_ftd.id}"
  route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "subnet_inside_csr_fw" {
  vpc_id            = "${aws_vpc.default.id}"
  cidr_block        = "${var.subnet_inside_csr_fw}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "subnet_inside_csr_fw"
  }
}

resource "aws_route_table_association" "private_rt_subnet_inside_csr_fw" {
  subnet_id      = "${aws_subnet.subnet_inside_csr_fw.id}"
  route_table_id = "${aws_route_table.private.id}"
}

resource "aws_subnet" "subnet_outside_csr_fw" {
  vpc_id            = "${aws_vpc.default.id}"
  cidr_block        = "${var.subnet_outside_csr_fw}"
  availability_zone = "${var.availability_zone}"

  tags {
    Name = "subnet_outside_csr_fw"
  }
}

resource "aws_route_table_association" "private_rt_subnet_outside_csr_fw" {
  subnet_id      = "${aws_subnet.subnet_outside_csr_fw.id}"
  route_table_id = "${aws_route_table.private.id}"
}

/*
  Security Groups - SG_SSH_IPSEC, SG_SSH, SG_All_Traffic
*/
resource "aws_security_group" "SG_SSH_IPSEC" {
  name        = "SG_SSH_IPSEC"
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
    Name = "SG_SSH_IPSEC"
  }
}

resource "aws_security_group" "SG_SSH" {
  name        = "SG_SSH"
  description = "Only SSH incoming"

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
    Name = "SG_SSH"
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
    Name = "SG_All_Traffic"
  }
}
