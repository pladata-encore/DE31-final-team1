# Configure the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  # Terraform 상태 파일을 S3에 저장하도록 설정
  # S3 버킷 이름 및 경로를 적절히 수정
  backend "s3" {
    bucket = "your-terraform-state-bucket" 
    key    = "terraform.tfstate"
    region = "ap-northeast-2"
  }
}

# AWS Provider 설정
provider "aws" {
  region = "ap-northeast-2" # 서울 리전
}

# VPC 생성
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16" # VPC CIDR 블록
  enable_dns_hostnames = true # DNS 호스트 이름 활성화
  enable_dns_support   = true # DNS 지원 활성화

  tags = {
    Name = "main-vpc"
  }
}

# Public Subnet 생성
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id # VPC ID 참조
  cidr_block = "10.0.1.0/24" # 서브넷 CIDR 블록
  availability_zone = "ap-northeast-2a" # 가용 영역 지정

  tags = {
    Name = "public-subnet"
  }
}

# ... (생략) 다른 서브넷 생성 (Private Subnet 등) - 필요에 따라 추가

# Internet Gateway 생성
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id # VPC ID 참조

  tags = {
    Name = "main-igw"
  }
}

# Public Route Table 생성
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id # VPC ID 참조

  route {
    cidr_block = "0.0.0.0/0" # 모든 트래픽을 인터넷 게이트웨이로 라우팅
    gateway_id = aws_internet_gateway.gw.id # 인터넷 게이트웨이 ID 참조
  }

  tags = {
    Name = "public-route-table"
  }
}

# Public Subnet Association 생성
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id # Public Subnet ID 참조
  route_table_id = aws_route_table.public.id # Public Route Table ID 참조
}

# ... (생략) 다른 서브넷에 대한 Route Table Association 생성 - 필요에 따라 추가

# MSK Cluster 생성
resource "aws_msk_cluster" "example" {
  cluster_name = "kafka-cluster"
  kafka_version = "2.8.1"
  number_of_broker_nodes = 3

  broker_node_group_info {
    instance_type = "kafka.m5.large"
    storage_info {
      ebs_storage_info {
        volume_size = 1000
      }
    }
    # Security Group 설정 (필요에 따라 추가)
    security_groups = [aws_security_group.msk.id]

    # Subnet 설정
    client_subnets = [
      aws_subnet.public.id,
      aws_subnet.public.id,
      aws_subnet.public.id,
    ]
  }

  tags = {
    Name = "main-kafka-cluster"
  }
}

# EC2 Instance 생성 (Airflow)
resource "aws_instance" "airflow" {
  ami           = "ami-09e67e426f25ce0d7" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.public.id # Public Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.airflow.id] 

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# Deploy Airflow using Docker Compose
cd DE31-final-team1/airflow
docker-compose up -d
EOF

  tags = {
    Name = "Airflow-Server"
  }
}

# EC2 Instance 생성 (NiFi)
resource "aws_instance" "nifi" {
  ami           = "ami-09e67e426f25ce0d7" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.public.id # Public Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.nifi.id] 

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# Deploy Airflow using Docker Compose
cd DE31-final-team1/nifi
docker-compose up -d
EOF

  tags = {
    Name = "NiFi-Server"
  }
}

# EC2 Instance 생성 (FE)
resource "aws_instance" "frontend" {
  ami           = "ami-09e67e426f25ce0d7" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.public.id # Public Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.frontend.id] 

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# Deploy Airflow using Docker Compose
cd DE31-final-team1/FE
docker-compose up -d
EOF

  tags = {
    Name = "Frontend-Server"
  }
}

# EC2 Instance 생성 (BE)
resource "aws_instance" "backend" {
  ami           = "ami-09e67e426f25ce0d7" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.public.id # Public Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.backend.id] 

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# Deploy Airflow using Docker Compose
cd DE31-final-team1/BE
docker-compose up -d
EOF

  tags = {
    Name = "Backend-Server"
  }
}

# EC2 Instance 생성 (MongoDB)
resource "aws_instance" "mongo" {
  ami           = "ami-09e67e426f25ce0d7" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.public.id # Public Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.mongo.id] 

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# Deploy Airflow using Docker Compose
cd DE31-final-team1/mongo
docker-compose up -d
EOF

  tags = {
    Name = "Mongo-Server"
  }
}

# Security Groups
# ... (생략) 각 인스턴스에 대한 보안 그룹 규칙 정의 - 필요에 따라 추가

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "cpu_utilization_airflow" {
  alarm_name                = "Airflow-CPU-Utilization-High"
  comparison_operator       = "GreaterThanThreshold"
  evaluation_periods        = 2
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = 60
  statistic                 = "Average"
  threshold                 = 80
  alarm_description          = "Airflow EC2 instance CPU utilization is high."
  dimensions = {
    InstanceId = aws_instance.airflow.id
  }

  alarm_actions = ["arn:aws:sns:ap-northeast-2:your-account-id:your-sns-topic"] # 알림을 받을 SNS 토픽 ARN
}

# ... (생략) 다른 CloudWatch 알람 생성 (메모리 사용량 등) - 필요에 따라 추가