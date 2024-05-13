variable "location" {
  type    = string
  default = "asia-northeast1"
}

variable "function_bucket_prefix" {
  type = string
}

variable "function_name" {
  type = string
}

variable "function_available_memory_mb" {
  type = number
}

variable "dataset_id" {
  type = string
}

variable "table_id" {
  type = string
}

variable "scheduler_name" {
  type = string
}

variable "scheduler_schedule" {
  type = string
}

variable "scheduler_time_zone" {
  type = string
}