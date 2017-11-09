output "default_vpc_id" {
  value = "${aws_vpc.default.id}"
}

output "region" {
  value = "${var.region}"
}

output "availability_zone" {
  value = "${var.availability_zone}"
}

output "cidr_block" {
  value = "${var.cidr_block}"
}

output "SG_SSH_IPSEC" {
  value = "${aws_security_group.SG_SSH_IPSEC.id}"
}

output "SG_SSH" {
  value = "${aws_security_group.SG_SSH.id}"
}

output "SG_All_Traffic" {
  value = "${aws_security_group.SG_All_Traffic.id}"
}

output "subnet_public" {
  value = "${aws_subnet.subnet_public.id}"
}

output "subnet_management" {
  value = "${aws_subnet.subnet_management.id}"
}

output "subnet_outside_csr_fw" {
  value = "${aws_subnet.subnet_outside_csr_fw.id}"
}

output "subnet_inside_csr_fw" {
  value = "${aws_subnet.subnet_inside_csr_fw.id}"
}

output "subnet_asav_ftd" {
  value = "${aws_subnet.subnet_asav_ftd.id}"
}
