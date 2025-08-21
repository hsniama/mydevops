output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_cluster_resource_group" {
  value = azurerm_kubernetes_cluster.aks.node_resource_group
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}
