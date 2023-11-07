resource "kubernetes_ingress_v1" "example_ingress" {
  metadata {
    annotations = {
      "cert-manager.io/cluster-issuer"              = "letsencrypt-prod"
      "enable-vts-status"                           = "true"
      "prometheus.io/port"                          = "10254"
      "prometheus.io/scrape"                        = "true"
      "nginx.ingress.kubernetes.io/proxy-body-size" = "8m"
      "ingress.kubernetes.io/force-ssl-redirect"    = "true"
      "kubernetes.io/ingress.class"                 = "nginx"
    }
    name      = "${local.name}-minio"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    rule {
      host = "minio.${local.environment_url}"
      http {
        path {
          backend {
            service {
              name = "minio"
              port {
                number = 9000
              }
            }
          }

          path = "/"
        }
      }
    }
    tls {
      hosts       = ["minio.${local.environment_url}"]
      secret_name = "minio.${local.environment_url}"
    }
  }
}
