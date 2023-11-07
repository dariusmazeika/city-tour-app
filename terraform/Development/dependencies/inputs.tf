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

locals {
  name            = replace(lower("${var.ENVIRONMENT}-${var.PROJECT_NAME}"), " ", "-")
  environment_url = element(split("/", var.ENVIRONMENT_URL), 2)
  selector        = "${var.PROJECT_NAME}-dependencies"
}

variable "db_version" {
  type    = string
  default = "postgres:14"
}

variable "minio_storage" {
  type    = string
  default = "6Gi"
}
