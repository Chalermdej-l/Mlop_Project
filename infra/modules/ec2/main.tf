data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "tls_private_key" "generated_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "mlop_keypair" {
  key_name   = "mlop-keypair"
  public_key = tls_private_key.generated_key.public_key_openssh
}

resource "aws_security_group" "instance_sg" {
  name        = "instance-sg"
  description = "Security group for the MLop EC2 instance"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  ingress {
    from_port   = 9696
    to_port     = 9696
    protocol    = "tcp"
    cidr_blocks = [var.allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ec2_instance" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.ec2_instance
  subnet_id     = var.subnet_id

  key_name = aws_key_pair.mlop_keypair.key_name

  security_groups = [aws_security_group.instance_sg.name]
  root_block_device {
    volume_size = 20
  }
  tags = {
    Name = "MLop-projectserver"
  }
}

output "private_key_pem" {
  value     = tls_private_key.generated_key.private_key_pem
  sensitive = true
}

output "public_key_openssh" {
  value     = aws_key_pair.mlop_keypair.public_key
  sensitive = true
}

output "DBS_ENDPOINT" {
  value = aws_instance.ec2_instance.public_dns
}
