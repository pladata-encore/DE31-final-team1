terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

resource "aws_vpc" "msk-vpc" {
  cidr_block = "192.168.0.0/16"
}

resource "aws_internet_gateway" "msk-igw" {
  vpc_id = aws_vpc.msk-vpc.id
}

resource "aws_route_table" "msk-rtb" {
  vpc_id = aws_vpc.msk-vpc.id
}

resource "aws_route" "msk-route" {
  route_table_id         = aws_vpc.msk-vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.msk-igw.id
}

resource "aws_route_table_association" "msk-subnet-association" {
  count          = length(data.aws_availability_zones.azs.names)
  subnet_id      = element([aws_subnet.subnet_az1.id, aws_subnet.subnet_az2.id, aws_subnet.subnet_az3.id], count.index)
  route_table_id = aws_route_table.msk-rtb.id
}

data "aws_availability_zones" "azs" {
  state = "available"
}

resource "aws_subnet" "subnet_az1" {
  availability_zone = data.aws_availability_zones.azs.names[0]
  cidr_block        = "192.168.1.0/24"
  vpc_id            = aws_vpc.msk-vpc.id
}

resource "aws_subnet" "subnet_az2" {
  availability_zone = data.aws_availability_zones.azs.names[1]
  cidr_block        = "192.168.2.0/24"
  vpc_id            = aws_vpc.msk-vpc.id
}

resource "aws_subnet" "subnet_az3" {
  availability_zone = data.aws_availability_zones.azs.names[2]
  cidr_block        = "192.168.3.0/24"
  vpc_id            = aws_vpc.msk-vpc.id
}

resource "aws_security_group" "msk-sg" {
  vpc_id = aws_vpc.msk-vpc.id
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_kms_key" "kms" {
  description = "encore"
}

resource "aws_msk_cluster" "test" {
  cluster_name           = "test"
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
      aws_subnet.subnet_az1.id,
      aws_subnet.subnet_az2.id,
      aws_subnet.subnet_az3.id,
    ]
    storage_info {
      ebs_storage_info {
        volume_size = 10
      }
    }
    security_groups = [aws_security_group.msk-sg.id]
  }

  encryption_info {
    encryption_at_rest_kms_key_arn = aws_kms_key.kms.arn
  }

  tags = {
    name = "MSK"
  }
}
