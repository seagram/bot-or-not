variable "turso_database_url" {
  type        = string
  sensitive   = true
}

variable "turso_auth_token" {
  type        = string
  sensitive   = true
}

variable "domain_name" {
  type        = string
  default     = "botornot.tech"
}
