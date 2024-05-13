variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-northeast1"
}

variable "source_bucket_prefix" {
  type    = string
  default = "igc_files"
}

variable "function_bucket_prefix" {
  type    = string
  default = "igc_file_processor"
}

variable "function_name" {
  type    = string
  default = "igc_file_processor"
}

variable "dataset_id" {
  type    = string
  default = "data_lake"
}

variable "table_id" {
  type    = string
  default = "flight_log"
}