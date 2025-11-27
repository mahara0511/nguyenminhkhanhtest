terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "optibot" {
  name     = var.resource_group_name
  location = var.location
  
  tags = {
    Environment = var.environment
    Project     = "Optibot"
  }
}

# Virtual Network
resource "azurerm_virtual_network" "optibot" {
  name                = "${var.prefix}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.optibot.location
  resource_group_name = azurerm_resource_group.optibot.name
  
  tags = {
    Environment = var.environment
  }
}

# Subnet
resource "azurerm_subnet" "optibot" {
  name                 = "${var.prefix}-subnet"
  resource_group_name  = azurerm_resource_group.optibot.name
  virtual_network_name = azurerm_virtual_network.optibot.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Public IP
resource "azurerm_public_ip" "optibot" {
  name                = "${var.prefix}-public-ip"
  location            = azurerm_resource_group.optibot.location
  resource_group_name = azurerm_resource_group.optibot.name
  allocation_method   = "Static"
  sku                 = "Standard"
  
  tags = {
    Environment = var.environment
  }
}

# Network Security Group
resource "azurerm_network_security_group" "optibot" {
  name                = "${var.prefix}-nsg"
  location            = azurerm_resource_group.optibot.location
  resource_group_name = azurerm_resource_group.optibot.name

  # SSH access
  security_rule {
    name                       = "SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # HTTP access (port 80)
  security_rule {
    name                       = "HTTP"
    priority                   = 200
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Environment = var.environment
  }
}

# Network Interface
resource "azurerm_network_interface" "optibot" {
  name                = "${var.prefix}-nic"
  location            = azurerm_resource_group.optibot.location
  resource_group_name = azurerm_resource_group.optibot.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.optibot.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.optibot.id
  }
  
  tags = {
    Environment = var.environment
  }
}

# Associate NSG with NIC
resource "azurerm_network_interface_security_group_association" "optibot" {
  network_interface_id      = azurerm_network_interface.optibot.id
  network_security_group_id = azurerm_network_security_group.optibot.id
}

# Virtual Machine
resource "azurerm_linux_virtual_machine" "optibot" {
  name                = "${var.prefix}-vm"
  resource_group_name = azurerm_resource_group.optibot.name
  location            = azurerm_resource_group.optibot.location
  size                = var.vm_size
  admin_username      = var.admin_username
  
  network_interface_ids = [
    azurerm_network_interface.optibot.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file(var.ssh_public_key_path)
  }

  os_disk {
    name                 = "${var.prefix}-osdisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  # Cloud-init script to install Docker and setup environment
  custom_data = base64encode(templatefile("${path.module}/cloud-init.yml", {
    gemini_api_key     = var.gemini_api_key
    github_token       = var.github_token
    github_username    = var.github_username
    docker_image       = var.docker_image
  }))

  tags = {
    Environment = var.environment
  }
}
