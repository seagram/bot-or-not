output "route53_nameservers" {
  value       = aws_route53_zone.main.name_servers
}

output "route53_zone_id" {
  value       = aws_route53_zone.main.zone_id
}

output "acm_certificate_arn" {
  value       = aws_acm_certificate.api.arn
}
