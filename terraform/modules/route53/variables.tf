variable "app_name" {
  type        = string
}

variable "domain_name" {
  type        = string
}

variable "api_gateway_domain_name" {
  type = object({
    target_domain_name = string
    hosted_zone_id     = string
  })
}
