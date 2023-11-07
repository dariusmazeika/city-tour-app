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

locals {
  name            = replace(lower("${var.ENVIRONMENT}-${var.PROJECT_NAME}"), " ", "-")
  environment_url = element(split("/", var.ENVIRONMENT_URL), 2)
}

variable "max_body_size" {
  type    = string
  default = "16m"
}
