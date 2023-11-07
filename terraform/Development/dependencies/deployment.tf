resource "kubernetes_deployment" "dependencies" {
  metadata {
    name      = "dependencies"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    replicas = "1"

    selector {
      match_labels = {
        "app" = local.selector
      }
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "app" = local.selector
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
          args = [
            "-c",
            "minio server /data",
          ]
          command = [
            "/bin/sh",
          ]
          image             = "minio/minio:RELEASE.2022-10-24T18-35-07Z"
          image_pull_policy = "Always"
          name              = "minio"

          port {
            container_port = 9000

            protocol = "TCP"
          }
          env {
            name  = "MINIO_API_CORS_ALLOW_ORIGIN"
            value = "*"
          }
          env {
            name  = "MINIO_BROWSER"
            value = "off"
          }
          env {
            name  = "MINIO_ROOT_USER"
            value = "EDRTXJEZ0X6EMKE1BBWA"
          }
          env {
            name  = "MINIO_ROOT_PASSWORD"
            value = "qxhPwheeKulTs/FJikLSH/czIOQnUcLeQyjRcNCi"
          }
          env {
            name  = "MINIO_SITE_NAME"
            value = "media-django-rest-framework"
          }
          env {
            name  = "MINIO_SITE_REGION"
            value = "eu-central-1"
          }

          readiness_probe {
            failure_threshold     = 30
            initial_delay_seconds = 0
            period_seconds        = 10
            success_threshold     = 1
            timeout_seconds       = 5

            http_get {
              path   = "/minio/health/live"
              port   = "9000"
              scheme = "HTTP"
            }
          }
          volume_mount {
            mount_path = "/data"
            name       = "media-files"
            read_only  = false
          }
        }

        container {
          image             = var.db_version
          image_pull_policy = "Always"
          name              = "postgresql"

          env {
            name  = "POSTGRES_USER"
            value = "psql"
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = "django"
          }
          env {
            name  = "POSTGRES_DB"
            value = "django"
          }
          env {
            name  = "PGDATA"
            value = "/var/lib/postgresql/data/pg_data"
          }

          port {
            container_port = 5432

            protocol = "TCP"
          }
          volume_mount {
            mount_path = "/var/lib/postgresql/data"
            name       = "database-storage"
          }
        }

        init_container {
          args = [
            "-c",
            "[ -d /data/media-${var.PROJECT_NAME} ] || mkdir /data/media-${var.PROJECT_NAME}",
          ]
          command = [
            "/bin/sh",
          ]
          image             = "busybox:latest"
          image_pull_policy = "Always"
          name              = "init-minio"

          volume_mount {
            mount_path = "/data"
            name       = "media-files"
            read_only  = false
          }
        }
        volume {
          name = "database-storage"

          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.database.metadata[0].name
          }
        }
        volume {
          name = "media-files"

          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.media.metadata[0].name
          }
        }
      }
    }
  }
}
