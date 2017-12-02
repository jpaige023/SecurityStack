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

variable "G1_static_private_ipA" {
    default = "router_a_address_g1"
}

variable "G2_static_private_ipA" {
    default = "router_a_address_g2"
}

