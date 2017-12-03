resource "azurerm_resource_group" "RGInfrastructure" {
  name     = "${var.vpc_number}"
  location = "${var.region}"
}

resource "azurerm_storage_account" "sainfrastructure1" {
  name                     = "${var.vpc_number}randomnumber958"
  resource_group_name      = "${azurerm_resource_group.RGInfrastructure.name}"
  location                 = "${var.region}"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags {
    environment = "Production"
  }
}

resource "azurerm_network_security_group" "SGInfrastructure" {
  name                = "${var.vpc_number}"
  location            = "${var.region}"
  resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"

  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowUDP500"
    priority                   = 101
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Udp"
    source_port_range          = "*"
    destination_port_range     = "500"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowUDP4500"
    priority                   = 102
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Udp"
    source_port_range          = "*"
    destination_port_range     = "4500"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  tags {
    environment = "Production"
  }
}

resource "azurerm_network_security_group" "SGInfrastructureG2" {
  name                = "${var.vpc_number}G2"
  location            = "${var.region}"
  resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"

  security_rule {
    name                       = "AllowAll"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

resource "azurerm_virtual_network" "VNVPC" {
  name                = "${var.vpc_number}"
  resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"
  address_space       = ["${var.cidr_block}"]
  location            = "${var.region}"
  dns_servers         = ["208.67.222.222", "8.8.8.8"]

  tags {
    environment = "Production"
  }
}

resource "azurerm_route_table" "RTPublic" {
  name                = "RTPublic"
  location            = "${var.region}"
  resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"

  route {
    name           = "DefaultInternet"
    address_prefix = "0.0.0.0/0"
    next_hop_type  = "Internet"
  }

  tags {
    environment = "Production"
  }
}

resource "azurerm_route_table" "RTPrivate" {
  name                = "RTPrivate"
  location            = "${var.region}"
  resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"

  route {
    name                   = "DefaulttoRouter"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = "${var.router_a_subnet_g2}"
  }

  tags {
    environment = "Production"
  }
}

resource "azurerm_subnet" "SubnetPublic" {
  name                 = "SubnetPublic"
  resource_group_name  = "${azurerm_resource_group.RGInfrastructure.name}"
  virtual_network_name = "${azurerm_virtual_network.VNVPC.name}"
  address_prefix       = "${var.router_a_subnet_g1}"
  route_table_id       = "${azurerm_route_table.RTPublic.id}"
}

resource "azurerm_subnet" "SubnetPrivate" {
  name                 = "SubnetPrivate"
  resource_group_name  = "${azurerm_resource_group.RGInfrastructure.name}"
  virtual_network_name = "${azurerm_virtual_network.VNVPC.name}"
  address_prefix       = "${var.router_a_subnet_g2}"
  route_table_id       = "${azurerm_route_table.RTPrivate.id}"
}

resource "azurerm_public_ip" "PIP1" {
  name                         = "PIP1"
  location                     = "${var.region}"
  resource_group_name          = "${azurerm_resource_group.RGInfrastructure.name}"
  public_ip_address_allocation = "static"

  tags {
    environment = "Production"
  }
}

resource "azurerm_network_interface" "NICPublic" {
  name                      = "NICPublic"
  location                  = "${var.region}"
  resource_group_name       = "${azurerm_resource_group.RGInfrastructure.name}"
  network_security_group_id = "${azurerm_network_security_group.SGInfrastructure.id}"
  enable_ip_forwarding      = true

  ip_configuration {
    name                          = "NICPublic"
    subnet_id                     = "${azurerm_subnet.SubnetPublic.id}"
    private_ip_address_allocation = "static"
    private_ip_address            = "${var.router_a_address_g1}"
    public_ip_address_id          = "${azurerm_public_ip.PIP1.id}"
  }
}

resource "azurerm_network_interface" "NICPrivate" {
  name                      = "NICPrivate"
  location                  = "${var.region}"
  resource_group_name       = "${azurerm_resource_group.RGInfrastructure.name}"
  network_security_group_id = "${azurerm_network_security_group.SGInfrastructureG2.id}"
  enable_ip_forwarding      = true

  ip_configuration {
    name                          = "NICPrivate"
    subnet_id                     = "${azurerm_subnet.SubnetPrivate.id}"
    private_ip_address_allocation = "static"
    private_ip_address            = "${var.router_a_address_g2}"
  }
}

resource "azurerm_virtual_machine" "CSR1000vA" {
  name                = "CSR1000vA"
  location            = "${var.region}"
  resource_group_name = "${azurerm_resource_group.RGInfrastructure.name}"

  plan {
    name      = "16_6"
    product   = "cisco-csr-1000v"
    publisher = "cisco"
  }

  vm_size = "${var.CSR1000v_instance_type}"

  storage_image_reference {
    publisher = "cisco"
    offer     = "cisco-csr-1000v"
    sku       = "16_6"
    version   = "latest"
  }

  storage_os_disk {
    name          = "CSR1000vA-disk"
    vhd_uri       = "${azurerm_storage_account.sainfrastructure1.primary_blob_endpoint}vhds/CSR1000vAdisk.vhd"
    caching       = "ReadWrite"
    create_option = "FromImage"
  }

  delete_os_disk_on_termination = true

  os_profile {
    computer_name  = "CSR1000vA"
    admin_username = "${var.default_user}"
    admin_password = "${var.default_password}"
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  network_interface_ids        = ["${azurerm_network_interface.NICPublic.id}", "${azurerm_network_interface.NICPrivate.id}"]
  primary_network_interface_id = "${azurerm_network_interface.NICPublic.id}"

  tags {
    environment = "Production"
  }
}
