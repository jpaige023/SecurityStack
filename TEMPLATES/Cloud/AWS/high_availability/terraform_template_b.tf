/*
  Public Subnet
*/
resource "aws_subnet" "high_availability_zone_ha-public" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.router_b_subnet_g1}"
  availability_zone = "${var.availability_zone_ha}"

  tags {
    Name = "Public SubnetB"
  }
}

resource "aws_route_table_association" "high_availability_zone_ha-public" {
  subnet_id      = "${aws_subnet.high_availability_zone_ha-public.id}"
  route_table_id = "${aws_route_table.cloud_provider_region-public.id}"
}

/*
  Private Subnet
*/
resource "aws_subnet" "high_availability_zone_ha-private" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.router_b_subnet_g2}"
  availability_zone = "${var.availability_zone_ha}"

  tags {
    Name = "Private SubnetB"
  }
}

resource "aws_subnet" "high_availability_zone_ha-private_users" {
  vpc_id = "${aws_vpc.default.id}"

  cidr_block        = "${var.users_subnet_b}"
  availability_zone = "${var.availability_zone_ha}"

  tags {
    Name = "Private SubnetB_users"
  }
}

resource "aws_route_table_association" "high_availability_zone_ha-private" {
  subnet_id      = "${aws_subnet.high_availability_zone_ha-private.id}"
  route_table_id = "${aws_route_table.cloud_provider_region-private.id}"
}

resource "aws_route_table_association" "high_availability_zone_ha-private_users" {
  subnet_id      = "${aws_subnet.high_availability_zone_ha-private_users.id}"
  route_table_id = "${aws_route_table.cloud_provider_region-private.id}"
}

/*
  CSR1000v Instance
*/

resource "aws_instance" "CSR1000vB" {
  ami                         = "${lookup(var.ami_csr1000v, var.region)}"
  availability_zone           = "${var.availability_zone_ha}"
  instance_type               = "${var.csr1000v_instance_type}"
  key_name                    = "${var.aws_key_name}"
  vpc_security_group_ids      = ["${aws_security_group.SG_G1_CSR1000v.id}"]
  subnet_id                   = "${aws_subnet.high_availability_zone_ha-public.id}"
  associate_public_ip_address = true
  private_ip                  = "${var.router_b_address_g1}"
  source_dest_check           = false
  iam_instance_profile        = "${var.IAM_Role}"

  tags {
    Name = "${var.router_b_address_g1}"
  }
}

resource "aws_eip" "CSR1000vB" {
  network_interface = "${aws_instance.CSR1000vB.network_interface_id}"
  vpc               = true
}

resource "aws_network_interface" "G2B" {
  subnet_id         = "${aws_subnet.high_availability_zone_ha-private.id}"
  private_ips       = ["${var.router_b_address_g2}"]
  security_groups   = ["${aws_security_group.SG_G2_CSR1000v.id}"]
  source_dest_check = false

  attachment {
    instance     = "${aws_instance.CSR1000vB.id}"
    device_index = 1
  }
}
