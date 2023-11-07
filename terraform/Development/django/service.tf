resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    selector = {
      "app" = var.PROJECT_NAME
    }
    session_affinity = "None"
    type             = "ClusterIP"

    port {
      port        = 8000
      protocol    = "TCP"
      target_port = "8000"
    }
  }
}

resource "kubernetes_service" "media" {
  metadata {
    name      = "media"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    selector = {
      "app" = var.PROJECT_NAME
    }
    session_affinity = "None"
    type             = "ClusterIP"

    port {
      port        = 80
      protocol    = "TCP"
      target_port = "80"
    }
  }
}

resource "kubernetes_service" "redis" {
  metadata {
    name      = "redis"
    namespace = var.KUBE_NAMESPACE
  }

  spec {
    selector = {
      "redis" = var.PROJECT_NAME
    }
    session_affinity = "None"
    type             = "ClusterIP"

    port {
      port        = 6379
      protocol    = "TCP"
      target_port = "6379"
    }
  }
}