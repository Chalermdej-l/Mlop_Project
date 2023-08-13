provider "aws" {
  region = var.aws_region
}

resource "aws_db_instance" "DB_ML" {
  allocated_storage    = 20
  storage_type        = "gp2"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = "db.m5d.large"
  identifier          = var.db_identifier_ml
  db_name             = var.db_name_ml
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true
  publicly_accessible = true

  tags = {
    Name = "DB_ML"
  }
}

resource "aws_db_instance" "DB_MONI" {
  allocated_storage    = 20
  storage_type        = "gp2"
  engine              = "postgres"
  engine_version      = "15"
  instance_class      = "db.m5d.large"
  identifier          = var.db_identifier_moni
  db_name             = var.db_name_moni
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true
  publicly_accessible = true
  tags = {
    Name = "DB_MONI"
  }
}
