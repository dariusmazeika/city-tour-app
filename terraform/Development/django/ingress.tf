resource "kubernetes_ingress_v1" "minio" {
  metadata {
    annotations = {
      "cert-manager.io/cluster-issuer"              = "letsencrypt-prod"
      "enable-vts-status"                           = "true"
      "prometheus.io/port"                          = "10254"
      "prometheus.io/scrape"                        = "true"
      "nginx.ingress.kubernetes.io/proxy-body-size" = var.max_body_size
      "ingress.kubernetes.io/force-ssl-redirect"    = "true"
      "kubernetes.io/ingress.class"                 = "nginx"
    }
    name      = local.name
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    rule {
      host = local.environment_url
      http {
        path {
          backend {
            service {
              name = "backend"
              port {
                number = 8000
              }
            }
          }
          path = "/"
        }
        path {
          backend {
            service {
              name = "media"
              port {
                number = 80
              }
            }
          }
          path = "/static/"
        }
      }
    }
    tls {
      hosts       = [local.environment_url]
      secret_name = local.environment_url
    }
  }
}
