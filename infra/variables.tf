variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
  default     = "e7699692-4fb7-46a7-93ae-e0fa12d22d4a"
}

variable "location" {
  description = "Azure region (p.ej. eastus, eastus2)"
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Nombre del Resource Group"
  type        = string
  default     = "rg-devops-henry"
}

variable "acr_name" {
  description = "Nombre del ACR (único global, 5-50 chars, solo minúsculas y números)"
  type        = string
  default     = "acrdevopshenry"
}

variable "aks_name" {
  description = "Nombre del AKS"
  type        = string
  default     = "aks-devops-henry"
}

variable "node_count" {
  description = "Cantidad de nodos del pool del AKS"
  type        = number
  default     = 2
}

variable "node_vm_size" {
  description = "Tamaño de VM para los nodos"
  type        = string
  default     = "Standard_B2s" # económico
}

variable "vnet_name" {
  description = "Nombre de la VNet"
  type        = string
  default     = "vnet-devops-henry"
}

variable "subnet_name" {
  description = "Nombre de la Subnet para AKS"
  type        = string
  default     = "snet-aks"
}

variable "vnet_cidr" {
  description = "CIDR de la VNet"
  type        = string
  default     = "10.100.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR de la Subnet"
  type        = string
  default     = "10.100.1.0/24"
}

variable "tags" {
  description = "Tags comunes"
  type        = map(string)
  default = {
    project = "devops-assessment"
    owner   = "henry"
    env     = "prod"
  }
}
