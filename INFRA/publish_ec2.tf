terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

# 새로운 Key Pair 생성
resource "aws_key_pair" "example" {
  key_name   = "jenkins-ec2-key"
  public_key = file("~/.ssh/id_rsa.pub") # 로컬 PC의 공개 키 파일 경로 수정
}

resource "aws_instance" "example" {
  ami           = "ami-0023481579962abd4" # Amazon Linux 2023 AMI (ap-northeast-2) 2024-09-06 기준 최신
  instance_type = "t2.micro"
  key_name      = aws_key_pair.example.key_name

  tags = {
    Name = "Jenkins-Automated-EC2"
  }
}

# 생성된 Key Pair의 Private Key 출력 (로컬에 저장 필요)
output "private_key" {
  value     = aws_key_pair.example.private_key
  sensitive = true
}
