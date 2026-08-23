variable "ec2_instance" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "allowed_cidr" {
  description = "CIDR allowed to reach the EC2 instance (SSH and service ports)"
  type        = string
}
