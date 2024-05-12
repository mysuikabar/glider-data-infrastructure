variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-northeast1"
}

variable "bucket_name_igc" {
  type = string
}

variable "dataset_id" {
  type    = string
  default = "data_lake"
}

variable "table_id" {
  type    = string
  default = "flight_log"
}