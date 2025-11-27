output "public_ip_address" {
  description = "Public IP address of the VM"
  value       = azurerm_public_ip.optibot.ip_address
}

output "vm_name" {
  description = "Name of the VM"
  value       = azurerm_linux_virtual_machine.optibot.name
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.optibot.name
}

output "ssh_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.optibot.ip_address}"
}

output "api_url" {
  description = "API URL"
  value       = "http://${azurerm_public_ip.optibot.ip_address}"
}

output "swagger_url" {
  description = "Swagger UI URL"
  value       = "http://${azurerm_public_ip.optibot.ip_address}/docs"
}
