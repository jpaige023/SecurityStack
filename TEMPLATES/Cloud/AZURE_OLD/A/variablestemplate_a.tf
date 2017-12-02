variable "subscription_id" {}
variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}
variable "default_user" {}
variable "default_password" {}

variable "RG_NAME" {
	default = "rgXXX"
}

variable "CSR1000v_instance_type" {
        default = "cloud_instance_size"
}

variable "azure_region" {
    description = "Azure Region for the Resource Group"
    default = "cloud_provider_region_long"
}

variable "VPC_cidr" {
    description = "CIDR for the VPC"
    default = "cidr_block"
}

variable "SubnetPublic" {
    description = "CIDR for the Public Subnet"
    default = "router_a_subnet_g1"
}

variable "SubnetPrivate" {
    description = "CIDR for the Private Subnet"
    default = "router_a_subnet_g2"
}

variable "SubnetPublicB" {
    description = "CIDR for the Public SubnetB"
    default = "router_b_subnet_g1"
}

variable "SubnetPrivateB" {
    description = "CIDR for the Private SubnetB"
    default = "router_b_subnet_g2"
}

variable "SubnetPrivateUsers1" {
    description = "CIDR for the Private Subnet Users1"
    default = "users_subnet_a"
}

variable "SubnetPrivateUsers2" {
    description = "CIDR for the Private Subnet Users2"
    default = "users_subnet_b"
}

variable "G1_static_private_ipA" {
    default = "router_a_address_g1"
}

variable "G2_static_private_ipA" {
    default = "router_a_address_g2"
}

variable "G1_static_private_ipB" {
    default = "router_b_address_g1"
}

variable "G2_static_private_ipB" {
    default = "router_b_address_g2"
}
