variable "resource_group_name" {
  default = "DevOpsRG"
}

variable "location" {
  default = "EastUS"
}

variable "aks_name" {
  default = "devops-aks"
}

variable "acr_name" {
  default = "devopsregistryhenry"
}

variable "node_count" {
  default = 2
}
