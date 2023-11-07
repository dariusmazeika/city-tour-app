resource "kubernetes_persistent_volume_claim" "media" {
  metadata {
    name      = "persistent-storage"
    namespace = var.KUBE_NAMESPACE
  }
  wait_until_bound = false
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = var.minio_storage
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "database" {
  metadata {
    name      = "database-storage"
    namespace = var.KUBE_NAMESPACE
  }
  wait_until_bound = false
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "8Gi"
      }
    }
  }
}
