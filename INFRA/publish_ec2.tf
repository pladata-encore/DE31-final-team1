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
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

# 서브넷 생성 (각 서비스별로 하나씩)
resource "aws_subnet" "msk1" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.10.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "msk1-subnet"
  }
}

resource "aws_subnet" "msk2" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.11.0/24"
  availability_zone = "ap-northeast-2b"

  tags = {
    Name = "msk2-subnet"
  }
}

resource "aws_subnet" "msk3" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.12.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "msk3-subnet"
  }
}

resource "aws_subnet" "airflow" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "airflow-subnet"
  }
}

resource "aws_subnet" "nifi" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "nifi-subnet"
  }
}

resource "aws_subnet" "fe" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "fe-subnet"
  }
}

resource "aws_subnet" "be" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "ap-northeast-2b"

  tags = {
    Name = "be-subnet"
  }
}

resource "aws_subnet" "mongodb" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.5.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "mongodb-subnet"
  }
}

##########################################################################

# Security Groups
# 모든 입출력을 허용하는 보안 그룹 생성 (VPC 내부 IP만 허용)
resource "aws_security_group" "allow_all_internal" {
  name = "allow_all_internal"
  description = "Allow all traffic from internal IPs"
  vpc_id = aws_vpc.main.id

  # 인바운드 규칙: VPC 내부 IP에서 모든 포트 허용
  ingress {
    from_port = 0
    to_port = 65535
    protocol = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # VPC CIDR 블록으로 변경
  }

  ingress {
    from_port = 0
    to_port = 65535
    protocol = "udp"
    cidr_blocks = ["10.0.0.0/16"]  # VPC CIDR 블록으로 변경
  }

  # 아웃바운드 규칙: 모든 곳으로 모든 트래픽 허용
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_all_internal"
  }
}

###########################################################################

# Internet Gateway 생성
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id # VPC ID 참조

  tags = {
    Name = "main-igw"
  }
}


##############################################################################

# 서브넷 라우팅 테이블 설정 (모든 서브넷에 대해 VPC 라우팅 설정)
resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id # 인터넷 게이트웨이 연결 (필요한 경우)
  }

  tags = {
    Name = "main-route-table"
  }
}

# 서브넷 연결
resource "aws_route_table_association" "msk1" {
  subnet_id      = aws_subnet.msk1.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "msk2" {
  subnet_id      = aws_subnet.msk2.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "msk3" {
  subnet_id      = aws_subnet.msk3.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "airflow" {
  subnet_id      = aws_subnet.airflow.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "nifi" {
  subnet_id      = aws_subnet.nifi.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "fe" {
  subnet_id      = aws_subnet.fe.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "be" {
  subnet_id      = aws_subnet.be.id
  route_table_id = aws_route_table.main.id
}

resource "aws_route_table_association" "mongodb" {
  subnet_id      = aws_subnet.mongodb.id
  route_table_id = aws_route_table.main.id
}

##################################################################3

# MSK Cluster 생성
resource "aws_msk_cluster" "example" {
  cluster_name = "kafka-cluster"
  kafka_version = "2.8.1"
  number_of_broker_nodes = 3

  broker_node_group_info {
    instance_type = "kafka.m5.large"
    storage_info {
      ebs_storage_info {
        volume_size = 10
      }
    }
    # Security Group 설정 (필요에 따라 추가)
    security_groups = [aws_security_group.allow_all_internal.id]

    # Subnet 설정
    client_subnets = [
      aws_subnet.msk1.id,
      aws_subnet.msk2.id,
      aws_subnet.msk3.id
    ]
  }

  tags = {
    Name = "main-kafka-cluster"
  }
}

# EC2 Instance 생성 (Airflow)
resource "aws_instance" "airflow" {
  ami           = "ami-09e67e426f25ce0d7" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.xlarge"
  subnet_id     = aws_subnet.airflow.id # airflow Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

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
  instance_type = "m5.xlarge"
  subnet_id     = aws_subnet.nifi.id # nifi Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

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
  subnet_id     = aws_subnet.fe.id # Frontend Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

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
  subnet_id     = aws_subnet.be.id # Backend Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# AWS CLI configure
mkdir -p /home/ubuntu/.aws
echo '[default]' > /home/ubuntu/.aws/config
echo 'region = ap-northeast-2' >> /home/ubuntu/.aws/config
echo 'output = json' >> /home/ubuntu/.aws/config

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
  instance_type = "m5.xlarge"
  subnet_id     = aws_subnet.mongodb.id # MongoDB Subnet ID 참조
  key_name      = "your-key-pair-name" # Key Pair 이름

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

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



#####################################################################




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

  alarm_actions = ["arn:aws:sns:ap-northeast-2:your-account-id:your-sns-topic"] # 알림을 받을 SNS 토픽  ########### 추후 변경해야함
}

# ... (생략) 다른 CloudWatch 알람 생성 (메모리 사용량 등) - 필요에 따라 추가