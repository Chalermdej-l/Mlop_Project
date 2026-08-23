# Networking
resource "aws_vpc" "mlop_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "mlop-vpc"
  }
}

resource "aws_subnet" "db_subnet_mlop" {
  vpc_id            = aws_vpc.mlop_vpc.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = var.aws_region_sn
}

resource "aws_subnet" "db_subnet_mlop2" {
  vpc_id            = aws_vpc.mlop_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = var.aws_region_sn2
}

# Public subnet for the EC2 app server. Subnets associate with the VPC
# main route table by default, which routes 0.0.0.0/0 to the IGW below.
resource "aws_subnet" "app_subnet" {
  vpc_id            = aws_vpc.mlop_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.aws_region_sn
}

resource "aws_db_subnet_group" "db_subnet_mlop_group" {
  name       = "db-subnet-mlop-group"
  subnet_ids = [aws_subnet.db_subnet_mlop.id, aws_subnet.db_subnet_mlop2.id]
}

resource "aws_internet_gateway" "mlop_igw" {
  vpc_id = aws_vpc.mlop_vpc.id
}

resource "aws_route" "mlop_route" {
  route_table_id         = aws_vpc.mlop_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.mlop_igw.id
}

resource "aws_security_group" "rds_sg" {
  name        = "rds_security_group"
  description = "Security group for RDS databases (VPC traffic only)"
  vpc_id      = aws_vpc.mlop_vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.mlop_vpc.cidr_block]
  }
}

# Databases
resource "aws_db_instance" "DB_ML" {
  allocated_storage      = 10
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = var.db_instance_type
  identifier             = var.db_identifier_ml
  db_name                = var.db_name_ml
  username               = var.db_username
  password               = var.db_password
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_mlop_group.name

  tags = {
    Name = "DB_ML"
  }
}

resource "aws_db_instance" "DB_MONI" {
  allocated_storage      = 10
  storage_type           = "gp2"
  engine                 = "postgres"
  engine_version         = "15"
  instance_class         = var.db_instance_type
  identifier             = var.db_identifier_moni
  db_name                = var.db_name_moni
  username               = var.db_username
  password               = var.db_password
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_mlop_group.name

  tags = {
    Name = "DB_MONI"
  }
}

output "AWS_DB_ML" {
  value = aws_db_instance.DB_ML.endpoint
}

output "AWS_DB_MONITOR" {
  value = aws_db_instance.DB_MONI.endpoint
}

output "vpc_id" {
  value = aws_vpc.mlop_vpc.id
}

output "app_subnet_id" {
  value = aws_subnet.app_subnet.id
}
