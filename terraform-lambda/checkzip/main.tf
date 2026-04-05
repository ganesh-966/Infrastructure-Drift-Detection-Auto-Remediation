terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket-12345a"   # your S3 bucket
    key            = "terraform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "terraform-lock"
  }
}



provider "aws" {
  region = "ap-southeast-1"
}

# ---------------------------
# Security Group
# ---------------------------
resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow SSH and HTTP access"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ---------------------------
# EC2 Instance
# ---------------------------
resource "aws_instance" "web_server" {
  ami           = "ami-0e7ff22101b84bcff" # Amazon Linux 2 (verify for ap-southeast-1)
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "Terraform-EC2"
  }
}

# ---------------------------
# S3 Bucket
# ---------------------------
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-terraform-bucket-67890"

  tags = {
    Name        = "TerraformBucket"
    Environment = "Dev"
  }
}