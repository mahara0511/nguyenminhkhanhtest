variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "optibot-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "Japan East"
}

variable "prefix" {
  description = "Prefix for resource names"
  type        = string
  default     = "optibot"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "vm_size" {
  description = "Size of the Azure VM"
  type        = string
  default     = "Standard_B1s"  # 2 vCPU, 4GB RAM
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key for VM access"
  type        = string
  default     = "~/.ssh/id_rsa_azure.pub"
}

variable "gemini_api_key" {
  description = "Gemini API Key for the application"
  type        = string
  sensitive   = true
}

variable "github_token" {
  description = "GitHub token for GHCR access"
  type        = string
  sensitive   = true
}

variable "github_username" {
  description = "GitHub username for GHCR"
  type        = string
}

variable "docker_image" {
  description = "Docker image to deploy"
  type        = string
  default     = "ghcr.io/mahara0511/nguyenminhkhanhtest:latest"
}
