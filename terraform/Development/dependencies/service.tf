resource "kubernetes_service" "postgresql" {
  metadata {
    name      = "postgresql"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    selector = {
      "app" = local.selector
    }
    session_affinity = "None"
    type             = "ClusterIP"

    port {
      port        = 5432
      protocol    = "TCP"
      target_port = "5432"
    }
  }
}

resource "kubernetes_service" "minio" {
  metadata {
    name      = "minio"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    selector = {
      "app" = local.selector
    }
    session_affinity = "None"
    type             = "ClusterIP"

    port {
      port        = 9000
      protocol    = "TCP"
      target_port = "9000"
    }
  }
}
