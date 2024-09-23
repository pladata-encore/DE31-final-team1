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
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "terraform.tfstate"
  #   region = "ap-northeast-2"
  # }
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
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # VPC CIDR 블록으로 변경
  }
  
  # nifi 웹 UI 접근을 위한 8443포트 개방
  ingress {
    from_port = 8443
    to_port = 8443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # airflow 웹 UI 접근을 위한 8080포트 개방
  ingress {
    from_port = 8080
    to_port = 8080
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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
  ami           = "ami-056a29f2eddc40520" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.xlarge"
  subnet_id     = aws_subnet.airflow.id # airflow Subnet ID 참조
  key_name      = "airflow_test_key" # Key Pair 이름
  associate_public_ip_address = true

  # airflow 애플리케이션의 용량으로 인해 볼륨 지정
  root_block_device {
    volume_size = 30  # 볼륨 크기 (GB)
    volume_type = "gp2"  # 기본 SSD (gp2)
    delete_on_termination = true  # 인스턴스 종료 시 볼륨 삭제 여부
  }  

  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

  user_data = <<EOF
#!/bin/bash
# 패키지 업데이트
sudo apt-get update -y

# Git 설치 (필요한 경우)
sudo apt-get install git -y

# Docker 설치
echo "Installing Docker..."
curl -sSL get.docker.com | sh

# Docker Compose 설치
echo "Installing Docker Compose..."
wget https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-x86_64

# Docker 소켓 권한 변경
echo "Changing Docker socket permissions..."
sudo chown -R ubuntu:ubuntu /var/run/docker.sock

# Docker 그룹에 유저 추가
echo "Adding user to Docker group..."
sudo usermod -aG docker ubuntu

# Docker Compose 실행 권한 부여 및 이동
echo "Setting up Docker Compose..."
chmod +x ./docker-compose-linux-x86_64
sudo mv ./docker-compose-linux-x86_64 /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 완료 메시지
echo "Docker and Docker Compose installation is complete. You can now use Docker without sudo."

# Git repository 클론
git clone https://github.com/pladata-encore/DE31-final-team1.git

# GitHub Secrets의 ENV_FILE을 .env 파일로 생성
cd DE31-final-team1/Airflow/docker
# GitHub Secrets에서 전달된 값을 .env로 저장
echo 'AIRFLOW_DATABASE_PASSWORD=${var.AIRFLOW_DATABASE_PASSWORD}' >> .env
echo 'AIRFLOW_EMAIL=${var.AIRFLOW_EMAIL}' >> .env
echo 'AIRFLOW_FERNET_KEY=${var.AIRFLOW_FERNET_KEY}' >> .env
echo 'AIRFLOW_PASSWORD=${var.AIRFLOW_PASSWORD}' >> .env
echo 'AIRFLOW_SECERT_KEY=${var.AIRFLOW_SECRET_KEY}' >> .env
echo 'AIRFLOW_USERNAME=${var.AIRFLOW_USERNAME}' >> .env
echo 'POSTGRESQL_DATABASE=${var.POSTGRESQL_DATABASE}' >> .env
echo 'POSTGRESQL_PASSWORD=${var.POSTGRESQL_PASSWORD}' >> .env
echo 'POSTGRESQL_USERNAME=${var.POSTGRESQL_USERNAME}' >> .env


# Airflow 설정 및 실행
chmod +x ./setup_permission.sh
./setup_permission.sh

docker-compose up -d
EOF

  tags = {
    Name = "Airflow-Server"
  }
}
# 고정 IP 할당(Airflow)
resource "aws_eip" "airflow_eip" {
  instance = aws_instance.airflow.id
  vpc      = true

  tags = {
    Name = "airflow-EIP"
  }
}

# 백엔드 IP 표시
output "airflow_public_ip" {
  value       = aws_eip.airflow_eip.public_ip
  description = "The public IP address of the airflow server"
}

# EC2 Instance 생성 (NiFi)
resource "aws_instance" "nifi" {
  ami           = "ami-056a29f2eddc40520" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.xlarge"
  subnet_id     = aws_subnet.nifi.id # nifi Subnet ID 참조
  key_name      = "nifi_test_key_pair" # Key Pair 이름
  associate_public_ip_address = true
  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

  user_data = <<EOF
#!/bin/bash
# Install Java, Docker, Docker Compose
# ... (Java, Docker, Docker Compose 설치 스크립트 추가)

sudo apt-get update
sudo apt-get install -y openjdk-11-jdk docker.io docker-compose git

sudo systemctl enable docker
sudo systemctl start docker

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# Get public IP from AWS EC2 metadata
PUBLIC_IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)

# Update docker-compose.yaml with the public IP using sed
sed -i "s/NIFI_WEB_PROXY_HOST=.*/NIFI_WEB_PROXY_HOST=$${PUBLIC_IP}:8443/" DE31-final-team1/NiFi/docker-compose.yaml

# Deploy nifi using Docker Compose
cd DE31-final-team1/Nifi

sudo docker-compose up -d
EOF

  tags = {
    Name = "NiFi-Server"
  }
}

# EC2 Instance 생성 (FE)
resource "aws_instance" "frontend" {
  ami           = "ami-056a29f2eddc40520" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.fe.id # Frontend Subnet ID 참조
  key_name      = "test_key_pair" # Key Pair 이름

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
  ami           = "ami-056a29f2eddc40520" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.large"
  subnet_id     = aws_subnet.be.id # Backend Subnet ID 참조
  key_name      = "nifi_test_key_pair" # Key Pair 이름
  associate_public_ip_address = true
  
  # 보안 그룹 설정
  vpc_security_group_ids = [aws_security_group.allow_all_internal.id]

  user_data = <<EOF
#!/bin/bash

# Install Docker
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone Git repository
git clone https://github.com/pladata-encore/DE31-final-team1.git

# AWS CLI configure
mkdir -p /home/ubuntu/.aws
echo '[default]' > /home/ubuntu/.aws/config
echo 'region = ap-northeast-2' >> /home/ubuntu/.aws/config
echo 'output = json' >> /home/ubuntu/.aws/config

# Set Environment Variables
echo 'KAFKA_BOOTSTRAP_SERVERS=${var.KAFKA_BOOTSTRAP_SERVERS}' >> /etc/environment  
echo 'MONGO=${var.MONGO}' >> /etc/environment
echo 'MONGO_COLLECTION_NAME=${var.MONGO_COLLECTION_NAME}' >> /etc/environment
echo 'MONGO_DATABASE_NAME=${var.MONGO_DATABASE_NAME}' >> /etc/environment
echo 'MONGO_URI=${var.MONGO_URI}' >> /etc/environment
echo 'MYSQL_URI=${var.MYSQL_URI}' >> /etc/environment  
echo 'NIFI_URL=${var.NIFI_URL}' >> /etc/environment

# Copy environment variables to .env file
grep -E 'KAFKA_BOOTSTRAP_SERVERS|MONGO|MONGO_COLLECTION_NAME|MONGO_DATABASE_NAME|MONGO_URI|MYSQL_URI|NIFI_URL' /etc/environment > /DE31-final-team1/BE/.env

# Deploy Airflow using Docker Compose
cd DE31-final-team1/BE
docker-compose up -d
EOF

  tags = {
    Name = "Backend-Server"
  }
}

# 고정 IP 할당(BE)
resource "aws_eip" "backend_eip" {
  instance = aws_instance.backend.id
  vpc      = true

  tags = {
    Name = "Backend-EIP"
  }
}

# 백엔드 IP 표시
output "backend_public_ip" {
  value       = aws_eip.backend_eip.public_ip
  description = "The public IP address of the backend server"
}

# EC2 Instance 생성 (MongoDB)
resource "aws_instance" "mongo" {
  ami           = "ami-056a29f2eddc40520" # Ubuntu 22.04 LTS AMI (서울 리전)
  instance_type = "m5.xlarge"
  subnet_id     = aws_subnet.mongodb.id # MongoDB Subnet ID 참조
  key_name      = "test_key_pair" # Key Pair 이름

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


# # CloudWatch Alarms
# resource "aws_cloudwatch_metric_alarm" "cpu_utilization_airflow" {
#   alarm_name                = "Airflow-CPU-Utilization-High"
#   comparison_operator       = "GreaterThanThreshold"
#   evaluation_periods        = 2
#   metric_name               = "CPUUtilization"
#   namespace                 = "AWS/EC2"
#   period                    = 60
#   statistic                 = "Average"
#   threshold                 = 80
#   alarm_description          = "Airflow EC2 instance CPU utilization is high."
#   dimensions = {
#     InstanceId = aws_instance.airflow.id
#   }

#   alarm_actions = ["arn:aws:sns:ap-northeast-2:your-account-id:your-sns-topic"] # 알림을 받을 SNS 토픽  ########### 추후 변경해야함
# }

# ... (생략) 다른 CloudWatch 알람 생성 (메모리 사용량 등) - 필요에 따라 추가