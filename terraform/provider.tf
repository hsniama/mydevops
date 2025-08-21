terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.85"
    }
  }
}


provider "azurerm" {
  features {}
  subscription_id = "835ac1b6-a568-4266-a5b1-f04f403bfe34"
}
