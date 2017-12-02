resource "azurerm_public_ip" "PIP2" {
    name = "PIP2"
    location = "${var.azure_region}"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    public_ip_address_allocation = "static"

    tags {
        environment = "Production"
    }
}

resource "azurerm_subnet" "SubnetPublicB" {
    name = "SubnetPublicB"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    virtual_network_name = "${azurerm_virtual_network.VNVPC.name}"
    address_prefix = "${var.SubnetPublicB}"
    route_table_id = "${azurerm_route_table.RTPublic.id}"
}

resource "azurerm_subnet" "SubnetPrivateB" {
    name = "SubnetPrivateB"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    virtual_network_name = "${azurerm_virtual_network.VNVPC.name}"
    address_prefix = "${var.SubnetPrivateB}"
    route_table_id = "${azurerm_route_table.RTPrivate.id}"
}

resource "azurerm_subnet" "SubnetPrivateUsers2" {
    name = "SubnetPrivateUsers2"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    virtual_network_name = "${azurerm_virtual_network.VNVPC.name}"
    address_prefix = "${var.SubnetPrivateUsers2}"
    route_table_id = "${azurerm_route_table.RTPrivate.id}"
}

resource "azurerm_network_interface" "NICPublicB" {
    name = "NICPublicB"
    location = "${var.azure_region}"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    network_security_group_id = "${azurerm_network_security_group.SGInfrastructure.id}"
    enable_ip_forwarding = true

    ip_configuration {
        name = "NICPublicB"
        subnet_id = "${azurerm_subnet.SubnetPublicB.id}"
        private_ip_address_allocation = "static"
        private_ip_address = "${var.G1_static_private_ipB}"
        public_ip_address_id = "${azurerm_public_ip.PIP2.id}"
    }
}

resource "azurerm_network_interface" "NICPrivateB" {
    name = "NICPrivateB"
    location = "${var.azure_region}"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    network_security_group_id = "${azurerm_network_security_group.SGInfrastructureG2.id}"
    enable_ip_forwarding = true

    ip_configuration {
        name = "NICPrivateB"
        subnet_id = "${azurerm_subnet.SubnetPrivateB.id}"
        private_ip_address_allocation = "static"
        private_ip_address = "${var.G2_static_private_ipB}"
    }
}

resource "azurerm_virtual_machine" "CSR1000vB" {
    name = "CSR1000vB"
    location = "${var.azure_region}"
    resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
    plan {
        name = "16_6"
        product = "cisco-csr-1000v"
        publisher = "cisco"
    }
    availability_set_id = "${azurerm_availability_set.ASInfrastructure.id}"
    vm_size = "${var.CSR1000v_instance_type}"
    storage_image_reference {
        publisher = "cisco"
        offer = "cisco-csr-1000v"
        sku = "16_6"
        version = "latest"
    }
    storage_os_disk {
        name = "CSR1000vB-disk"
        vhd_uri = "${azurerm_storage_account.sainfrastructure1.primary_blob_endpoint}vhds/CSR1000vBdisk.vhd"
        caching = "ReadWrite"
        create_option = "FromImage"
    }
    delete_os_disk_on_termination = true
    os_profile {
        computer_name = "CSR1000vB"
        admin_username = "${var.default_user}"
        admin_password = "${var.default_password}"
    }
    os_profile_linux_config {
        disable_password_authentication = false
    }
    network_interface_ids = ["${azurerm_network_interface.NICPublicB.id}","${azurerm_network_interface.NICPrivateB.id}"]
       primary_network_interface_id = "${azurerm_network_interface.NICPublicB.id}"
       network_interface_ids = ["${azurerm_network_interface.NICPublicB.id}"]
    tags {
        environment = "Production"
    }
}

