data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "${path.module}/function"
  output_path = "${path.module}/function.zip"
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "function_bucket" {
  name          = "${var.function_bucket_prefix}_${random_id.suffix.hex}"
  location      = var.location
  force_destroy = true
}

resource "google_storage_bucket_object" "function_source" {
  name   = "function.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_archive.output_path
}

resource "google_cloudfunctions_function" "function" {
  name                  = var.function_name
  runtime               = "python312"
  available_memory_mb   = var.function_available_memory_mb
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_source.name
  entry_point           = "main"
  trigger_http          = true
  environment_variables = {
    DATASET_ID = var.dataset_id
    TABLE_ID   = var.table_id
  }
}

resource "google_service_account" "scheduler_service_account" {
  account_id = "scheduler-sa"
}

resource "google_project_iam_member" "scheduler_invoker" {
  project = var.project_id
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.scheduler_service_account.email}"
}

resource "google_cloud_scheduler_job" "scheduler_job" {
  name      = var.scheduler_name
  schedule  = var.scheduler_schedule
  time_zone = var.scheduler_time_zone

  http_target {
    uri         = google_cloudfunctions_function.function.https_trigger_url
    http_method = "GET"
    oidc_token {
      service_account_email = google_service_account.scheduler_service_account.email
    }
  }
}