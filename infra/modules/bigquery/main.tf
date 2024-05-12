resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset_id
  delete_contents_on_destroy = true
}