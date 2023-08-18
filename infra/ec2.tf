
resource "tls_private_key" "generated_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "mlop_keypair" {
  key_name   = "example-keypair"
  public_key = tls_private_key.generated_key.public_key_openssh
}

resource "aws_security_group" "instance_sg" {
  name        = "instance-sg"
  description = "Security group for EC2 instance"
  
  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH access from anywhere (not recommended for production)
  }
  
  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outbound traffic (not recommended for production)
  }
}

resource "aws_instance" "ec2_instance" {
  ami           = "ami-091a58610910a87a9"
  instance_type = "t2.micro"

  key_name      = aws_key_pair.mlop_keypair.key_name  # Use the created key pair

  security_groups = [aws_security_group.instance_sg.name]

  tags = {
    Name = "MLop-projectserver"
  }
}

output "private_key_pem" {
  value = tls_private_key.generated_key.private_key_pem
  sensitive = true
}

output "public_key_openssh" {
  value = aws_key_pair.mlop_keypair.public_key
  sensitive = true
}

output "instance_dns_name" {
  value = aws_instance.ec2_instance.public_dns
}