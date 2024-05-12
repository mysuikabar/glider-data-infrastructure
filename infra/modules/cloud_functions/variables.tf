variable "location" {
  type    = string
  default = "asia-northeast1"
}

variable "bucket_name_igc" {
  type = string
}

variable "function_name" {
  type    = string
  default = "igc_file_processor"
}

variable "dataset_id" {
  type = string
}

variable "table_id" {
  type = string
}