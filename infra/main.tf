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

module "functions" {
  source          = "./modules/cloud_functions"
  bucket_name_igc = var.bucket_name_igc
  dataset_id      = var.dataset_id
  table_id        = var.table_id
}

module "bigquery" {
  source     = "./modules/bigquery"
  dataset_id = var.dataset_id
}