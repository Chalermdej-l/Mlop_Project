variable "aws_region" {
  type = string
}

variable "aws_region_sn" {
  type = string
}

variable "aws_region_sn2" {
  type = string
}

variable "db_name_ml" {
  type = string
}

variable "db_name_moni" {
  type = string
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_identifier_ml" {
  type = string
}

variable "db_identifier_moni" {
  type = string
}

variable "db_instance_type" {
  type = string
}

variable "ec2_instance" {
  type = string
}

variable "allowed_cidr" {
  description = "CIDR allowed to reach the EC2 instance (SSH and service ports), e.g. your egress IP as 203.0.113.7/32"
  type        = string
}
