# Net work
resource "aws_vpc" "mlop_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
}

resource "aws_subnet" "db_subnet_mlop" {
  vpc_id     = aws_vpc.mlop_vpc.id
  cidr_block = "10.0.0.0/24"  # Adjust the CIDR block as needed
  availability_zone = var.aws_region_sn
}
resource "aws_subnet" "db_subnet_mlop2" {
  vpc_id     = aws_vpc.mlop_vpc.id
  cidr_block = "10.0.2.0/24"  # Adjust the CIDR block as needed
  availability_zone = var.aws_region_sn2
}

resource "aws_db_subnet_group" "db_subnet_mlop_group" {
  name       = "db-subnet-mlop-group"
  subnet_ids = [aws_subnet.db_subnet_mlop.id,aws_subnet.db_subnet_mlop2.id]
}

# Create an Internet Gateway
resource "aws_internet_gateway" "mlop_igw" {
  vpc_id = aws_vpc.mlop_vpc.id
}

# Update the main route table of the VPC to route traffic to the Internet Gateway
resource "aws_route" "mlop_route" {
  route_table_id         = aws_vpc.mlop_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.mlop_igw.id
}


resource "aws_security_group" "rds_sg" {
  name        = "rds_security_group"
  description = "Security group for RDS database"
  vpc_id = aws_vpc.mlop_vpc.id
  # Inbound rule to allow database connections
  ingress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Limit this to specific IPs if possible
  }
}


# Databaee
resource "aws_db_instance" "DB_ML" {
  allocated_storage    = 10
  storage_type        = "gp2"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = var.db_intance_type
  identifier          = var.db_identifier_ml
  db_name             = var.db_name_ml
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name = aws_db_subnet_group.db_subnet_mlop_group.name



  tags = {
    Name = "DB_ML"
  }
}

resource "aws_db_instance" "DB_MONI" {
  allocated_storage    = 10
  storage_type        = "gp2"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = var.db_intance_type
  identifier          = var.db_identifier_moni
  db_name             = var.db_name_moni
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true
  publicly_accessible = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name = aws_db_subnet_group.db_subnet_mlop_group.name

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

