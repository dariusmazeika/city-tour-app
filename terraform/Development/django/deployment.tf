resource "kubernetes_deployment" "web_application" {
  metadata {
    annotations = {
      "app.gitlab.com/app" = var.PROJECT_PATH_SLUG
      "app.gitlab.com/env" = var.ENVIRONMENT_SLUG
    }
    name      = local.name
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    replicas = "1"

    selector {
      match_labels = {
        "app" = var.PROJECT_NAME
      }
    }

    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = "100%"
        max_unavailable = "25%"
      }
    }

    template {
      metadata {
        annotations = {
          "app.gitlab.com/app" = var.PROJECT_PATH_SLUG
          "app.gitlab.com/env" = var.ENVIRONMENT_SLUG
        }
        labels = {
          "app" = var.PROJECT_NAME
        }
      }

      spec {
        affinity {
          node_affinity {
            preferred_during_scheduling_ignored_during_execution {
              weight = 1
              preference {
                match_expressions {
                  key      = "eks.amazonaws.com/capacityType"
                  operator = "In"
                  values   = ["SPOT"]
                }
              }
            }
          }
        }
        toleration {
          key   = "no-pvc"
          value = "true"
        }
        image_pull_secrets {
          name = "regcred"
        }
        image_pull_secrets {
          name = "regcred-default"
        }

        container {
          name  = "application"
          image = "${var.REGISTRY_IMAGE}:${var.CI_COMMIT_SHORT_SHA}"
          port {
            container_port = 8000
            protocol       = "TCP"
          }
          env {
            name  = "RUN_MODE"
            value = "GUNICORN"
          }
          env_from {
            config_map_ref {
              name     = "values"
              optional = false
            }
          }
          env_from {
            secret_ref {
              name     = "app-secrets"
              optional = true
            }
          }

          readiness_probe {
            failure_threshold     = 30
            initial_delay_seconds = 0
            period_seconds        = 10
            success_threshold     = 1
            timeout_seconds       = 5

            http_get {
              path   = "/health/"
              port   = "8000"
              scheme = "HTTP"
            }
          }

          resources {
            limits = {
              memory = "1024Mi"
            }
            requests = {
              memory = "768Mi"
            }

          }
          volume_mount {
            mount_path = "/app/static"
            name       = "static-files"
          }
        }
        container {
          image             = "nginx:alpine"
          image_pull_policy = "IfNotPresent"
          name              = "media"


          port {
            container_port = 80
            protocol       = "TCP"
          }
          volume_mount {
            mount_path = "/usr/share/nginx/html/static"
            name       = "static-files"
          }

        }
        volume {
          name = "static-files"
          empty_dir {}
        }
      }
    }
  }
  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].container[0].image
    ]
  }
  depends_on = [
    kubernetes_deployment.celery
  ]
}

resource "kubernetes_deployment" "celery" {
  metadata {
    name      = "${local.name}-celery"
    namespace = var.KUBE_NAMESPACE
  }
  spec {
    replicas = "1"
    selector {
      match_labels = {
        "celery" = var.PROJECT_NAME
      }
    }
    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = "100%"
        max_unavailable = "25%"
      }
    }

    template {
      metadata {
        labels = {
          "celery" = var.PROJECT_NAME
        }
      }
      spec {
        affinity {
          node_affinity {
            preferred_during_scheduling_ignored_during_execution {
              weight = 1
              preference {
                match_expressions {
                  key      = "eks.amazonaws.com/capacityType"
                  operator = "In"
                  values   = ["SPOT"]
                }
              }
            }
          }
        }
        toleration {
          key   = "no-pvc"
          value = "true"
        }
        image_pull_secrets {
          name = "regcred"
        }
        image_pull_secrets {
          name = "regcred-default"
        }

        container {
          name  = "celery"
          image = "${var.REGISTRY_IMAGE}:${var.CI_COMMIT_SHORT_SHA}"

          env {
            name  = "RUN_MODE"
            value = "CELERY_WORKER"
          }

          env_from {
            config_map_ref {
              name     = "values"
              optional = false
            }
          }
          env_from {
            secret_ref {
              name     = "app-secrets"
              optional = true
            }
          }

          resources {
            limits = {
              memory = "1024Mi"
            }
            requests = {
              memory = "768Mi"
            }
          }
        }
      }
    }
  }
  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].container[0].image
    ]
  }
}

resource "kubernetes_deployment" "celery-beat" {
  metadata {
    name      = "${local.name}-celery-beat"
    namespace = var.KUBE_NAMESPACE
  }
  spec {
    replicas = "1"
    selector {
      match_labels = {
        "celery-beat" = var.PROJECT_NAME
      }
    }
    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = "25%"
        max_unavailable = "25%"
      }
    }

    template {
      metadata {
        labels = {
          "celery-beat" = var.PROJECT_NAME
        }
      }
      spec {
        affinity {
          node_affinity {
            preferred_during_scheduling_ignored_during_execution {
              weight = 1
              preference {
                match_expressions {
                  key      = "eks.amazonaws.com/capacityType"
                  operator = "In"
                  values   = ["SPOT"]
                }
              }
            }
          }
        }
        toleration {
          key   = "no-pvc"
          value = "true"
        }
        image_pull_secrets {
          name = "regcred"
        }
        image_pull_secrets {
          name = "regcred-default"
        }

        container {
          name  = "celery-beat"
          image = "${var.REGISTRY_IMAGE}:${var.CI_COMMIT_SHORT_SHA}"

          env {
            name  = "RUN_MODE"
            value = "CELERY_BEAT"
          }

          env_from {
            config_map_ref {
              name     = "values"
              optional = false
            }
          }
          env_from {
            secret_ref {
              name     = "app-secrets"
              optional = true
            }
          }

          resources {
            limits = {
              memory = "1024Mi"
            }
            requests = {
              memory = "768Mi"
            }
          }
        }
      }
    }
  }
  lifecycle {
    ignore_changes = [
      spec[0].template[0].spec[0].container[0].image
    ]
  }
}

resource "kubernetes_deployment" "redis" {
  metadata {
    name      = "${local.name}-redis"
    namespace = var.KUBE_NAMESPACE
  }
  spec {
    replicas = "1"
    selector {
      match_labels = {
        "redis" = var.PROJECT_NAME
      }
    }
    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = "25%"
        max_unavailable = "25%"
      }
    }

    template {
      metadata {
        labels = {
          "redis" = var.PROJECT_NAME
        }
      }
      spec {
        affinity {
          node_affinity {
            preferred_during_scheduling_ignored_during_execution {
              weight = 1
              preference {
                match_expressions {
                  key      = "eks.amazonaws.com/capacityType"
                  operator = "In"
                  values   = ["ON_DEMAND"]
                }
              }
            }
          }
        }
        toleration {
          key   = "databases"
          value = "true"
        }
        container {
          name  = "redis"
          image = "redis:6-alpine"

          port {
            container_port = 6379
            protocol       = "TCP"
          }
        }
      }
    }
  }
}
