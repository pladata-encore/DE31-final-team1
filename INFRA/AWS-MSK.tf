# 라우팅 테이블과 서브넷 연결
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

# 서브넷 생성
resource "aws_subnet" "msk1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "msk1-subnet"
  }
}

resource "aws_subnet" "msk2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "ap-northeast-2b"

  tags = {
    Name = "msk2-subnet"
  }
}

resource "aws_subnet" "msk3" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.12.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "msk3-subnet"
  }
}

# 저장된 데이터 암호화
# AWS Key Management Service(KMS)를 사용하여 CMK를 생성하고 관리
resource "aws_kms_key" "kms" {
  description = "encore"
}

# AWS MSK 클러스터 생성
resource "aws_msk_cluster" "DP" {
  cluster_name           = "DP"
  kafka_version          = "3.7.x.kraft"
  number_of_broker_nodes = 3

  client_authentication {
    sasl {
      iam = true
    }
  }

  broker_node_group_info {
    instance_type = "kafka.m5.large"

    client_subnets = [
      aws_subnet.msk1.id,
      aws_subnet.msk2.id,
      aws_subnet.msk3.id,
    ]
    storage_info {
      ebs_storage_info {
        volume_size = 1000
      }
    }
    security_groups = [aws_security_group.allow_all_internal.id]
  }

  encryption_info {
    encryption_at_rest_kms_key_arn = aws_kms_key.kms.arn
  }

  tags = {
    name = "main_kafka_cluster"
  }
}
