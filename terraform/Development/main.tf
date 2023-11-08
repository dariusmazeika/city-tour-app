terraform {
  backend "http" {
  }
}

variable "PROJECT_NAME" {
  type = string
}

variable "KUBE_NAMESPACE" {
  type = string
}

variable "ENVIRONMENT_SLUG" {
  type = string
}

variable "ENVIRONMENT_URL" {
  type = string
}

variable "PROJECT_PATH_SLUG" {
  type = string
}

variable "ENVIRONMENT" {
  type = string
}

variable "REGISTRY_IMAGE" {
  type = string
}

variable "CI_COMMIT_SHORT_SHA" {
  type = string
}

module "development" {
  source = "./django"

  PROJECT_NAME        = var.PROJECT_NAME
  KUBE_NAMESPACE      = var.KUBE_NAMESPACE
  ENVIRONMENT_SLUG    = var.ENVIRONMENT_SLUG
  ENVIRONMENT_URL     = var.ENVIRONMENT_URL
  PROJECT_PATH_SLUG   = var.PROJECT_PATH_SLUG
  ENVIRONMENT         = var.ENVIRONMENT
  REGISTRY_IMAGE      = var.REGISTRY_IMAGE
  CI_COMMIT_SHORT_SHA = var.CI_COMMIT_SHORT_SHA

  depends_on = [
    module.dependencies
  ]
}

module "dependencies" {
  source = "./dependencies"

  PROJECT_NAME      = var.PROJECT_NAME
  KUBE_NAMESPACE    = var.KUBE_NAMESPACE
  ENVIRONMENT_SLUG  = var.ENVIRONMENT_SLUG
  ENVIRONMENT_URL   = var.ENVIRONMENT_URL
  PROJECT_PATH_SLUG = var.PROJECT_PATH_SLUG
  ENVIRONMENT       = var.ENVIRONMENT

  db_version = "postgis/postgis:14-3.4-alpine"
}

output "KUBERNETES_DEPLOYMENT" {
  value = module.development.KUBERNETES_DEPLOYMENT
}
