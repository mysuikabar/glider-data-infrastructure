terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.25.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "bigquery" {
  source     = "./modules/bigquery"
  dataset_id = "data_lake"
}

module "igc_file_processor" {
  source                       = "./modules/storage_triggered_function"
  source_bucket_prefix         = "igc_files"
  function_bucket_prefix       = "igc_file_processor"
  function_name                = "igc_file_processor"
  function_available_memory_mb = 256
  dataset_id                   = "data_lake"
  table_id                     = "flight_log"
}

module "amedas_scraper" {
  project_id                   = var.project_id
  source                       = "./modules/scheduled_function"
  function_bucket_prefix       = "amedas_scraper"
  function_name                = "amedas_scraper"
  function_available_memory_mb = 256
  dataset_id                   = "data_lake"
  table_id                     = "amedas"
  scheduler_name               = "amedas_scraper"
  scheduler_schedule           = "0 3 * * *"
  scheduler_time_zone          = "Asia/Tokyo"
}